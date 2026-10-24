"""Dispositions for the checks the templates embed.

This repository is a consumer of its own base tier, so the checks the
templates prescribe apply here. Every runnable fenced block under
`templates/` MUST appear below exactly once. `tests/conformance/run.py` fails on
a block with no entry, which is what stops a check added to a template from
arriving unexamined.

A block is located by a string only its body contains, never by position:
one template can hold several, and selecting by index has already found
the wrong one.
"""

import os
import sys

from conformance import MANUAL, READ, RUN, SKIP

# Pass predicates, named here and implemented in the runner.
#
#   [...]     a list naming what each line the check declares must hold:
#             "nonzero" for a count that proves the check reached its
#             inputs, "zero" for a violation count, "any" where zero is a
#             real answer, "line" for a declared line carrying no count.
#             Anything printed after the declared lines is a finding. A
#             check's own pass condition mixes the two directions, so a
#             single rule for the whole head does not fit
#   READ      ends the scored run inside such a list: the lines from
#             there on are a reading for whoever the verdict's failure
#             summons, carried into the report and never scored. An
#             entry using it MUST carry "reading", saying which lines
#             those are and who they are for; the runner refuses one
#             that does not. It is how a check reaches a verdict on the
#             counts its pass condition decides without failing on the
#             lines it leaves to a person
#   manual    the check runs and its output is reported, but no automatic
#             verdict is possible -- the operator reads it. A manual entry
#             MUST carry "reason", naming what about the check takes a
#             person; the runner refuses one that does not. A check whose
#             pass condition declares a threshold and counts against it
#             has a verdict available and is not manual
#
# "grep": True marks a check whose last command is a grep. grep exits 1
# when it matches nothing, which is the CLEAN result, so the exit code
# carries no verdict.
#
# "substitute": {placeholder: actual} resolves what a template leaves for
# its consumer to fill in, so a check written against a placeholder runs
# here instead of being skipped for naming one. A skip taken for that
# reason ages badly: it describes the repository on the day it was
# written, and nothing re-reads it when the repository grows the thing.
#
# "reason" is required on every SKIP and every MANUAL entry. A skip is a
# check that does not run, and the reason is the whole of what justifies
# it.
#
# SKIP_BUDGET is how many entries below are SKIP, and the runner fails when
# the count differs. A reason is prose nothing re-reads, so without a count
# the largest population in the registry could grow with every gate green;
# adding a skip, or retiring one, moves this number in the same diff. A
# fork's skips are counted against the SKIP_BUDGET fork_dispositions.py
# declares beside them.
SKIP_BUDGET = 5

# The interpreter running this suite, for a substitution that runs a tool.
# A bare `py` exists on Windows only and `python3` on Windows may be a stub,
# so the block runs the one already running.
PYTHON = '"%s"' % sys.executable.replace(os.sep, "/")

CHECKS = [

    # -- core/docs.md ------------------------------------------------

    # The linter is pinned to the version CI's setup step fetches, and read
    # from the npm cache, so a download cannot spend the runner's time limit.
    {"file": "core/docs.md", "find": "npx --yes markdownlint-cli2",
     "title": "Markdown holds to the declared line width",
     "do": RUN, "expect": ["nonzero", "nonzero", "nonzero"],
     "substitute": {"CONFIG=<markdownlint-config>":
                    "CONFIG=.github/linters/.markdownlint-cli2.jsonc",
                    "npx --yes markdownlint-cli2":
                    "npx --yes --prefer-offline markdownlint-cli2@0.23.3"}},

    # -- core/git.md -------------------------------------------------

    # This repository's regenerator is sync_docs.py, and what it writes depends
    # on the tree -- a fork's examples document among them -- so the diff
    # covers the whole tree. The run therefore reads committed work only,
    # which is how the suite is run anyway. sync_docs.py's own report is
    # silenced, so anything printed is a diff.
    {"file": "core/git.md", "find": "<regenerate-command>",
     "title": "Regenerated artifact matches its sources", "do": RUN,
     "expect": [],
     "substitute": {"<regenerate-command>":
                    PYTHON + " tools/sync_docs.py > /dev/null",
                    "<artifact-path>": "."}},

    {"file": "core/git.md", "find": "--ignore-cr-at-eol <file>",
     "title": "A line-ending-only regeneration diff is dropped before staging",
     "do": SKIP,
     "reason": "Classifies one file's pending change, between regenerating "
               "and staging it. It is run per change on the file just "
               "regenerated; a committed tree holds no pending change to "
               "classify."},

    {"file": "core/git.md", "find": "checks not passing",
     "title": "A pull request with no registered check has not passed CI",
     "do": SKIP,
     "reason": "Takes the pull request about to merge as `<N>`. Run per "
               "merge, before `gh pr merge`, not against a tree."},

    {"file": "core/git.md", "find": "check-heading-numbers",
     "title": "An ordered document keeps its numbering", "do": RUN,
     "args": ["--path", "AGENTS.md", "--path", "docs/playbook.md"],
     "expect": ["nonzero", "nonzero", "zero"]},

    {"file": "core/git.md", "find": "report-off-limits-paths",
     "title": "A diff touching an off-limits path says so", "do": RUN,
     "args": ["--path", ".github/workflows/", "--path", ".env",
              "--path", "migrations/"],
     "expect": MANUAL,
     "reason": "The finding is whether the change SAYS SO about the path it "
               "touches, which is prose in a pull request body and not a "
               "count."},

    # -- core/quality.md ------------------------------------------

    # The shipped hooks are this repository's one real boundary: they run
    # in consumers' CI and must not reach the maintainer-side tools or the
    # tests.
    {"file": "core/quality.md", "find": "find-import-bans",
     "title": "A directional layering ban names its check", "do": RUN,
     "args": ["--forbid", "hooks:tools", "--forbid", "hooks:tests"],
     "expect": ["nonzero", "nonzero", "zero"]},

    {"file": "core/quality.md", "find": "rg -n \"#<number>",
     "title": "Closing a cited item audits the citations to it",
     "do": SKIP,
     "reason": "Takes the item being closed or superseded as `<number>`. "
               "It is run per closure, in the change that closes the item, "
               "not as a property of the tree."},

    {"file": "core/quality.md", "find": "check-ascii-identifiers",
     "title": "Identifiers stay ASCII", "do": RUN,
     "expect": ["nonzero", "zero"]},

    {"file": "core/quality.md", "find": "check-comment-layout",
     "title": "Comment layout", "do": RUN, "expect": ["nonzero", "zero"]},

    # This repository has no scripts/; its maintained, unshipped tooling is
    # tools/, which is the directory the rule is about.
    {"file": "core/quality.md", "find": "find-unreferenced-scripts",
     "title": "The scripts directory carries the rules it owes", "do": RUN,
     "args": ["--dir", "tools"], "expect": ["nonzero", "nonzero", "zero"]},

    {"file": "core/quality.md", "find": "files not filed i/lf",
     "title": "No committed text file carries CRLF", "do": RUN,
     "expect": ["nonzero", "any", "any", "zero"]},

    {"file": "core/quality.md",
     "find": "checked out against a different convention",
     "title": "The checkout carries the line ending the index does",
     "do": RUN, "expect": ["nonzero", "zero"]},

    # -- core/testing.md ---------------------------------------------

    {"file": "core/testing.md", "find": "guard-field-name",
     "title": "A guard field has a consumer, not only an assignment",
     "do": SKIP,
     "reason": "Takes the module under review and the guard field as "
               "arguments. It is run when one inert primitive is found, to "
               "sweep for its siblings, not as a property of the tree."},

    # -- security/devsecops.md ---------------------------------------

    {"file": "security/devsecops.md", "find": "sbom.json",
     "title": "The SBOM lists the components the build produced",
     "do": SKIP,
     "reason": "Reads `sbom.json`, produced by a build this repository does "
               "not have -- it ships Markdown and has no dependency graph "
               "to describe."},

    # -- core/quality-gates.md -----------------------------------

    # The example's limit stands for the project's own. Here that is the
    # 88 .editorconfig declares for Python, and the Python is all this
    # repository holds that carries no exempt line: its Markdown keeps
    # table rows over the width, which its linter configuration exempts.
    {"file": "core/quality-gates.md", "find": "length > 80 { print; bad = 1 }",
     "title": "An output constraint is paired with its check", "do": RUN,
     "expect": [],
     "substitute": {"80": "88", "FILE": "tools/*.py tests/*.py"}},

    # The hooks scan the tracked tree. The Markdown ones take --root, which
    # here is the templates: the docs quote checks in prose on purpose, as
    # history and as worked examples of the defects the hooks find.
    {"file": "core/quality-gates.md", "find": "find-bare-suppressions",
     "title": "A suppression names the rule it suppresses", "do": RUN,
     "expect": ["nonzero", "any", "zero"]},

    {"file": "core/quality-gates.md",
     "find": "report-test-edits", "title": "A change to an existing test is visible",
     "do": RUN, "expect": MANUAL,
     "reason": "Governance rather than a pass/fail metric: it decides "
               "review eligibility, not whether the build is green. Every "
               "template change owes a disposition in this file, which is "
               "itself a test edit, so scoring it would fail each "
               "conforming change on arrival."},

    {"file": "core/embedded-checks.md",
     "find": "find-unfenced-checks",
     "title": "Every stated check is in a form a tool can extract",
     "do": RUN, "args": ["--root", "templates"],
     "expect": ["nonzero", "nonzero", "zero"]},

    # -- core/embedded-checks.md ---------------------------------

    {"file": "core/embedded-checks.md",
     "find": "compile-embedded-checks",
     "title": "A shipped rule states its check", "do": RUN,
     "args": ["--root", "templates"],
     "expect": ["nonzero", "nonzero", "zero"]},

    {"file": "core/embedded-checks.md", "find": "find-line-continuations",
     "title": "A shipped check is safe to run where it is documented",
     "do": RUN, "args": ["--root", "templates"],
     "expect": ["nonzero", "nonzero", "nonzero", READ],
     "reading": "The continuation count and the lines under it. A non-zero "
                "count is not a failure -- it is the set to read against "
                "what was written, because the check cannot tell a "
                "continuation that is safe where it sits from one a reader "
                "would lose. The three counts above it are decided: zero "
                "files means the root named nothing, zero blocks that the "
                "fence pattern drifted, and zero check-language blocks that "
                "the language filter did."},

]


# A fork's dispositions cover the blocks only a fork's templates carry --
# its stacks, platforms, workflow and process sections. They live in
# fork_dispositions.py, which this registry takes in when the file exists,
# so a tree without those templates carries no entry for a block it lacks.
try:
    import fork_dispositions
except ModuleNotFoundError as exc:
    if exc.name != "fork_dispositions":
        raise
    fork_dispositions = None

# Each registry's entries beside the skip count it declares. A fork's file
# that declares none is reported with None, which the runner refuses.
SKIP_BUDGETS = [("tests/conformance/dispositions.py", CHECKS, SKIP_BUDGET)]
FORK_CHECKS = []
if fork_dispositions is not None:
    FORK_CHECKS = fork_dispositions.CHECKS
    SKIP_BUDGETS.append(("tests/fork_dispositions.py", FORK_CHECKS,
                         getattr(fork_dispositions, "SKIP_BUDGET", None)))

CHECKS = CHECKS + FORK_CHECKS
