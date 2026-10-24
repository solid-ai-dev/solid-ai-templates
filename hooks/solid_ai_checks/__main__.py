"""Run one hook: `python -m solid_ai_checks <hook-id> [--pre-commit] [args]`.

`--pre-commit` is set by the hook entries in `.pre-commit-hooks.yaml`. It
maps "does not apply" to a printed line and exit 0, because pre-commit
fails a hook on any nonzero exit. A git failure inside a work tree fails
the hook in either mode.
"""

import sys

from . import (check_ascii_identifiers, check_comment_layout,
               check_heading_numbers, compile_embedded_checks,
               find_bare_suppressions, find_import_bans,
               find_line_continuations, find_unfenced_checks,
               find_unreferenced_scripts, report_off_limits_paths,
               report_test_edits)
from .support.files import GitFailed, NotARepository
from .support.report import Report

# The hook IDs are frozen once shipped, like a section ID.
HOOKS = {
    "find-unfenced-checks": find_unfenced_checks,
    "compile-embedded-checks": compile_embedded_checks,
    "find-line-continuations": find_line_continuations,
    "find-bare-suppressions": find_bare_suppressions,
    "report-test-edits": report_test_edits,
    "check-ascii-identifiers": check_ascii_identifiers,
    "check-comment-layout": check_comment_layout,
    "find-import-bans": find_import_bans,
    "find-unreferenced-scripts": find_unreferenced_scripts,
    "check-heading-numbers": check_heading_numbers,
    "report-off-limits-paths": report_off_limits_paths,
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in HOOKS:
        print("usage: python -m solid_ai_checks <hook-id> [args]")
        print("hooks: %s" % ", ".join(sorted(HOOKS)))
        return 1
    hook = HOOKS[argv.pop(0)]
    pre_commit = "--pre-commit" in argv
    argv = [a for a in argv if a != "--pre-commit"]
    report = Report(pre_commit=pre_commit)
    try:
        return hook.main(argv, report)
    except NotARepository as error:
        return report.not_applicable(str(error))

    # The scan read nothing, so no count it would print can be trusted;
    # passing it would report a clean tree that was never read.
    except GitFailed as error:
        report.finding(".", 0, "GIT", str(error))
        return report.finish(True)


if __name__ == "__main__":
    sys.exit(main())
