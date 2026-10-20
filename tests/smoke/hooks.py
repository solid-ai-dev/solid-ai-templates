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

    # git prints `docs/rules.md`; a root written another way must still
    # reach it, and `.` means the whole tree.
    ("find-unfenced-checks", "a root written as ./docs",
     {"docs/rules.md": "Verify with `git status`.\n"}, ["--root", "./docs"],
     1, 1),
    ("find-unfenced-checks", "a root of .",
     {"docs/rules.md": "Verify with `git status`.\n"}, ["--root", "."],
     1, 1),
    ("check-ascii-identifiers", "an identifier with an accented letter",
     {"app.py": "caf%s = 1\n" % chr(233)}, [], 1, 1),
    ("check-ascii-identifiers", "an ASCII identifier",
     {"app.py": "cafe = 1\n"}, [], 0, 0),
    ("check-ascii-identifiers", "no Python file",
     {"README.md": "x\n"}, [], 3, 0),
    ("check-comment-layout", "a comment block with code directly above",
     {"app.py": "x = 1\n%s note\ny = 2\n" % HASH}, [], 1, 1),
    ("check-comment-layout", "an aside to the right of code",
     {"app.py": "x = 1  %s note\n" % HASH}, [], 1, 1),
    ("check-comment-layout", "a comment above its item, after a blank line",
     {"app.py": "x = 1\n\n%s note\ny = 2\n" % HASH}, [], 0, 0),
    ("find-import-bans", "a domain module importing an adapter",
     {"domain/core.py": "import adapters.db\n", "adapters/db.py": "x = 1\n"},
     ["--forbid", "domain:adapters"], 1, 1),
    ("find-import-bans", "a domain module importing nothing banned",
     {"domain/core.py": "import os\n", "adapters/db.py": "x = 1\n"},
     ["--forbid", "domain:adapters"], 0, 0),
    ("find-import-bans", "no ban declared",
     {"domain/core.py": "import adapters.db\n"}, [], 3, 0),
    ("find-import-bans", "a ban written without its colon",
     {"domain/core.py": "import adapters.db\n"},
     ["--forbid", "domain=adapters"], 1, 1),
    ("find-import-bans", "a ban with a doubled colon",
     {"domain/core.py": "import adapters.db\n"},
     ["--forbid", "domain::adapters"], 1, 1),
    ("find-import-bans", "a ban whose side is not a module name",
     {"domain/core.py": "import adapters.db\n"},
     ["--forbid", "domain:adapters."], 1, 1),
    ("find-import-bans", "a malformed ban beside a valid one",
     {"domain/core.py": "import os\n"},
     ["--forbid", "domain:adapters", "--forbid", ":adapters"], 1, 1),
    ("find-unreferenced-scripts", "a script nothing names",
     {"scripts/old.py": "x = 1\n", "README.md": "Nothing here.\n"},
     [], 1, 1),
    ("find-unreferenced-scripts", "a script the README names",
     {"scripts/old.py": "x = 1\n", "README.md": "Run old.py.\n"}, [], 0, 0),
    ("find-unreferenced-scripts", "no scripts directory",
     {"README.md": "x\n"}, [], 3, 0),
    ("check-heading-numbers", "two sections numbered alike",
     {"spec.md": "## 1 One\n\n## 2 Two\n\n## 2 Again\n"},
     ["--path", "spec.md"], 1, 1),
    ("check-heading-numbers", "a skipped list ordinal",
     {"spec.md": "## Steps\n\n1. One\n2. Two\n4. Four\n"},
     ["--path", "spec.md"], 1, 1),
    ("check-heading-numbers", "a consistent document",
     {"spec.md": "## 1 One\n\n1. a\n2. b\n\n## 2 Two\n\n### 2.1 Sub\n"},
     ["--path", "spec.md"], 0, 0),
    ("check-heading-numbers", "a document with no ordinal",
     {"spec.md": "## Plain\n\nText.\n"}, ["--path", "spec.md"], 1, 1),
    ("check-heading-numbers", "no document named",
     {"spec.md": "## 1 One\n"}, [], 3, 0),
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
    findings = [l for l in lines if re.match(r"^\S+:[0-9]+: [A-Z-]+ ", l)]
    return proc.returncode, lines, findings


def planted_repo(files):
    """A throwaway repository holding `files`, all committed."""
    work = tempfile.mkdtemp(prefix="sait-hooks-")
    git(work, "init", "-q")
    for name, text in files.items():
        path = os.path.join(work, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8",
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

        # A base that does not resolve is a missing baseline, and a run
        # that compared nothing fails in either mode.
        for pre_commit in (False, True):
            code, lines, findings = run_hook(
                work, "report-test-edits", ["--base", "no-such-ref"],
                pre_commit=pre_commit)
            if code != 1 or len(findings) != 1:
                failures.append("  report-test-edits, an unresolved base%s: "
                                "exited %d, printed %s"
                                % (" under pre-commit" if pre_commit else "",
                                   code, lines))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return failures


def off_limits_cases():
    """report-off-limits-paths on a branch touching a declared path."""
    failures = []
    work = planted_repo({"README.md": "x\n"})
    try:
        git(work, "branch", "base")
        os.makedirs(os.path.join(work, ".github", "workflows"))
        with open(os.path.join(work, ".github", "workflows", "ci.yml"),
                  "w") as handle:
            handle.write("on: push\n")
        with open(os.path.join(work, "README.md"), "w") as handle:
            handle.write("y\n")
        git(work, "add", "-A")
        git(work, "commit", "-q", "-m", "touch")
        args = ["--base", "base", "--path", ".github/workflows/"]
        code, lines, findings = run_hook(work, "report-off-limits-paths", args)
        if code != 0 or len(findings) != 1 or "files changed: 2" not in lines:
            failures.append("  report-off-limits-paths, a touched workflow: "
                            "exited %d, printed %s" % (code, lines))
        code, lines, findings = run_hook(
            work, "report-off-limits-paths", ["--base", "base", "--path",
                                              "migrations/"])
        if code != 0 or findings:
            failures.append("  report-off-limits-paths, no declared path "
                            "touched: exited %d, printed %s" % (code, lines))
        code, lines, _ = run_hook(work, "report-off-limits-paths",
                                  ["--base", "no-such-ref", "--path", "x/"])
        if code != 1:
            failures.append("  report-off-limits-paths, an unresolved base: "
                            "exited %d, owed 1" % code)
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

    # A top-level module is a hook and nothing else; shared code lives in
    # support/, so a helper cannot pass for a misnamed hook.
    package = os.path.join(HOOKS_DIR, "solid_ai_checks")
    modules = {name[:-3] for name in os.listdir(package)
               if name.endswith(".py") and not name.startswith("__")}
    dispatched = {m.__name__.rsplit(".", 1)[1] for m in HOOKS.values()}
    for module in sorted(modules ^ dispatched):
        failures.append("  solid_ai_checks/%s.py: a top-level module that is "
                        "not a hook, or a hook with no module; shared code "
                        "goes in support/" % module)
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
    failures += off_limits_cases()
    return seen.failures() + failures, seen.notes()
