"""Report the changes under review that edit an existing test.

Adding a test strengthens the standard; editing or deleting one may weaken
it, which takes a person. The verdict is that person's, so this is a
reading.
"""

import argparse

from .support.history import git, open_change


def main(argv, report):
    parser = argparse.ArgumentParser(prog="report-test-edits")
    parser.add_argument("--base", default="origin/main",
                        help="the ref the change is compared against")
    parser.add_argument("--tests", default="tests",
                        help="the project's test root")
    args = parser.parse_args(argv)

    span, status = open_change(report, args.base)
    if span is None:
        return status

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
