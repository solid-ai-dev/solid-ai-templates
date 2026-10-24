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
TILDES = "~" * 3
LONG_FENCE = "`" * 4

# The parts of one package, for the import cases that resolve a name
# against it.
PACKAGE = {"pkg/__init__.py": "", "pkg/adapters.py": "x = 1\n",
           "pkg/other.py": "y = 1\n"}
LAYERS = ["--forbid", "pkg.domain:pkg.adapters"]

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

    # Each heredoc in a block is a check of its own, and a fence of tildes
    # or of more than three backticks is as much a fence as the usual one.
    ("compile-embedded-checks", "a second heredoc check that does not compile",
     {"rules.md": "%sbash\npy - <<'EOF'\nprint(1)\nEOF\npy - <<'EOF'\n"
                  "print(\nEOF\n%s\n" % (FENCE, FENCE)}, [], 1, 1),
    ("compile-embedded-checks", "two heredoc checks that compile",
     {"rules.md": "%sbash\npy - <<'EOF'\nprint(1)\nEOF\npy - <<'EOF'\n"
                  "print(2)\nEOF\n%s\n" % (FENCE, FENCE)}, [], 0, 0),
    ("compile-embedded-checks", "a check in a tilde fence that does not compile",
     {"rules.md": "%sbash\npy - <<'EOF'\nprint(\nEOF\n%s\n" % (TILDES, TILDES)},
     [], 1, 1),
    ("find-line-continuations", "a continued line in a check",
     {"rules.md": "%sbash\nls %s\n  -la\n%s\n" % (FENCE, chr(92), FENCE)},
     [], 0, 1),
    ("find-line-continuations", "a continued line in a tilde fence",
     {"rules.md": "%sbash\nls %s\n  -la\n%s\n" % (TILDES, chr(92), TILDES)},
     [], 0, 1),
    ("find-line-continuations", "a continued line in a four-backtick fence",
     {"rules.md": "%sbash\nls %s\n  -la\n%s\n"
                  % (LONG_FENCE, chr(92), LONG_FENCE)}, [], 0, 1),
    ("find-line-continuations", "no block in a check language",
     {"rules.md": "%syaml\nkey: value\n%s\n" % (FENCE, FENCE)}, [], 3, 0),
    ("find-bare-suppressions", "a suppression naming no rule",
     {"app.py": "import os  %s noqa\n" % HASH}, [], 1, 1),
    ("find-bare-suppressions", "a suppression naming its rule",
     {"app.py": "import os  %s noqa: F401\n" % HASH}, [], 0, 0),

    # ESLint reads its directives from block comments as well as line ones,
    # and a directive quoted in a string suppresses nothing.
    ("find-bare-suppressions", "a bare whole-file ESLint block comment",
     {"app.js": "/* eslint-disable */\nrun();\n"}, [], 1, 1),
    ("find-bare-suppressions", "a bare next-line ESLint block comment",
     {"app.js": "/* eslint-disable-next-line */\nrun();\n"}, [], 1, 1),
    ("find-bare-suppressions", "an ESLint block comment naming its rule",
     {"app.js": "/* eslint-disable no-console */\nrun();\n"}, [], 0, 0),

    # The slash family is read by line, so a quoted directive over-reports
    # rather than a real one hiding behind a regex or a template.
    ("find-bare-suppressions", "a suppression quoted in a JavaScript string",
     {"app.js": "const s = \"// eslint-disable-next-line\";\n"}, [], 1, 1),
    ("find-bare-suppressions", "a suppression quoted in a Python string",
     {"app.py": "value = '%s noqa'\n" % HASH}, [], 0, 0),
    ("find-bare-suppressions", "a bare suppression after a quote in a regex",
     {"app.js": "const r = /\"/; // eslint-disable-next-line\nrun();\n"},
     [], 1, 1),
    ("find-bare-suppressions", "a bare suppression after a postfix division",
     {"app.js": "a++ / b; // eslint-disable-next-line\nrun(a);\n"}, [], 1, 1),
    ("find-bare-suppressions", "a bare suppression after a keyword property",
     {"app.js": "obj.return / b; // eslint-disable-next-line\nrun();\n"},
     [], 1, 1),
    ("find-bare-suppressions", "a bare suppression after a regex in a condition",
     {"app.js": "if (ok) /\"/.test(v); // eslint-disable-next-line\nrun();\n"},
     [], 1, 1),
    ("find-bare-suppressions", "a bare suppression after a commented regex",
     {"app.js": "const r = /* p */ /\"/; // eslint-disable-next-line\n"},
     [], 1, 1),
    ("find-bare-suppressions", "a bare suppression after an object division",
     {"app.js": "const x = {} / 2; // eslint-disable-next-line\nrun();\n"},
     [], 1, 1),
    ("find-bare-suppressions", "a bare suppression after a commented property",
     {"app.js": "obj./* p */return / b; // eslint-disable-next-line\n"},
     [], 1, 1),
    ("find-bare-suppressions", "a bare suppression in a template expression",
     {"app.js": "const s = `${(() => { // eslint-disable-next-line\n"
                "  return 1;\n})()}`;\n"}, [], 1, 1),
    ("find-bare-suppressions", "a bare directive in a multi-line block comment",
     {"app.js": "/*\n * eslint-disable\n */\nrun();\n"}, [], 1, 1),

    # A line can close one block comment and open the next, so the scanner
    # follows every boundary on it, not only the first.
    ("find-bare-suppressions", "a bare directive in a block opened after one",
     {"app.js": "/* a */ /* b\neslint-disable-next-line\n*/\nrun();\n"},
     [], 1, 1),
    ("find-bare-suppressions", "a bare directive in a block reopened in one",
     {"app.js": "/* a\n*/ run(); /* b\neslint-disable\n*/\n"}, [], 1, 1),
    ("find-bare-suppressions", "a bare line comment after a block closes",
     {"app.js": "/* a\n*/ run(); // eslint-disable-line\n"}, [], 1, 1),

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
    ("check-comment-layout", "a comment opening a block that quotes a hash",
     {"app.py": "if value == \"%s\":\n    %s note\n    pass\n" % (HASH, HASH)},
     [], 0, 0),
    ("check-comment-layout", "a comment under code that quotes a hash",
     {"app.py": "x = \"%s\"\n%s note\ny = 2\n" % (HASH, HASH)}, [], 1, 1),
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

    # The banned module reached through its package, relative to the
    # importer, and from below a src directory.
    ("find-import-bans", "an adapter imported from its package",
     dict(PACKAGE, **{"pkg/domain.py": "from pkg import adapters\n"}),
     LAYERS, 1, 1),
    ("find-import-bans", "an adapter imported relatively",
     dict(PACKAGE, **{"pkg/domain.py": "from . import adapters\n"}),
     LAYERS, 1, 1),
    ("find-import-bans", "an adapter imported in a src layout",
     {"src/pkg/__init__.py": "", "src/pkg/adapters.py": "x = 1\n",
      "src/pkg/domain.py": "import pkg.adapters\n"}, LAYERS, 1, 1),
    ("find-import-bans", "a sibling imported from the same package",
     dict(PACKAGE, **{"pkg/domain.py": "from pkg import other\n"}),
     LAYERS, 0, 0),
    ("find-unreferenced-scripts", "a script nothing names",
     {"scripts/old.py": "x = 1\n", "README.md": "Nothing here.\n"},
     [], 1, 1),
    ("find-unreferenced-scripts", "a script the README names",
     {"scripts/old.py": "x = 1\n", "README.md": "Run old.py.\n"}, [], 0, 0),

    # A helper is kept by the script that imports it, but only when that
    # script is itself reached.
    ("find-unreferenced-scripts", "a helper the documented script imports",
     {"scripts/main.py": "import helper\n", "scripts/helper.py": "x = 1\n",
      "README.md": "Run scripts/main.py.\n"}, [], 0, 0),
    ("find-unreferenced-scripts", "a helper only an unnamed script imports",
     {"scripts/main.py": "import helper\n", "scripts/helper.py": "x = 1\n",
      "README.md": "Nothing here.\n"}, [], 1, 2),
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

    # A nested list and a second list each run from 1, and a fence holds an
    # example, not the document's numbering. A skip across a flush code
    # block and a repeat inside a nested list are still found.
    ("check-heading-numbers", "a nested list numbered from 1",
     {"spec.md": "## 1 Steps\n\n1. a\n   1. x\n   2. y\n2. b\n"},
     ["--path", "spec.md"], 0, 0),
    ("check-heading-numbers", "two lists under one heading, each from 1",
     {"spec.md": "## Steps\n\n1. a\n2. b\n\nThen:\n\n1. c\n2. d\n"},
     ["--path", "spec.md"], 0, 0),
    ("check-heading-numbers", "a numbered heading in a code fence",
     {"spec.md": "## 1 One\n\n%smarkdown\n## 9 Example\n%s\n\n## 2 Two\n"
                 % (FENCE, FENCE)}, ["--path", "spec.md"], 0, 0),
    ("check-heading-numbers", "a skip across a flush code block",
     {"spec.md": "## Steps\n\n1. a\n2. b\n\n%sbash\nls\n%s\n\n4. d\n"
                 % (FENCE, FENCE)}, ["--path", "spec.md"], 1, 1),
    ("check-heading-numbers", "a repeat inside a nested list",
     {"spec.md": "## Steps\n\n1. a\n   1. x\n   1. y\n2. b\n"},
     ["--path", "spec.md"], 1, 1),
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

        # The same directory spelled as a user might type it, which git
        # never prints.
        for spelling in ("./.github/workflows/",
                         ".github%sworkflows%s" % (chr(92), chr(92))):
            code, lines, findings = run_hook(
                work, "report-off-limits-paths",
                ["--base", "base", "--path", spelling])
            if code != 0 or len(findings) != 1:
                failures.append("  report-off-limits-paths, the path spelled "
                                "%r: exited %d, printed %s"
                                % (spelling, code, lines))
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

        # A rename out of the declared directory touches it as much as an
        # edit does, though git prints only the destination by name.
        git(work, "branch", "moved")
        os.makedirs(os.path.join(work, "retired"))
        git(work, "mv", ".github/workflows/ci.yml", "retired/ci.yml")
        git(work, "commit", "-q", "-m", "retire")
        code, lines, findings = run_hook(
            work, "report-off-limits-paths",
            ["--base", "moved", "--path", ".github/workflows/"])
        touched = [f.split(":")[0] for f in findings]
        if code != 0 or "files changed: 2" not in lines \
                or touched != [".github/workflows/ci.yml"]:
            failures.append("  report-off-limits-paths, a workflow renamed "
                            "out: exited %d, printed %s" % (code, lines))

        # git quotes a path holding a space or a non-ASCII letter unless
        # asked for raw output, and the quoted path matches no prefix.
        git(work, "branch", "spaced")
        name = os.path.join(work, ".github", "workflows",
                            "caf%s ci.yml" % chr(233))
        with open(name, "w", encoding="utf-8") as handle:
            handle.write("on: push\n")
        git(work, "add", "-A")
        git(work, "commit", "-q", "-m", "spaced")
        code, lines, _ = run_hook(
            work, "report-off-limits-paths",
            ["--base", "spaced", "--path", ".github/workflows/"])
        if code != 0 or "off-limits files touched: 1" not in lines:
            failures.append("  report-off-limits-paths, a workflow named with "
                            "a space and an accent: exited %d, printed %s"
                            % (code, lines))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return failures


def git_failure_cases():
    """A tree scan where git fails, and the same scan outside a repository.

    Outside a repository the hook does not apply. Inside one, a git that
    cannot list the tree read nothing, so the hook fails in either mode.
    """
    failures = []
    work = planted_repo({"app.py": "x = 1\n"})
    plain = tempfile.mkdtemp(prefix="sait-plain-")
    try:
        with open(os.path.join(work, ".git", "config"), "w") as handle:
            handle.write("[broken\n")
        for hook in ("find-bare-suppressions", "check-comment-layout"):
            for pre_commit in (False, True):
                code, lines, findings = run_hook(work, hook, [],
                                                 pre_commit=pre_commit)
                if code != 1 or len(findings) != 1:
                    failures.append("  %s, a malformed git config%s: exited "
                                    "%d, printed %s"
                                    % (hook, " under pre-commit"
                                       if pre_commit else "", code, lines))
            code, lines, _ = run_hook(plain, hook, [], pre_commit=True)
            if code != 0 or not any(l.startswith("not applicable:")
                                    for l in lines):
                failures.append("  %s under pre-commit, outside a "
                                "repository: exited %d, printed %s"
                                % (hook, code, lines))
            code, lines, _ = run_hook(plain, hook, [])
            if code != 3:
                failures.append("  %s, outside a repository: exited %d, "
                                "owed 3" % (hook, code))
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(plain, ignore_errors=True)
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
    failures += git_failure_cases()
    return seen.failures() + failures, seen.notes()
