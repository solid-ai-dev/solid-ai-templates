"""The change under review: the commits between a base and HEAD."""

import subprocess


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True,
                          text=True, check=True).stdout


def open_change(report, base):
    """The range under review, or the exit status that ends the run.

    Returns (span, None) when a change is open, or (None, status) when the
    run has already been answered: a base that does not resolve fails, a
    base at HEAD with uncommitted work asks for a commit, and a base at
    HEAD with a clean tree does not apply.
    """

    # A base that does not resolve, unfetched or mistyped, is a missing
    # baseline. Reading it as "no change under review" would pass a run
    # that compared nothing, so it is a failure.
    try:
        head = git("rev-parse", "HEAD").strip()
        resolved = git("rev-parse", "--verify", base).strip()
    except (OSError, subprocess.CalledProcessError):
        report.finding(base, 0, "BASE",
                       "cannot resolve HEAD and the base; fetch the base or "
                       "pass --base")
        return None, report.finish(True)
    if head == resolved:
        if git("status", "--porcelain").strip():
            report.note("HEAD is at %s and the work is uncommitted; commit it "
                        "and run again" % base)
            return None, report.finish(False)
        return None, report.not_applicable(
            "HEAD is at %s and the tree is clean; no change is under review"
            % base)
    return "%s...HEAD" % base, None
