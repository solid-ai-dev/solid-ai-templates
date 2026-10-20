"""Report the changes under review that edit an existing test.

Adding a test strengthens the standard; editing or deleting one may weaken
it, which takes a person. The verdict is that person's, so this is a
reading.
"""

import argparse
import subprocess


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True,
                          text=True, check=True).stdout


def main(argv, report):
    parser = argparse.ArgumentParser(prog="report-test-edits")
    parser.add_argument("--base", default="origin/main",
                        help="the ref the change is compared against")
    parser.add_argument("--tests", default="tests",
                        help="the project's test root")
    args = parser.parse_args(argv)

    # A base that does not resolve, unfetched or mistyped, is a missing
    # baseline. Reading it as "no change under review" would pass a run
    # that compared nothing, so it is a failure.
    try:
        head, base = git("rev-parse", "HEAD").strip(), \
            git("rev-parse", "--verify", args.base).strip()
    except (OSError, subprocess.CalledProcessError):
        report.finding(args.base, 0, "BASE",
                       "cannot resolve HEAD and the base; fetch the base or "
                       "pass --base")
        return report.finish(True)
    if head == base:
        if git("status", "--porcelain").strip():
            report.note("HEAD is at %s and the work is uncommitted; commit it "
                        "and run again" % args.base)
            return report.finish(False)
        return report.not_applicable(
            "HEAD is at %s and the tree is clean; no change is under review"
            % args.base)

    span = "%s...HEAD" % args.base
    scope = "%s/" % args.tests.rstrip("/")
    changed = [l for l in git("diff", "--name-status", span).splitlines() if l]
    tests = [l for l in git("diff", "--name-status", span, "--", scope)
             .splitlines() if l]
    loosened = [l for l in tests if not l.startswith("A")]
    added = removed = 0
    for row in git("diff", "--numstat", span, "--", scope).splitlines():
        cells = row.split("\t")
        if len(cells) >= 2 and cells[0].isdigit() and cells[1].isdigit():
            added, removed = added + int(cells[0]), removed + int(cells[1])

    report.count("files changed in range", changed)
    report.count("test-file changes inspected", tests)
    report.count("changes that are not pure additions", loosened)
    report.count("test-root lines added", added)
    report.count("test-root lines removed", removed)
    for row in loosened:
        status, path = row.split("\t", 1)
        report.finding(path.split("\t")[-1], 0, "EDITED",
                       "test file changed with status %s" % status)
    return report.finish(False)
