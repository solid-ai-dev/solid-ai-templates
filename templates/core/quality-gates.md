# Base — Quality Gates

[ID: base-quality-gates]
[DEPENDS ON: templates/core/quality.md, templates/core/git.md]
[DEPENDS ON: templates/core/testing.md, templates/core/config.md]

What to gate, how to build, adopt, read and change a gate. When gates run,
and at which thresholds, is the project's choice.

## Paired checks

[ID: quality-gates-pair-check]

A stated constraint without its check is decorative: a violating artifact
looks like a clean one.

- Name the agent-runnable check of an output constraint that is
  mechanically checkable: the command to run and the pass condition (MUST)
- State the check next to the rule, so the two travel together into every
  generated artifact
- Put the command in a fenced block; prose carries the pass condition
  beside it
- Write the command first; a sentence describing an action is not a check
- Keep a subjective constraint declarative, and never invent a brittle
  check for it
- Wire a check guarding a committed generated artifact into CI as a
  required status check (see `quality-gates-staleness`)
- Test a pattern check against its own source, as
  `quality-cross-validation` states

A line-length limit of 80, for example, pairs with:

```bash
awk 'length > 80' FILE
```

Pass condition: no output. Any line printed is longer than the limit.

## Conventions as tests

[ID: quality-gates-convention-as-test]

- Encode an "if X then Y" convention whose Y is mechanically comparable as
  a test, and name the pair that broke it in the failure

## Generated-file staleness

[ID: quality-gates-staleness]

Committed generated artifacts — rendered docs, configs, resolved chains,
schema output — drift silently without a gate.

- Wire the `--check` invocation from `base-docs` into CI as a required
  status check on the relevant paths
- Generate hand-written content that reproduces tool output behind a
  marker, so the gate covers it
- Enumerate the derivable blocks inside each artifact, not only the
  artifacts in the repository
- Generate a worked example of a tool's output too; it drifts first
- Make a generator fail when its declared destination or marker is missing
- Treat a banner naming the regenerate command as decorative without the
  gate
- Run the gate on the relevant paths; passing because skipped is not
  passing (see `quality-gates-scope-agreement`)
- Make the path filter enumerate all three inputs: the generator code, the
  source assets the render consumes, and the committed artifacts
- Never scope the filter to the generator alone
- Fail the gate when a committed artifact differs from a fresh render

## Procedure steps

[ID: quality-gates-procedure-steps]

- Audit a procedure step by step, recording against each step the check
  that enforces it, or that nothing does
- Gate the remaining steps, or mark each unenforced step as unenforced
  where it is written
- Gate first the step whose omission cannot be corrected afterwards

## Tier promotion

[ID: base-quality-gates-tier-promotion]

Gated tiers fail the build; ungated ones are spot-checked or verified
informally.

- When a bug in an ungated case resists every quick fix, promote the case
  to the next-strictest tier before the deep fix
- Land the deep fix against the metric the promotion created
- Apply the same move elsewhere, the first time a case lets a defect
  through: a flaky integration test to a contract test, a tutorial example
  to a CI-verified one, a manual smoke test to an automated regression

## Running a check

[ID: quality-gates-check-runs]

### Reporting

- Run a check in the form it ships before merging the rule
- Run a check whose subject is the change under review in the environment
  that builds its tree
- Report what a check inspected, not only what it found; the test-suite
  form of this rule is `testing-negative-assertion-coverage`
- Report how many checks a tool could not read beside how many it ran
  (MUST)
- Report every finding before exiting; where a check cannot continue past
  one, say so
- Decide which counts carry the verdict as `quality-cross-validation`
  states, from the pass condition rather than a sample of the output
- Report an empty result as a failure where emptiness means drift
- Emit ASCII only, and print an offending character's code point, never
  the character
- Triage a violation count far larger than expected as a possible defect
  in the check before working it as a backlog

### Controls

- Negative-control a check before merge: plant each break mode, confirm it
  is flagged, and confirm a valid input is not
- Plant behavioural breaks that keep the interface intact
- Show the plant reached the check, not only that the run failed: read
  which layer raised
- Force the path under test to run, then confirm from the run's own output
  that it acted
- Verify the plant landed in the artifact the check reads, by a diff or a
  re-read, before reading the run
- Name the mutated entity in the landing assertion, and compare its value
  on both sides
- Stage or commit before running a control that mutates the tree
- Plant into a throwaway copy whose clean state is known, so the landing
  check is a comparison (SHOULD)

### Shipped checks

- Take a check these templates ship as a pre-commit hook from the pinned
  repository, never by copying its code
- Run it with the command the template states; `--verbose` shows the
  counts a passing hook prints
- Read `not applicable: <reason>` as the hook finding nothing to check,
  never as a pass

```yaml
- repo: https://github.com/solid-ai-dev/solid-ai-templates
  rev: v3.0.0
  hooks:
    - id: find-unfenced-checks
      args: [--root, docs]
```

## Check timing

[ID: quality-gates-check-timing]

- Run a check after the change it gates, never before
- Where the check's subject is committed history, run it after committing,
  not after editing
- Fix a check that alters its own subject to inspect without mutating
- State the moment in the pass condition beside the command
- List "the change is not in the subject yet" among the causes of an empty
  result

## Check subject

[ID: quality-gates-check-selection]

A check can exit zero while reporting on the wrong thing, broken by a
change in another file whose reviewer has no reason to look.

- Select a check's subject by what is under test — the commit, the ref,
  the artifact name — never by recency or position
- Never filter on a property the violation can change
- State what a violating artifact's classification becomes, and cover that
  case with a second command and its own pass condition
- Treat a check that has never failed, on a rule never enforced, as blind
  until a planted violation makes it fail

## Gate scope

[ID: quality-gates-scope-agreement]

A gate breaks silently three ways: the formatter walks the wrong files,
the PR gate skips work, an aggregate job passes on skipped checks.

### Ignore lists and path filters

- Make the formatter and linter ignore lists and the CI path filter cover
  the same set of paths
- Verify a secondary toolchain with its own test runner, and document the
  split in the CI docs
- Exclude captured fixtures, scraped HTML or JSON of real external bytes,
  from the formatter
- Record, for a gate scoped by an explicit path list, why each candidate
  is off the list
- Ask first which candidate someone else runs; it is the likeliest omission

### Generator output

When a generator emits into a directory a commit-time formatter walks, all
three MUST hold:

- List the emitted path in the formatter's ignore list
  (`.prettierignore`, black `force-exclude`, or equivalent)
- Run a CI staleness gate (`<generator> --check`) on the same paths (see
  `quality-gates-staleness`)
- Land both in the same pull request

### Skipped jobs

- Never let the aggregate `gate` job report success when a code-touching
  change skipped the build through a path filter
- Distinguish "skipped because out of scope", a pass, from "skipped
  erroneously", a gap
- Encode that difference in the workflow, never in reviewer attention
- Verify the encoding on the skipped path: make one upstream job skip,
  confirm the gate fails, then revert

### Scope coverage

A gate green over almost nothing looks like a pass; review reads the
check, not its separate scope parameter:

| Gate | Scope parameter | Collapsed scope still exits zero |
|------|-----------------|----------------------------------|
| History secret scan | checkout fetch depth | scans the tip only |
| Linter | path filter or glob | lints zero files |
| Formatter check | ignore list | checks nothing |
| Test selector | marker or sampling rate | runs an empty selection |
| Coverage | measured package list | measures an empty set |

- Verify a gate whose scope is set by configuration by the coverage it
  reports, never by its exit status
- Wrap a gate that reports no coverage count so it fails on an implausibly
  small one, where the tool allows (SHOULD)
- Widen the scope parameter in the same change that widens what a check
  examines
- Never accept a green run as evidence that a scope change took effect

### Environment independence

A check whose input depends on the developer's environment passes in CI's
clean one and fails on a laptop.

- Enumerate tracked files (`git ls-tree`, explicit imports) rather than
  walk the working-tree filesystem (SHOULD)
- Gate a directory on an explicit anchor file, so local-only artifacts are
  filtered out
- Comment at the test any dependency on line endings, locale, timezone,
  case sensitivity or available binaries
- Run the gate locally on the development OS once per session where the CI
  matrix omits it

## Retrofitting a gate

[ID: quality-gates-retrofit-ratchet]

- Never make a red gate green by narrowing what it evaluates: removing a
  compared field, disabling a strict sub-flag or loosening a matcher
  (MUST NOT); exempting the failing instances is allowed (MAY)
- Retire an exemption whose remedy is known by applying the remedy
- Fix a genuine defect when the fix is small, instead of narrowing the check
- Clear a finding by changing the condition it describes, never the input
  the gate reads
- When a finding is false, fix the gate and record why in the same change
- Treat a gate whose cheapest remedy is falsifying its input as defective,
  and fix it in the same change (SHOULD)

### Linters

- Adopt a linter with its full rule selection and a per-file ignore table
  generated from its own output, never written by hand
- Pin the linter to a minor range; the table records one version's findings
- Never add a file to the table, or widen an entry, to make a gate pass

### Per-slice corpus

A gate with no per-file ignore, such as a test that enumerates its own
corpus, widens that corpus one cleaned slice at a time instead:

```
slice 1   ROOTS = ("scripts", "examples")     scripts/ and examples/ cleaned
slice 2   ROOTS = ("src", ...)                src/ cleaned
slice 3   ROOTS = ("src", "tests", ...)       tests/ cleaned
```

- Ship the gate with the list of directories it examines; each slice
  cleans one directory and widens the list in the same change
- Assert a floor on the number of files the gate enumerated, and re-size it
  in the change that widens the corpus
- Widen the corpus last in a slice, never first
- Keep the corpus as one list the gate reads, never a filter repeated at
  each call site

### Retiring a freeze

The table is the backlog, and shrinking it is the migration.

- Retire a freeze whose findings are raised where they are fixed in any
  order; cheapest first is a fair heuristic
- Retire a freeze whose findings are raised at the caller, such as a strict
  type checker's unannotated-call code, callees before callers
- Derive that order from the import graph before sizing the slices
- State the retirement order when the freeze is created
- Start a slice by emptying the entry and re-running the gate
- Delete a rule that then reports nothing, as a finding about the table
- Delete a dead rule name from an entry by hand; the ban on hand edits
  covers widening only
- Size one rule family by running the linter past its configuration with
  the family named; never edit the freeze to measure it
- Name the family: an unfiltered bypass measures the tool's defaults
- Where retiring an entry changes what code catches, accepts or returns,
  name the test that fails if the change goes too far
- Never count a suite that passed before the slice as that test
- Control the whole hierarchy: build every class with a value the
  interface cannot carry, and assert the declared error type comes back

### Site-local suppressions

- Suppress a finding that is wrong at one site at that site, never by
  adding the file to the freeze table
- Disable a rule in configuration only for a tree-wide decision, never to
  settle one site
- Name the rule in every suppression, such as `# noqa: B017` or
  `//nolint:errcheck`, and put the reason directly above the line

- Scan for a bare suppression:

```bash
pre-commit run find-bare-suppressions --all-files --verbose
```

- Require files scanned above zero and `bare (naming no rule)` zero
- Read zero files scanned as the hook's suffixes missing the project's
  languages; confirm a found count of zero rather than accept it

## Test edits

[ID: quality-gates-test-edit-boundary]

Strengthening a test needs no ceremony; weakening one redefines correct,
and takes a person.

- Strengthen the specification freely (MAY): add a test or tighten an assertion
  without escalation
- State why when a change deletes, loosens or rewrites an existing test
- Never merge such a change on a green suite alone
- When a change deliberately loosens a gate, add an assertion for the case
  the loosening admits, in the same change
- Name in that assertion's message why the case is admitted
- Where merges ride on green CI, remove auto-merge from a diff touching an
  existing test file; a diff only adding test files keeps it
- Put invariants that must not be renegotiated — safety, authentication,
  authorisation — under code ownership
- Fetch the base before classifying a change; a base that does not resolve
  fails the classification

- Classify a change against the project's test root, after committing it:

```bash
pre-commit run report-test-edits --hook-stage manual --all-files --verbose
```

- Require the not-pure-additions count to be zero for the change to keep
  the lenient path (MUST); each line after the counts names an edited test
- Set the ref with `--base`, by default `origin/main`, and the test root
  with `--tests`
- Read `not applicable` on a clean base as no change under review; on the
  base with uncommitted work it asks for a commit
- Read the line counts as a reading, not a verdict: more lines removed
  than added under the test root is a weakening shipped without its
  replacement
- Read a range total of zero as a check that inspected nothing

## Verdict reading

[ID: quality-gates-verdict-reading]

- Before acting on a failing verdict, decide whether the output is wrong,
  which the producer fixes, or the check is unsound for that input class,
  which a per-class fix to the check repairs
- Treat a passing gate as necessary, not sufficient, and name the artifact
  types a lenient gate leaves to a maintainer's review
