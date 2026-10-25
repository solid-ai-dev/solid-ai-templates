"""The change under review: the commits between a base and HEAD."""

import subprocess


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True,
                          text=True, check=True).stdout


def open_change(report, base):
    """The range under review, or the exit status that ends the run.

    Returns (span, None) when a change is open, or (None, status) when the
    run has already been answered: a base that does not resolve fails, and
    a HEAD at or behind the base asks for a commit when work is
    uncommitted and otherwise does not apply.
    """

    # A base that does not resolve, unfetched or mistyped, is a missing
    # baseline. Reading it as "no change under review" would pass a run
    # that compared nothing, so it is a failure.
    try:
        git("rev-parse", "HEAD")
        git("rev-parse", "--verify", base)
    except (OSError, subprocess.CalledProcessError):
        report.finding(base, 0, "BASE",
                       "cannot resolve HEAD and the base; fetch the base or "
                       "pass --base")
        return None, report.finish(True)

    # A base that already holds HEAD leaves base...HEAD empty, so no change
    # is under review. That covers HEAD behind the base as well as at it:
    # a release tag's pipeline runs behind main once another change merges
    # first.
    held = subprocess.run(
        ["git", "merge-base", "--is-ancestor", "HEAD", base],
        capture_output=True).returncode == 0
    if held:
        if git("status", "--porcelain").strip():
            report.note("HEAD is at or behind %s and the work is uncommitted; "
                        "commit it and run again" % base)
            return None, report.finish(False)
        return None, report.not_applicable(
            "HEAD is at or behind %s and the tree is clean; no change is "
            "under review" % base)
    return "%s...HEAD" % base, None
