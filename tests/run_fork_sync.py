#!/usr/bin/env python3
"""
Fork-sync runner: a simulated fork merges an upstream change cleanly.

Implements:
  SAIT-INT-MNF-06-001A  — a fork that only appends merges upstream cleanly

Usage:
  py tests/run_fork_sync.py                   # upstream change: HEAD
  py tests/run_fork_sync.py --base=<ref>      # fork from merge-base(HEAD, ref)
"""

import datetime
import os
import shutil
import stat
import subprocess
import sys
import tempfile

from lib import ROOT, PASS, FAIL, ERR, write_report, print_verdict

# Same boundary settings as the other runners: UTF-8 out, and LF line
# endings, so a consumer reading this output on Windows sees no stray
# carriage returns.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", newline="\n")
    except (AttributeError, ValueError):
        pass

DEFAULT_BASE = "origin/main"

# A fork owns these and resolves them in its own favour on every merge, so a
# conflict in one is expected rather than a finding (ADR-049, rule 7).
FORK_OWNED = ("README.md", "CLAUDE.md", "CHANGELOG.md")

MANIFEST = "templates/manifest.yaml"
FIXTURE = "templates/fixture/stack.md"
FORK_STACK = "templates/stack/fork-sync.md"

# The fork's manifest append. `stacks:` is the manifest's last key, so a fork
# appends at the end of the file, where a fork's own entries land.
FORK_ENTRY = """
  - id: stack-fork-sync
    file: templates/stack/fork-sync.md
    label: Fork sync
    layer: fixture
    description: A fork's own stack, appended by the fork-sync simulation
    fixture: true
    depends_on: [base-security, base-quality-gates]
"""

FORK_NOTE = "Simulated fork: this line is the fork's own edit."


def git(cwd, *args, check=True):
    """Run git in cwd and return the completed process."""
    run = subprocess.run(["git", "-C", cwd] + list(args),
                         capture_output=True, text=True, encoding="utf-8")
    if check and run.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {run.stderr.strip()}")
    return run


def out(cwd, *args):
    return git(cwd, *args).stdout.strip()


def read(repo, rel):
    with open(os.path.join(repo, rel), encoding="utf-8", newline="") as f:
        return f.read()


def write(repo, rel, text):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path) or repo, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def insert_after_title(text, line):
    """Put line under a document's first line, where a fork brands it."""
    head, sep, rest = text.partition("\n")
    return f"{head}\n\n{line}\n{sep}{rest}"


def commit(repo, base, message, edit):
    """Commit edit(repo) on top of base, detached, and return the commit.

    The commit MUST change what it claims to: an edit that lands nothing
    leaves a scenario that tests nothing, and its clean merge would read as
    the merge holding.
    """
    git(repo, "checkout", "-q", "--detach", base)
    owed = edit(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    tip = out(repo, "rev-parse", "HEAD")
    changed = set(out(repo, "diff", "--name-only", base, tip).splitlines())
    if changed != set(owed):
        raise RuntimeError(f"{message}: changed {sorted(changed)}, "
                           f"owed {sorted(owed)}")
    return tip


# ---------------------------------------------------------------------------
# The edits each side makes
# ---------------------------------------------------------------------------

def fork_edits(repo):
    """What a fork does under ADR-049: append, and own its documents."""
    stack = read(repo, FIXTURE)
    stack = stack.replace("# Stack — Fixture", "# Stack — Fork sync")
    stack = stack.replace("[ID: fixture-", "[ID: fork-sync-")
    write(repo, FORK_STACK, stack)

    manifest = read(repo, MANIFEST)
    if not manifest.endswith("\n"):
        manifest += "\n"
    write(repo, MANIFEST, manifest + FORK_ENTRY)

    for rel in FORK_OWNED:
        write(repo, rel, insert_after_title(read(repo, rel), FORK_NOTE))
    return [FORK_STACK, MANIFEST, *FORK_OWNED]


def upstream_base_edit(repo):
    """A change to `base:`, for a run whose own upstream change is empty."""
    lines = read(repo, MANIFEST).split("\n")
    start = lines.index("base:")
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("    description: "):
            lines[i] += " (upstream edit)"
            break
    write(repo, MANIFEST, "\n".join(lines))
    return [MANIFEST]


def upstream_appends_a_stack(repo):
    """Planted: upstream appends where the fork appends, so the two collide."""
    manifest = read(repo, MANIFEST)
    if not manifest.endswith("\n"):
        manifest += "\n"
    write(repo, MANIFEST, manifest + FORK_ENTRY.replace(
        "stack-fork-sync", "stack-upstream-plant"))
    return [MANIFEST]


def upstream_edits_readme(repo):
    """Planted: upstream edits the README where the fork brands it."""
    text = read(repo, "README.md")
    write(repo, "README.md",
          insert_after_title(text, "Upstream edit under the title."))
    return ["README.md"]


# ---------------------------------------------------------------------------
# The merge
# ---------------------------------------------------------------------------

def merge(repo, fork, upstream):
    """Merge upstream into fork the way a fork syncs.

    Returns (merged, owned, unexpected): the merge commit, or None when a
    conflict outside the fork's own documents stops it, and the conflicted
    paths on each side of that line.
    """
    git(repo, "checkout", "-q", "--detach", fork)
    run = git(repo, "merge", "--no-edit", "-q", upstream, check=False)
    conflicted = out(repo, "diff", "--name-only", "--diff-filter=U").split()
    if run.returncode != 0 and not conflicted:
        raise RuntimeError(f"merge failed without conflicts: "
                           f"{(run.stdout + run.stderr).strip()}")

    owned = sorted(p for p in conflicted if p in FORK_OWNED)
    unexpected = sorted(p for p in conflicted if p not in FORK_OWNED)
    if unexpected:
        git(repo, "merge", "--abort")
        return None, owned, unexpected

    for path in owned:
        git(repo, "checkout", "--ours", "--", path)
        git(repo, "add", "--", path)
    if owned:
        git(repo, "commit", "-q", "--no-edit")
    return out(repo, "rev-parse", "HEAD"), owned, unexpected


def follow_renames(repo, base, upstream, fork, merged):
    """Point the fork's own files at the paths upstream renamed.

    A rename is the one breaking change a fork migrates mechanically, so the
    simulation does what the fork would and reports it. Anything a rename
    does not explain, a deleted file or a removed ID, still reaches smoke.
    """
    status = out(repo, "diff", "-M", "--name-status", "--diff-filter=R",
                 base, upstream).splitlines()
    renames = [tuple(line.split("\t")[1:3]) for line in status]
    own = out(repo, "diff", "--name-only", "--diff-filter=A", base,
              fork).splitlines()

    git(repo, "checkout", "-q", "--detach", merged)
    touched = []
    for rel in own:
        text = read(repo, rel)
        moved = text
        for old, new in renames:
            moved = moved.replace(old, new)
        if moved != text:
            touched.append(rel)
    if not touched:
        return merged, renames

    def edit(target):
        for rel in touched:
            text = read(target, rel)
            for old, new in renames:
                text = text.replace(old, new)
            write(target, rel, text)
        return touched

    return commit(repo, merged, "fork: follow upstream renames", edit), renames


def nested_smoke(repo, upstream):
    """Run the merged tree's own smoke suite, with SYS-20 against upstream."""
    env = dict(os.environ, SAIT_UPSTREAM_REF=upstream)
    run = subprocess.run([sys.executable, "tests/run_smoke.py"], cwd=repo,
                         env=env, capture_output=True, text=True,
                         encoding="utf-8")
    lines = run.stdout.splitlines()
    verdict = next((l for l in reversed(lines) if l.startswith("VERDICT:")),
                   None)
    failing = [l for l in lines if l.startswith(("  FAIL", "  ERR"))]
    return run.returncode, verdict, failing


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

def planted(repo, base, fork, rid, title, edit, owed_owned, owed_unexpected):
    """A planted upstream change whose conflicts are known in advance."""
    upstream = commit(repo, base, f"upstream: {title}", edit)
    merged, owned, unexpected = merge(repo, fork, upstream)
    notes = [f"  conflicts in fork-owned files: {owned or 'none'}",
             f"  conflicts elsewhere: {unexpected or 'none'}"]
    failures = []
    if owned != owed_owned or unexpected != owed_unexpected:
        failures.append(f"  owed fork-owned {owed_owned} and elsewhere "
                        f"{owed_unexpected}")
    if not owed_unexpected and merged is None:
        failures.append("  the merge did not complete")
    return {"id": rid, "title": title, "notes": notes, "failures": failures}


def real(repo, base, head, fork):
    """The change under test, merged into the fork, then smoke on the result."""
    notes = []
    upstream = head
    if not out(repo, "diff", "--name-only", base, head):
        upstream = commit(repo, base, "upstream: edit base:",
                          upstream_base_edit)
        notes.append("  HEAD changes nothing against the base, so the "
                     "upstream change is a planted `base:` edit")
    changed = out(repo, "diff", "--name-only", base, upstream).splitlines()
    notes.append(f"  upstream change: {len(changed)} file(s), "
                 f"{base[:7]}..{upstream[:7]}")

    title = "the upstream change merges into a fork that only appends"
    merged, owned, unexpected = merge(repo, fork, upstream)
    notes.append(f"  conflicts in fork-owned files, kept as the fork's: "
                 f"{owned or 'none'}")
    if merged is None:
        return {"id": "FS-03", "title": title, "notes": notes, "failures": [
            f"  conflicts outside the fork's own documents: {unexpected}"]}

    merged, renames = follow_renames(repo, base, upstream, fork, merged)
    notes.append(f"  upstream renames, applied to the fork's own files: "
                 f"{renames or 'none'}")

    if not os.path.exists(os.path.join(repo, FORK_STACK)):
        return {"id": "FS-03", "title": title, "notes": notes, "failures": [
            f"  the merged tree lost the fork's stack, {FORK_STACK}"]}

    code, verdict, failing = nested_smoke(repo, upstream)
    notes.append(f"  smoke in the merged tree: {verdict or 'no verdict line'}")
    failures = []
    if code != 0 or verdict is None:
        failures.append("  smoke fails in the merged tree")
        failures.extend(failing)
    return {"id": "FS-03", "title": title, "notes": notes,
            "failures": failures}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def base_commit(ref):
    """The commit the fork was made from, or exit naming what is missing.

    A baseline that cannot be derived is a refusal, never a pass: a run
    against nothing would report the clean merge of an empty change.
    """
    resolved = git(ROOT, "rev-parse", "--verify", "-q", f"{ref}^{{commit}}",
                   check=False)
    if resolved.returncode != 0:
        print(f"Base ref {ref!r} does not resolve. Fetch it, or name "
              f"another with --base=<ref>. Nothing has run.")
        sys.exit(1)
    found = git(ROOT, "merge-base", "HEAD", resolved.stdout.strip(),
                check=False)
    if found.returncode != 0 or not found.stdout.strip():
        print(f"HEAD shares no history with {ref!r}. Nothing has run.")
        sys.exit(1)
    return found.stdout.strip()


def remove(path):
    # Git marks its object files read-only, which Windows refuses to delete.
    def retry(func, target, _info):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(path, onerror=retry)


def render(r):
    lines = [f"### {r['status']}  {r['id']} — {r['title']}", ""]
    if r.get("notes"):
        lines.extend(["**Inspected**:", "", "```", *r["notes"], "```", ""])
    if r.get("failures"):
        lines.extend(["**Observed**:", "", "```", *r["failures"], "```", ""])
    if r.get("error"):
        lines.extend([f"**Error**: {r['error']}", ""])
    return lines


def main():
    started_at = datetime.datetime.now()
    ref = DEFAULT_BASE
    for arg in sys.argv[1:]:
        if arg.startswith("--base="):
            ref = arg.split("=", 1)[1]

    head = out(ROOT, "rev-parse", "HEAD")
    base = base_commit(ref)
    if out(ROOT, "status", "--porcelain"):
        print("The working tree is dirty; this run reads committed HEAD only.")
    print(f"Fork from {base[:7]} (merge-base of HEAD and {ref}); "
          f"upstream change {base[:7]}..{head[:7]}\n")

    repo = tempfile.mkdtemp(prefix="sait-fork-sync-")
    results = []
    try:
        # A shared clone borrows ROOT's objects, so HEAD resolves even when
        # it is CI's detached merge commit, which no branch names.
        git(ROOT, "clone", "-q", "--shared", "--no-checkout", ROOT, repo)
        for key, value in (("core.autocrlf", "false"),
                           ("user.name", "fork-sync"),
                           ("user.email", "fork-sync@localhost")):
            git(repo, "config", key, value)
        fork = commit(repo, base, "fork: append a stack, own the documents",
                      fork_edits)

        scenarios = [
            ("FS-01", lambda: planted(
                repo, base, fork, "FS-01",
                "planted: upstream appends where the fork appends, and the "
                "conflict is caught",
                upstream_appends_a_stack, [], [MANIFEST])),
            ("FS-02", lambda: planted(
                repo, base, fork, "FS-02",
                "planted: a conflict in a fork-owned file is kept as the "
                "fork's",
                upstream_edits_readme, ["README.md"], [])),
            ("FS-03", lambda: real(repo, base, head, fork)),
        ]
        for rid, scenario in scenarios:
            try:
                r = scenario()
                r["status"] = FAIL if r["failures"] else PASS
            except RuntimeError as e:
                r = {"id": rid, "title": "scenario raised", "status": ERR,
                     "notes": [], "failures": [], "error": str(e)}
            results.append(r)
            print(f"  {r['status']}  {r['id']}  {r['title']}")
            for line in r["notes"] + r["failures"]:
                print(line)
            if r.get("error"):
                print(f"  {r['error']}")
    finally:
        remove(repo)

    failed = sum(1 for r in results if r["status"] == FAIL)
    errors = sum(1 for r in results if r["status"] == ERR)
    write_report(results, started_at, "fork_sync",
                 {PASS: render, FAIL: render, ERR: render})
    ok = failed == 0 and errors == 0 and len(results) == 3
    print_verdict(ok, "%d scenarios, %d failed, %d errors"
                  % (len(results), failed, errors))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
