"""Write the static-check freeze into pyproject.toml from the tools' own output.

The freeze lists each module the strict type checker still faults and each
file the formatter would still change. It is generated, never written by hand,
and it only shrinks: a module or file is taken off as it is cleaned.

Usage:
  py tools/freeze_static.py          # rewrite the freeze
  py tools/freeze_static.py --check  # fail when the freeze is not current
"""

from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import tempfile

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


def run(command: list[str]) -> str:
    """A command's output, run from the root with no config file of ours."""
    done = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    return done.stdout + done.stderr


def faulted_modules() -> list[str]:
    """Every module the strict type checker faults, read with an empty
    config so the freeze in force does not hide what it freezes."""
    with tempfile.NamedTemporaryFile("w", suffix=".ini", delete=False) as handle:
        handle.write("[mypy]\n")
    try:
        output = run(
            [
                sys.executable,
                "-m",
                "mypy",
                "--strict",
                "--config-file",
                handle.name,
                "--no-incremental",
            ]
            + ROOTS
        )
    finally:
        os.remove(handle.name)
    paths = {match.group("path").replace("\\", "/") for match in FAULT.finditer(output)}
    return sorted({module_of(path) for path in paths})


def unformatted_files() -> list[str]:
    """Every file the formatter would change at the project's width."""
    output = run(
        [
            sys.executable,
            "-m",
            "ruff",
            "format",
            "--check",
            "--isolated",
            "--line-length",
            str(WIDTH),
        ]
        + ROOTS
    )
    return sorted(
        {
            (match.group("old") or match.group("new")).strip().replace("\\", "/")
            for match in UNFORMATTED.finditer(output)
        }
    )


def listed(names: list[str]) -> str:
    return "".join('    "%s",\n' % name for name in names)


def freeze_block() -> str:
    """The generated block, from both tools' output now."""
    modules, files = faulted_modules(), unformatted_files()
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


def main(argv: list[str]) -> int:
    with io.open(PYPROJECT, encoding="utf-8") as handle:
        text = handle.read()
    block = freeze_block()
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
