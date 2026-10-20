"""Smoke check SYS-23: the shipped hooks, as a consumer meets them.

A template names a hook by its pre-commit command, so a renamed or removed
hook leaves a rule pointing at nothing. A hook that cannot fail is the
decoration the gate rules forbid, so each one runs against a planted
violation and a clean subject in a throwaway repository.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

from testkit import ROOT, template_files
from .common import HAS_YAML, Inspected, MISSING_YAML, read, yaml

HOOKS_DIR = os.path.join(ROOT, "hooks")
HOOK_COMMAND = re.compile(r"^\s*pre-commit run ([a-z0-9-]+)\b", re.M)

FENCE = "`" * 3

# Built rather than spelled, so the bare-suppression scan, which reads this
# file too, does not find its own planted case.
HASH = chr(35)

# (hook, label, files to plant, args, exit owed, findings owed). The second
# case of each pair is the clean subject: a hook that flags it is as blind
# as one that misses the plant.
CASES = [
    ("find-unfenced-checks", "a check typed into prose",
     {"rules.md": "Run the gate.\n\nVerify with `git status`.\n"},
     [], 1, 1),
    ("find-unfenced-checks", "the same check in a fence",
     {"rules.md": "Run the gate:\n\n%s\ngit status\n%s\n" % (FENCE, FENCE)},
     [], 0, 0),
    ("compile-embedded-checks", "a heredoc check that does not compile",
     {"rules.md": "%sbash\npy - <<'EOF'\nprint(\nEOF\n%s\n" % (FENCE, FENCE)},
     [], 1, 1),
    ("compile-embedded-checks", "a heredoc check that compiles",
     {"rules.md": "%sbash\npy - <<'EOF'\nprint(1)\nEOF\n%s\n" % (FENCE, FENCE)},
     [], 0, 0),
    ("compile-embedded-checks", "no heredoc check at all",
     {"rules.md": "Prose only.\n"}, [], 3, 0),
    ("find-line-continuations", "a continued line in a check",
     {"rules.md": "%sbash\nls %s\n  -la\n%s\n" % (FENCE, chr(92), FENCE)},
     [], 0, 1),
    ("find-line-continuations", "no block in a check language",
     {"rules.md": "%syaml\nkey: value\n%s\n" % (FENCE, FENCE)}, [], 3, 0),
    ("find-bare-suppressions", "a suppression naming no rule",
     {"app.py": "import os  %s noqa\n" % HASH}, [], 1, 1),
    ("find-bare-suppressions", "a suppression naming its rule",
     {"app.py": "import os  %s noqa: F401\n" % HASH}, [], 0, 0),
]


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=smoke", "-c",
                    "user.email=smoke@example.invalid"] + list(args),
                   cwd=cwd, check=True, capture_output=True)


def run_hook(cwd, hook, args, pre_commit=False):
    env = dict(os.environ, PYTHONPATH=HOOKS_DIR)
    argv = [sys.executable, "-m", "solid_ai_checks", hook] + list(args)
    if pre_commit:
        argv.append("--pre-commit")
    proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    findings = [l for l in lines if re.match(r"^\S+:[0-9]+: [A-Z]+ ", l)]
    return proc.returncode, lines, findings


def planted_repo(files):
    """A throwaway repository holding `files`, all committed."""
    work = tempfile.mkdtemp(prefix="sait-hooks-")
    git(work, "init", "-q")
    for name, text in files.items():
        with open(os.path.join(work, name), "w", encoding="utf-8",
                  newline="\n") as handle:
            handle.write(text)
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "plant")
    return work


def test_edit_cases():
    """report-test-edits against a base, an added test and an edited one."""
    failures = []
    work = planted_repo({"README.md": "x\n"})
    try:
        os.makedirs(os.path.join(work, "tests"))
        with open(os.path.join(work, "tests", "test_a.py"), "w") as handle:
            handle.write("assert True\n")
        git(work, "add", "-A")
        git(work, "commit", "-q", "-m", "base")
        git(work, "branch", "base")

        code, lines, _ = run_hook(work, "report-test-edits", ["--base", "base"])
        if code != 3:
            failures.append("  report-test-edits, HEAD at the base: exited "
                            "%d, owed 3" % code)
        code, lines, _ = run_hook(work, "report-test-edits",
                                  ["--base", "base"], pre_commit=True)
        if code != 0 or not any(l.startswith("not applicable:")
                                for l in lines):
            failures.append("  report-test-edits under pre-commit, HEAD at "
                            "the base: exited %d without a not-applicable "
                            "line" % code)

        with open(os.path.join(work, "tests", "test_a.py"), "w") as handle:
            handle.write("assert 1\n")
        git(work, "commit", "-q", "-am", "loosen")
        code, lines, findings = run_hook(work, "report-test-edits",
                                         ["--base", "base"])
        owed = "changes that are not pure additions: 1"
        if code != 0 or owed not in lines or len(findings) != 1:
            failures.append("  report-test-edits, an edited test: exited %d, "
                            "printed %s" % (code, lines))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return failures


def check_sys_23():
    if not HAS_YAML:
        return [MISSING_YAML]

    seen = Inspected()
    failures = []

    manifest = yaml.safe_load(read(os.path.join(ROOT, ".pre-commit-hooks.yaml")))
    shipped = {h["id"]: h for h in seen.count("hooks in the manifest",
                                              manifest or [])}
    sys.path.insert(0, HOOKS_DIR)
    try:
        from solid_ai_checks.__main__ import HOOKS
    finally:
        sys.path.remove(HOOKS_DIR)
    for hook in sorted(set(shipped) ^ set(HOOKS)):
        failures.append("  %s: in one of .pre-commit-hooks.yaml and "
                        "solid_ai_checks.HOOKS, not both" % hook)
    for hook, entry in sorted(shipped.items()):
        owed = "solid-ai-checks %s --pre-commit" % hook
        if entry.get("entry") != owed:
            failures.append("  %s: entry is %r, owed %r"
                            % (hook, entry.get("entry"), owed))

    named = 0
    for rel in template_files():
        text = read(os.path.join(ROOT, rel))
        for hook in HOOK_COMMAND.findall(text):
            named += 1
            if hook not in shipped:
                failures.append("  %s names hook %s, which no manifest "
                                "entry ships" % (rel, hook))
    seen.count("hook commands named in templates", named)

    seen.count("planted cases", CASES)
    for hook, label, files, args, code_owed, found_owed in CASES:
        work = planted_repo(files)
        try:
            code, lines, findings = run_hook(work, hook, args)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if code != code_owed or len(findings) != found_owed:
            failures.append("  %s, %s: exited %d with %d finding(s), owed "
                            "%d with %d" % (hook, label, code, len(findings),
                                            code_owed, found_owed))
    failures += test_edit_cases()
    return seen.failures() + failures, seen.notes()
