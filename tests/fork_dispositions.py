"""Dispositions for the checks only a fork's templates embed.

`conformance.py` takes these in when this file exists. They cover the
blocks in the stacks, platforms and workflow, and in the process sections
of `core/git.md` and `core/docs.md`: content that belongs to a fork rather
than to upstream, so the entries live beside it rather than in the
registry both share. The rules for an entry are `conformance.py`'s.
"""

from conformance import RUN, SKIP, MANUAL, READ

CHECKS = [

    # -- core/docs.md --------------------------------------------------

    {"file": "core/docs.md", "find": "community health files checked",
     "title": "Community health files resolve to one location each",
     "do": RUN, "expect": ["nonzero"]},

    {"file": "core/docs.md",
     "find": "the naming convention drifted",
     "title": "ADR frontmatter schema", "do": RUN, "expect": ["nonzero"]},

    {"file": "core/docs.md", "find": "bound by the layout, from",
     "title": "Decision records carry the layout's sections",
     "do": RUN, "expect": ["nonzero", "nonzero"]},

    {"file": "core/docs.md", "find": "over a bound and not frozen",
     "title": "Decision-record prose stays within the declared bounds",
     "do": RUN,
     "expect": ["line", "line", "nonzero", "nonzero", "zero", "zero",
                "zero", "zero"]},

    {"file": "core/docs.md", "find": "changelog entries measured",
     "title": "Changelog entries stay within the word bound",
     "do": RUN, "expect": ["nonzero", "nonzero", "any", "zero"]},

    {"file": "core/docs.md", "find": "entries, fenced = [], False",
     "title": "Development journal entry form", "do": RUN,
     "expect": ["nonzero"]},

    {"file": "core/docs.md", "find": "(?:R|TD)[0-9]{2}",
     "title": "Risk and technical-debt identifiers stay in their owning doc",
     "do": RUN, "expect": ["nonzero", "nonzero", "nonzero"]},

    {"file": "core/docs.md", "find": "git diff --word-diff=porcelain",
     "title": "A format-only ADR edit moved no claim", "do": SKIP,
     "reason": "Takes the format-only commit under review as its argument; "
               "`HEAD~1` is a placeholder. There is no standing corpus of "
               "format-only ADR edits to run it over."},

    # -- core/examples.md ----------------------------------------------

    {"file": "core/examples.md", "find": "example failed: $f",
     "title": "Every example runs against a consumer install", "do": SKIP,
     "reason": "Placeholder runner. This repository's `examples/` holds generated "
               "context files rather than executable programs, so there is nothing "
               "to execute."},

    # -- core/git.md ---------------------------------------------------

    {"file": "core/git.md", "find": "git diff --stat :3:<path>",
     "title": "A conflict resolution keeps both sides' content", "do": SKIP,
     "reason": "Runs only during an unresolved merge conflict, against the "
               "conflicting path."},

    {"file": "core/git.md",
     "find": "settings leaving no safe deletion path",
     "title": "A merged head branch has a safe deletion path", "do": RUN,
     "expect": ["nonzero", "zero"]},

    {"file": "core/git.md", "find": "MILESTONE",
     "title": "Every issue closed since the previous tag carries the "
              "milestone", "do": RUN, "expect": MANUAL,
     "reason": "Parameterised by MILESTONE, which is unset here, so the "
               "check reports that the release is not scoped to a "
               "milestone and does not apply."},

    {"file": "core/git.md", "find": "<release-workflow>.yml",
     "title": "The release pipeline has executed before", "do": RUN,
     "expect": ["nonzero"],
     "substitute": {"<release-workflow>.yml": "release-gates.yml"}},

    {"file": "core/git.md",
     "find": "closing issues the subject does not name",
     "title": "A single-commit branch names its issue in the subject",
     "do": RUN, "expect": ["nonzero", "nonzero", "nonzero", "zero"]},

    {"file": "core/git.md",
     "find": "named by a merged commit and still open",
     "title": "No issue whose work already merged is still open",
     "do": RUN,
     "expect": ["line", "nonzero", "nonzero", "nonzero", "zero"]},

    {"file": "core/git.md", "find": "ready but unmerged",
     "title": "Release ordering against other ready pull requests",
     "do": RUN, "expect": MANUAL,
     "reason": "Each pull request it lists as ready is a decision about "
               "which side of the tag the work lands on. The check states "
               "that is not a warning it can score."},

    # DOCS is the project judgement the check names: the paths a consumer of
    # the release reads. Here that is the templates themselves, so an
    # identifier a template documents is documented in what ships. The
    # v2.90.0 cut named `uv.lock`, which only `stack/python-lib.md` carries,
    # and the default set read it as undocumented. `generated/` stays out as
    # a derivation of `templates/`; `tools/` and `tests/` stay out because a
    # set covering the whole tree passes whatever the code mentions, which
    # the rule calls the defect itself.
    {"file": "core/git.md", "find": "documentation files in the tree",
     "title": "The tree being tagged documents what the release claims",
     "do": RUN,
     "expect": ["nonzero", "nonzero", "line", "line", "any", "any", "zero"],
     "substitute": {'DOCS = ("README.md", "docs/")':
                    'DOCS = ("README.md", "docs/", "templates/")'}},

    {"file": "core/git.md",
     "find": "bullets ever under Unreleased in that range",
     "title": "A bullet deleted from Unreleased is reported",
     "do": RUN, "expect": ["nonzero", "nonzero", "zero"]},

    {"file": "core/git.md", "find": "entries in Unreleased",
     "title": "The Unreleased section accounts for what the release carries",
     "do": RUN, "expect": MANUAL,
     "reason": "Parameterised by RELEASE, which is unset here, so the check "
               "reports that no release is in preparation and does not "
               "apply. With it set, the two counts are deliberately not "
               "required to match and the operator reconciles them."},

    {"file": "core/git.md", "find": "audit records found",
     "title": "The newest periodic-review record is inside the interval",
     "do": RUN, "expect": ["nonzero", "nonzero"]},

    {"file": "core/git.md", "find": "<source-owner>/<source-repo>",
     "title": "A repository migration preserves both remotes", "do": SKIP,
     "reason": "Placeholder owner/repo pairs, run once during a migration."},

    # -- language/python.md --------------------------------------------

    {"file": "language/python.md", "find": "pkg/_accel.py",
     "title": "An optional accelerator is isolated to one module",
     "do": SKIP,
     "reason": "An illustration of the module layout, not a check."},

    {"file": "language/python.md", "find": "_LOG.addHandler",
     "title": "A library core attaches a null handler",
     "do": SKIP,
     "reason": "An illustration of the module layout, not a check."},

    {"file": "language/python.md", "find": "the library attaches no handler",
     "title": "A plain import leaves the library's logger silent",
     "do": SKIP,
     "reason": "Imports a package named `pkg`. This repository ships no "
               "importable package."},

    {"file": "language/python.md",
     "find": "raises_nothing_outside_the_contract",
     "title": "The package raises nothing outside its error contract",
     "do": SKIP,
     "reason": "Imports a package named `pkg` and walks its raises. This "
               "repository ships no importable package; its own Python "
               "(tools/, tests/) raises SystemExit to carry a verdict and "
               "declares no error hierarchy, because nothing calls it as "
               "a library."},

    # -- workflow/scope.md ---------------------------------------------

    {"file": "workflow/scope.md", "find": "platform/[a-z-]+[.]md",
     "title": "The context file names exactly one platform", "do": SKIP,
     "reason": "Reads a generated project's `CLAUDE.md` for its platform "
               "axis. This repository's `CLAUDE.md` is authored, not "
               "generated, and declares no platform template."},

    # -- workflow/two-pass-review.md -----------------------------------

    {"file": "workflow/two-pass-review.md", "find": "usage: scan <artifact>",
     "title": "First-pass mechanical scan of an artifact under review",
     "do": SKIP,
     "reason": "Takes the artifact to scan as an argument. It is a review "
               "aid run per artifact, not a property of the tree."},

    # -- platform/github.md --------------------------------------------

    {"file": "platform/github.md", "find": "gh run list --commit",
     "title": "A commit's checks have started, not merely not failed",
     "do": RUN, "expect": ["line", "nonzero", READ],
     "reading": "The rows under the count, one per run that did not "
                "succeed. Whether a run still going is acceptable depends "
                "on what is being decided, so the rows go to whoever the "
                "count summons. The count itself is decided: its pass "
                "condition says a zero must be resolved either way, since "
                "the check cannot tell a malformed query from a workflow "
                "that never fired."},

    {"file": "platform/github.md", "find": "code-scanning/analyses",
     "title": "Code scanning is entitled before the workflow is committed",
     "do": SKIP,
     "reason": "Placeholder owner/repo, and it answers a question asked "
               "once when adding the workflow."},

    {"file": "platform/github.md", "find": "state,headRefOid",
     "title": "A branch is deleted only against the merged pull request",
     "do": SKIP, "reason": "Takes a pull request number as a placeholder."},

    {"file": "platform/github.md", "find": "refs/pull/<N>/head",
     "title": "A rewritten head is inspected rather than assumed",
     "do": SKIP, "reason": "Takes a pull request number as a placeholder."},

    {"file": "platform/github.md", "find": "TYPES = re.compile",
     "title": "Every open issue carries one type and one priority label",
     "do": RUN, "expect": ["nonzero"]},

    # -- stack/c-embedded.md -------------------------------------------

    {"file": "stack/c-embedded.md", "find": "Configure (cross-compile",
     "title": "Build commands for the embedded stack", "do": SKIP,
     "reason": "A stack's Commands section, not a check."},

    # -- stack/go-lib.md -----------------------------------------------

    {"file": "stack/go-lib.md", "find": "for program in examples",
     "title": "Every example program builds and runs", "do": SKIP,
     "reason": "Runs `go vet`, `go test` and each program under "
               "`examples/`. This repository ships no Go module."},

    # -- stack/nodejs-lib.md -------------------------------------------

    {"file": "stack/nodejs-lib.md", "find": "npm --prefix",
     "title": "Every example runs against the packed tarball", "do": SKIP,
     "reason": "Packs an npm distribution and installs it into a clean "
               "directory. This repository publishes no npm package."},

    # -- stack/python-lib.md -------------------------------------------

    {"file": "stack/python-lib.md",
     "find": "git grep -n \"sys.path\" -- 'tests/*'",
     "title": "The suite imports the installation, not the working tree",
     "do": SKIP,
     "reason": "Scoped to a packaged library adopting `src/`. This "
               "repository ships no importable package, so its `tests/` "
               "has no installation to import instead."},

    {"file": "stack/python-lib.md", "find": "assert 'pkg.heavy' not in",
     "title": "A plain import loads neither the submodule nor its dependency",
     "do": SKIP,
     "reason": "`pkg` is a placeholder for the library under test. This "
               "repository ships no importable package."},

    {"file": "stack/python-lib.md", "find": "tar -tzf dist/",
     "title": "The sdist carries no vendored or submodule path", "do": SKIP,
     "reason": "Builds a source distribution and lists it. This repository "
               "builds no distribution."},

    {"file": "stack/python-lib.md", "find": "pathlib.Path(\"dist\").glob",
     "title": "The built wheel contains what it should", "do": SKIP,
     "reason": "Inspects a wheel under `dist/`. This repository builds no "
               "distribution."},

    {"file": "stack/python-lib.md", "find": "from importlib import import_module",
     "title": "A deferred import binds its name on first access", "do": SKIP,
     "reason": "This repository ships no importable package. The block is "
               "the module `__getattr__` pattern itself; the check that "
               "every advertised name resolves is `core/testing.md`'s "
               "and carries its own entry."},

    {"file": "stack/python-lib.md", "find": "_RENAMED = {\"OldName\"",
     "title": "A renamed public symbol resolves through the deferred map",
     "do": SKIP,
     "reason": "This repository ships no importable package."},

    {"file": "stack/python-lib.md", "find": "READER = {",
     "title": "Every committed lock has a Dependabot ecosystem that reads it",
     "do": SKIP,
     "reason": "Pairs a committed Python lock with its Dependabot reader. "
               "This repository ships Markdown, commits no Python lock, and "
               "enrols no Python ecosystem, so the check would fail on the "
               "zero-locks branch that is a finding for a library and a "
               "fact here."},
]
