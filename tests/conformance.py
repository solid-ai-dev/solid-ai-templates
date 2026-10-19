"""Dispositions for the checks the templates embed.

This repository is a consumer of its own base tier, so the checks the
templates prescribe apply here. Every runnable fenced block under
`templates/` MUST appear below exactly once. `run_conformance.py` fails on
a block with no entry, which is what stops a check added to a template from
arriving unexamined.

A block is located by a string only its body contains, never by position:
`core/git.md` alone holds ten of them, and selecting by index has
already found the wrong one.
"""

# Disposition values.
RUN = "run"
SKIP = "skip"

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
MANUAL = "manual"
READ = "read"

CHECKS = [

    # -- core/docs.md ------------------------------------------------

    # The efficacy benchmark's arm files are a generator's verbatim output,
    # which its design forbids editing; `short`'s is held to its own budget
    # and the others to none. They are source material the benchmark
    # measures, not documentation, so both checks leave them out.
    {"file": "core/docs.md", "find": "width, source = None, None",
     "title": "Documentation line width matches the declared one",
     "do": RUN, "expect": ["nonzero"],
     "substitute": {'["git", "ls-files", "*.md"]':
                    '["git", "ls-files", "*.md", '
                    '":(exclude)tests/efficacy/arms/"]'}},

    {"file": "core/docs.md", "find": "ungated figures",
     "title": "A documentation figure comes from a generator",
     "do": RUN, "expect": ["nonzero", "zero"],
     "substitute": {'SOURCES = ("templates/", "generated/", "examples/")':
                    'SOURCES = ("templates/", "generated/", "examples/", '
                    '"tests/efficacy/arms/")'}},

    # -- core/agents.md ----------------------------------------------

    {"file": "core/agents.md", "find": "scope silently lost",
     "title": "A consumer's chain list matches what its pin resolves",
     "do": SKIP,
     "reason": "Applies to a hybrid consumer that vendors this repository "
               "and lists its chain in its context file. This repository "
               "vendors nothing, and its CLAUDE.md is inline, so it holds "
               "no chain list to compare."},

    # -- core/git.md -------------------------------------------------

    {"file": "core/git.md", "find": "<regenerate-command>",
     "title": "Regenerated artifact matches its sources", "do": SKIP,
     "reason": "The regeneration command is a placeholder the consuming "
               "project fills in. This repository's equivalent is "
               "`py tools/sync.py`, already gated in CI."},

    {"file": "core/git.md", "find": "mask() {",
     "title": "Volatile parts of a binary artifact are masked before diffing",
     "do": SKIP,
     "reason": "Needs the paths of two generated bundles to compare. This "
               "repository commits no binary artifact."},

    {"file": "core/git.md", "find": "checks not passing",
     "title": "A pull request with no registered check has not passed CI",
     "do": SKIP,
     "reason": "Takes the pull request about to merge as `<N>`. Run per "
               "merge, before `gh pr merge`, not against a tree."},

    {"file": "core/git.md", "find": "PATHS = [\"<file>\"]",
     "title": "Numbered headings stay consistent across concurrent edits",
     "do": SKIP,
     "reason": "PATHS is a placeholder naming the documents two open "
               "branches both edit; it is set per release, not per repo."},

    {"file": "core/git.md", "find": "BASE = \"origin/main\"",
     "title": "A diff touching an off-limits path says so", "do": RUN,
     "expect": MANUAL,
     "reason": "The finding is whether the change SAYS SO about the path it "
               "touches, which is prose in a pull request body and not a "
               "count."},

    # -- core/quality.md ------------------------------------------

    {"file": "core/quality.md", "find": "FORBIDDEN = ()",
     "title": "A directional layering ban names its check", "do": SKIP,
     "reason": "FORBIDDEN is empty by design -- this repository's own "
               "Python (tools/, tests/) is a flat test/tooling layer "
               "with no domain/adapter split to bound. Re-examine if "
               "one is ever adopted."},

    {"file": "core/quality.md", "find": "def unwrap(cls, name)",
     "title": "A frozen override checker is backed by a hierarchy "
              "contract test", "do": SKIP,
     "reason": "BASE and HIERARCHY are empty by design -- this "
               "repository's own Python (tools/, tests/) declares one "
               "plain class (run_smoke.py's Inspected) with no "
               "subtype and no overridable operation. Applies to a "
               "consuming project's own abstract hierarchy."},

    {"file": "core/quality.md", "find": "documents naming ${module}",
     "title": "A document naming a check is re-read when its exemptions change",
     "do": SKIP,
     "reason": "Takes the check whose exemptions are changing as an "
               "argument. It is run per change, at the moment an "
               "exemption is added or removed, not as a property of the "
               "tree."},

    {"file": "core/quality.md", "find": "Identifiers only",
     "title": "Identifiers stay ASCII", "do": RUN,
     "expect": ["nonzero", "zero"]},

    {"file": "core/quality.md", "find": "aside to the right of code",
     "title": "Comment layout", "do": RUN, "expect": ["nonzero"]},

    {"file": "core/quality.md", "find": "SCRIPTS = pathlib.Path",
     "title": "The scripts directory carries the rules it owes", "do": SKIP,
     "reason": "This repository has no `scripts/` directory. Its permanent "
               "tooling lives in `tools/`, which the rule's own text scopes "
               "out. Re-examine if `scripts/` is ever added."},

    {"file": "core/quality.md",
     "find": "ya?ml|json|txt|toml|cfg|ini|sh|sql|css|js|ts",
     "title": "No committed text file carries CRLF", "do": RUN,
     "expect": ["nonzero", "zero"]},

    {"file": "core/quality.md", "find": "eol() { git ls-files --eol",
     "title": "The checkout carries the line ending the index does",
     "do": RUN, "expect": ["nonzero", "zero"]},

    # -- core/review.md ----------------------------------------------

    {"file": "core/review.md", "find": "open pull requests inspected",
     "title": "An issue is not already in flight before work starts",
     "do": SKIP,
     "reason": "The jq filter carries `#<N>` for the issue being checked. "
               "Run per issue when picking up work, not against a tree."},

    {"file": "core/review.md", "find": "pull requests linked to it",
     "title": "A sibling's shipped route, not the one it proposed",
     "do": SKIP,
     "reason": "Takes the sibling issue number as a placeholder. Run per "
               "issue when picking one up that defers to another, not "
               "against a tree."},

    {"file": "core/review.md", "find": "--since=<filing date>",
     "title": "A filed issue's claim is re-measured against the tree",
     "do": SKIP,
     "reason": "Takes the issue's filing date as an argument; run per issue "
               "during a groom, which the PLAYBOOK covers."},

    # -- core/testing.md ---------------------------------------------

    {"file": "core/testing.md", "find": "module-under-change",
     "title": "A remedy naming another check is re-read before narrowing it",
     "do": SKIP,
     "reason": "Takes the module whose scope is narrowing as an argument. "
               "It is run per change, not as a property of the tree."},

    {"file": "core/testing.md", "find": "guard-field-name",
     "title": "A guard field has a consumer, not only an assignment",
     "do": SKIP,
     "reason": "Takes the module under review and the guard field as "
               "arguments. It is run when one inert primitive is found, to "
               "sweep for its siblings, not as a property of the tree."},

    {"file": "core/testing.md", "find": "class ServerFixture",
     "title": "Fixture shape for a threaded server", "do": SKIP,
     "reason": "An illustration of the pattern, not a check. It has no pass "
               "condition and names a project's own server class."},

    {"file": "core/testing.md", "find": "type[(]self[)]",
     "title": "A class attribute is not mutated through the instance",
     "do": RUN, "expect": ["nonzero"], "grep": True},

    {"file": "core/testing.md", "find": "SERVER_THREAD_NAME",
     "title": "A test names its server thread", "do": SKIP,
     "reason": "An illustration of the naming pattern, not a check."},

    {"file": "core/testing.md", "find": "ssl.TLSVersion.TLSv1_2",
     "title": "A TLS floor is asserted, not assumed", "do": SKIP,
     "reason": "An illustration: an assertion a consuming project's own "
               "suite makes about its own context object."},

    {"file": "core/testing.md", "find": "pkg.__all__",
     "title": "Everything in __all__ is importable", "do": SKIP,
     "reason": "This repository ships no importable package. It applies to "
               "a library stack, where `stack/python-lib.md` carries it."},

    {"file": "core/testing.md", "find": "def fingerprint(path)",
     "title": "A mechanical move leaves the fingerprint unchanged",
     "do": SKIP,
     "reason": "Compares two revisions of a module named as arguments; run "
               "during a module split, not against a tree."},

    # -- security/devsecops.md ---------------------------------------

    {"file": "security/devsecops.md", "find": "sbom.json",
     "title": "The SBOM lists the components the build produced",
     "do": SKIP,
     "reason": "Reads `sbom.json`, produced by a build this repository does "
               "not have -- it ships Markdown and has no dependency graph "
               "to describe."},

    # -- core/quality-gates.md -----------------------------------

    {"file": "core/quality-gates.md",
     "find": "family: $FAMILY",
     "title": "Sizing one frozen rule family", "do": SKIP,
     "reason": "Names a rule family and a source root as placeholders, and "
               "runs `ruff` against a project that has adopted a freeze. "
               "This repository ships Markdown, has no `pyproject.toml`, no "
               "linter freeze and no `src/`, so there is no family to size."},

    {"file": "core/quality-gates.md", "find": "SUPPRESSIONS = (",
     "title": "A suppression names the rule it suppresses", "do": RUN,
     "expect": ["nonzero", "any", "zero"]},

    {"file": "core/quality-gates.md",
     "find": "'tests/*'", "title": "A change to an existing test is visible",
     "do": RUN, "expect": MANUAL,
     "reason": "Governance rather than a pass/fail metric: it decides "
               "review eligibility, not whether the build is green. Every "
               "template change owes a disposition in this file, which is "
               "itself a test edit, so scoring it would fail each "
               "conforming change on arrival."},

    {"file": "core/quality-gates.md",
     "find": "A shipped check is a heredoc inside a fenced block",
     "title": "A shipped rule states its check", "do": RUN,
     "expect": ["nonzero", "nonzero", "zero"]},

    {"file": "core/quality-gates.md", "find": "CHECK_LANGUAGES = (",
     "title": "A shipped check is safe to run where it is documented",
     "do": RUN, "expect": ["nonzero", "nonzero", READ],
     "reading": "The continuation count and the lines under it. A non-zero "
                "count is not a failure -- it is the set to read against "
                "what was written, because the check cannot tell a "
                "continuation that is safe where it sits from one a reader "
                "would lose. The two counts above it are decided: its pass "
                "condition says zero on either is a failure, the first "
                "meaning the fence pattern drifted and the second the "
                "language filter."},

    {"file": "core/quality-gates.md",
     "find": "checks stated outside a fence",
     "title": "Every stated check is in a form a tool can extract",
     "do": RUN, "expect": ["nonzero", "zero"]},

]


# A fork's dispositions cover the blocks only a fork's templates carry --
# its stacks, platforms, workflow and process sections. They live in
# fork_dispositions.py, which this registry takes in when the file exists,
# so a tree without those templates carries no entry for a block it lacks.
try:
    from fork_dispositions import CHECKS as FORK_CHECKS
except ModuleNotFoundError as exc:
    if exc.name != "fork_dispositions":
        raise
    FORK_CHECKS = []

CHECKS = CHECKS + FORK_CHECKS
