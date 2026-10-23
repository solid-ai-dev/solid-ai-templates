"""Report the committed changes that touch a path declared off-limits.

A hit is an escalation trigger, not a failure: the check reads path names
and cannot tell an executable change from a prose one, so the summary and,
where owed, the proposal are a person's to write.
"""

import argparse

from .support.files import GitFailed, path_prefix, run_git
from .support.history import open_change


def touches(path, prefix):
    """Whether a path git printed falls under a normalised prefix."""
    return path.startswith(prefix) or ("/" + prefix) in path


def changed_paths(span):
    """Every path the range touches, in the order git lists them.

    A rename touches both of its paths: moving a protected file out of
    its directory changes that directory as much as editing it does. A
    copy leaves its source as it was, so only the destination counts.
    """

    # -z prints each path raw and NUL-ended. The default output quotes a
    # path holding a space or a non-ASCII byte, and the quoted spelling no
    # longer starts with the prefix it falls under.
    diff = run_git(["diff", "--name-status", "-z", span])
    if diff.returncode != 0:
        raise GitFailed("git diff exited %d: %s" % (
            diff.returncode, diff.stderr.decode("utf-8", "replace").strip()))
    fields = diff.stdout.decode("utf-8").split("\0")
    paths, i = [], 0
    while i < len(fields) and fields[i]:
        status = fields[i]
        if status[0] in "RC":
            old, new = fields[i + 1], fields[i + 2]
            paths += [old, new] if status[0] == "R" else [new]
            i += 3
        else:
            paths.append(fields[i + 1])
            i += 2
    return list(dict.fromkeys(paths))


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

    changed = report.count("files changed", changed_paths(span))
    for path in changed:
        for prefix in prefixes:
            if touches(path, prefix):
                report.finding(path, 0, "OFF-LIMITS", "matches %s" % prefix)
    report.count("off-limits files touched", report.findings)

    # No file changed on an open branch means the range reached nothing.
    return report.finish(not changed)
