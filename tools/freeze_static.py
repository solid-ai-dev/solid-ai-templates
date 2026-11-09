"""Write the static-check freeze into pyproject.toml from the tools' own output.

The freeze lists each module the strict type checker still faults and each
file the formatter would still change. It is generated, never written by hand,
and it only shrinks: a module or file is taken off as it is cleaned, and one
that newly fails is refused, never added.

Usage:
  py tools/freeze_static.py              # rewrite the freeze
  py tools/freeze_static.py --check      # fail when the freeze is not current
  py tools/freeze_static.py --self-test  # check the rules on planted cases
"""

from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import tempfile
from typing import Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYPROJECT = os.path.join(ROOT, "pyproject.toml")
ROOTS = ["tools", "tests", "hooks"]

# The width .editorconfig declares for Python.
WIDTH = 88

BEGIN = "# generated:static-freeze"
END = "# /generated:static-freeze"
BLOCK = re.compile(re.escape(BEGIN) + r"\n.*?" + re.escape(END), re.S)
FAULT = re.compile(r"^(?P<path>[^:\n]+\.py):\d+: error:", re.M)

# The formatter names a file it would change in one of two shapes, by version:
# "Would reformat: <path>", or "unformatted: ..." with "--> <path>:<line>"
# below it.
UNFORMATTED = re.compile(
    r"^(?:Would reformat: (?P<old>.+\.py)$"
    r"|unformatted: .*\n\s*--> (?P<new>[^:\n]+\.py):)",
    re.M,
)

# A list in the block: its key, then one quoted name a line.
LISTED = r"^%s = \[\n(?P<names>(?:    \"[^\"]+\",\n)*)\]"


class ToolFailed(Exception):
    """A checker that did not finish its scan, so its output is no baseline."""


def module_of(path: str) -> str:
    """The module name the type checker gives a file: its name, prefixed by
    each enclosing directory that is a package."""
    parts = [os.path.splitext(os.path.basename(path))[0]]
    folder = os.path.dirname(path)
    while os.path.isfile(os.path.join(ROOT, folder, "__init__.py")):
        parts.insert(0, os.path.basename(folder))
        folder = os.path.dirname(folder)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def run(command: list[str]) -> Tuple[int, str]:
    """A command's exit status and output, run from the root."""
    done = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    return done.returncode, done.stdout + done.stderr


def findings(name: str, status: int, output: str, found: list[str]) -> list[str]:
    """What a checker found, refused unless its run reads as a finished scan.

    Both checkers exit 0 when clean and 1 when they find something. A missing
    module also exits 1, and a crash exits 2, so an exit of 1 counts only with
    findings parsed from it, and anything else is a failed run.
    """
    if status == 0 and not found:
        return found
    if status == 1 and found:
        return found
    raise ToolFailed(
        "%s did not finish its scan (exit %d): %s"
        % (name, status, output.strip()[:300])
    )


def faulted_modules() -> list[str]:
    """Every module the strict type checker faults, read with an empty
    config so the freeze in force does not hide what it freezes."""
    with tempfile.NamedTemporaryFile("w", suffix=".ini", delete=False) as handle:
        handle.write("[mypy]\n")
    try:
        status, output = run(
            [sys.executable, "-m", "mypy", "--strict", "--config-file", handle.name]
            + ["--no-incremental"]
            + ROOTS
        )
    finally:
        os.remove(handle.name)
    paths = {match.group("path").replace("\\", "/") for match in FAULT.finditer(output)}
    return sorted(
        {module_of(path) for path in findings("mypy", status, output, sorted(paths))}
    )


def unformatted_files() -> list[str]:
    """Every file the formatter would change at the project's width."""
    status, output = run(
        [sys.executable, "-m", "ruff", "format", "--check", "--isolated"]
        + ["--line-length", str(WIDTH)]
        + ROOTS
    )
    found = sorted(
        {
            (match.group("old") or match.group("new")).strip().replace("\\", "/")
            for match in UNFORMATTED.finditer(output)
        }
    )
    return findings("ruff format", status, output, found)


def frozen(text: str) -> Optional[Tuple[list[str], list[str]]]:
    """The modules and files the freeze in a pyproject text holds, or None
    where it holds no freeze yet."""
    block = BLOCK.search(text)
    if not block:
        return None
    lists = []
    for key in ("module", "extend-exclude"):
        match = re.search(LISTED % re.escape(key), block.group(0), re.M)
        names = match.group("names") if match else ""
        lists.append(re.findall(r"\"([^\"]+)\"", names))
    return lists[0], lists[1]


def added(
    current: Optional[Tuple[list[str], list[str]]],
    modules: list[str],
    files: list[str],
) -> list[str]:
    """What a regenerated freeze would add to the one in force; nothing where
    none is in force yet, since the first freeze is the adoption."""
    if current is None:
        return []
    return sorted(set(modules) - set(current[0])) + sorted(set(files) - set(current[1]))


def listed(names: list[str]) -> str:
    return "".join('    "%s",\n' % name for name in names)


def freeze_block(modules: list[str], files: list[str]) -> str:
    """The generated block for the modules and files still frozen."""
    lines = [
        BEGIN,
        "# Written by tools/freeze_static.py; never edit by hand.",
        "[tool.mypy]",
        "strict = true",
        "files = [%s]" % ", ".join('"%s"' % root for root in ROOTS),
        "",
    ]
    if modules:
        lines += [
            "[[tool.mypy.overrides]]",
            "module = [",
            listed(modules).rstrip("\n"),
            "]",
            "ignore_errors = true",
            "",
        ]
    lines += ["[tool.ruff]", "line-length = %d" % WIDTH]
    if files:
        lines += ["extend-exclude = [", listed(files).rstrip("\n"), "]"]
    lines.append(END)
    return "\n".join(lines)


def self_test() -> int:
    """The shrink-only rule and the failed-run rule, on planted cases."""
    block = freeze_block(["a", "b"], ["x.py"])
    current = frozen("head\n\n" + block + "\n")
    checks = [
        (
            "a block reads back as the lists it was written from",
            current == (["a", "b"], ["x.py"]),
        ),
        (
            "no freeze in force: the first freeze adds freely",
            added(None, ["a"], ["x.py"]) == [],
        ),
        (
            "a module or file newly failing is an addition, refused",
            added(current, ["a", "b", "c"], ["x.py", "y.py"]) == ["c", "y.py"],
        ),
        (
            "a cleaned module or file leaves without an addition",
            added(current, ["a"], []) == [],
        ),
        ("a clean run finds nothing", findings("t", 0, "Success", []) == []),
        (
            "a run with findings returns them",
            findings("t", 1, "x.py:1: error:", ["x.py"]) == ["x.py"],
        ),
    ]
    for label, status, output in (
        ("a missing checker is a failed run", 1, "No module named mypy"),
        ("a crash is a failed run", 2, "Traceback"),
        ("a clean exit with findings is a failed run", 0, "x.py:1: error:"),
    ):
        try:
            findings("t", status, output, ["x.py"] if status == 0 else [])
            checks.append((label, False))
        except ToolFailed:
            checks.append((label, True))
    for label, ok in checks:
        print("  %-58s %s" % (label, "ok" if ok else "FAILED"))
    passed = sum(1 for _, ok in checks if ok)
    print(
        "VERDICT: %s - %d/%d case(s) passed"
        % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks))
    )
    return 0 if passed == len(checks) else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    with io.open(PYPROJECT, encoding="utf-8") as handle:
        text = handle.read()
    try:
        modules, files = faulted_modules(), unformatted_files()
    except ToolFailed as error:
        print("refused: %s" % error)
        return 2
    new = added(frozen(text), modules, files)
    if new:
        print("refused: the freeze only shrinks; clean these instead:")
        for name in new:
            print("  %s" % name)
        return 1
    block = freeze_block(modules, files)
    if BLOCK.search(text):
        updated = BLOCK.sub(lambda _: block, text)
    else:
        updated = text.rstrip("\n") + "\n\n" + block + "\n"
    if "--check" in argv:
        if updated != text:
            print(
                "the static-check freeze is not current; run py tools/freeze_static.py"
            )
            return 1
        return 0
    with io.open(PYPROJECT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(updated)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
