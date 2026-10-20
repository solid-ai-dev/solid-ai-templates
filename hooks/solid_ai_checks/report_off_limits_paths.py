"""Report the committed changes that touch a path declared off-limits.

A hit is an escalation trigger, not a failure: the check reads path names
and cannot tell an executable change from a prose one, so the summary and,
where owed, the proposal are a person's to write.
"""

import argparse

from .support.files import path_prefix
from .support.history import git, open_change


def touches(path, prefix):
    """Whether a path git printed falls under a normalised prefix."""
    return path.startswith(prefix) or ("/" + prefix) in path


def main(argv, report):
    parser = argparse.ArgumentParser(prog="report-off-limits-paths")
    parser.add_argument("--base", default="origin/main",
                        help="the ref the change is compared against")
    parser.add_argument("--path", action="append", default=[],
                        help="an off-limits path prefix; repeatable")
    args = parser.parse_args(argv)

    # git prints `.github/workflows/ci.yml`, so a prefix spelled
    # `./.github/workflows/` or with backslashes must be respelled before
    # it can match; left raw, the protected change drops out of the report.
    prefixes = report.count("off-limits paths declared",
                            [path_prefix(p) for p in args.path if p.strip()])
    if not prefixes:
        return report.not_applicable("no --path declared off-limits")

    span, status = open_change(report, args.base)
    if span is None:
        return status

    changed = [p for p in git("diff", "--name-only", span).splitlines() if p]
    report.count("files changed", changed)
    for path in changed:
        for prefix in prefixes:
            if touches(path, prefix):
                report.finding(path, 0, "OFF-LIMITS", "matches %s" % prefix)
    report.count("off-limits files touched", report.findings)

    # No file changed on an open branch means the range reached nothing.
    return report.finish(not changed)
