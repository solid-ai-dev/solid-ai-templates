# Base — Quality Gates

[ID: base-quality-gates]
[DEPENDS ON: templates/core/quality.md, templates/core/git.md]
[DEPENDS ON: templates/core/testing.md, templates/core/config.md]

How a check is built: retrofitting a gate without narrowing it, pairing a
constraint with its check, and running the check in the form it ships.
When gates run, and against which thresholds, is the project's choice.

---

## Retrofit a gate by freezing instances, never by narrowing it

[ID: quality-gates-retrofit-ratchet]

A complexity gate's ratchet is the familiar case. It generalises,
and it has a look-alike that is far more tempting because it is smaller:
writing a baseline is work, deleting a field from a comparison is one line
and the diff reads as a simplification. Both turn a red gate green. Only
one leaves a gate behind.

- A red gate MAY be made green by exempting the failing instances. It MUST
  NOT be made green by narrowing what the gate evaluates. Ratcheting freezes
  which instances fail and leaves the analysis intact; removing a field from
  a comparison, disabling a strict sub-flag or loosening a matcher removes
  the analysis for every case, including ones nobody has written yet
- The tell is what the exemption costs to reverse. A baseline entry is
  deleted and the case is checked again. A narrowed comparison leaves no
  record that the property was ever checked, so nothing prompts anyone to
  restore it
- An exemption is a holding position, not an outcome. It stops the gate
  reporting the instance and changes nothing about the instance, so the
  gate is now green over the defect it was added to catch. An entry whose
  remedy is known MUST be retired by applying it, not carried forward
  because the list is honest and documented
- When the failing case is a genuine defect and the fix is small, fix it. A
  check narrowed to accommodate one known defect is a permanent price paid
  for a temporary problem
- A finding MUST be cleared by changing the condition it describes, never
  the input the gate reads. The rules above govern the gate's
  configuration; this governs its data, under the same pressure. Editing a
  tracker field or a fixture to retire a finding leaves the gate green over
  a repository now additionally wrong about itself, and nothing afterwards
  tells that from a finding answered properly
- Where the finding is false, fix the gate and record why. A gate whose
  cheapest remedy is falsifying its input SHOULD be treated as defective in
  the same change

### Retrofitting a linter

Adopting a modern linter on an existing codebase produces a finding count
that makes the gate unadoptable as written. Four responses, two of which
are traps:

| Response | Outcome |
|----------|---------|
| Fix everything first | Buries the gate change under a mechanical diff no reviewer can separate from a behavioural one, and gates untouched code the change was never about |
| Ignore the offending rule families globally | Never ends. New code is ungated on exactly the rules the project says it wants, nothing ever fails, so nothing is ever fixed |
| Freeze per file | Works |
| Narrow the gate's corpus, widening it per slice | Works, where the tool has no per-file ignore |

- Enable the full rule selection, then record the violations existing on
  adoption day in a per-file ignore table, each file listed with exactly the
  rules it broke. A new file has no entry and is gated on everything, an
  existing file cannot get worse, and shrinking the table is the migration
- The table MUST be generated from the linter's own output, never curated by
  hand. A hand-maintained table drifts and becomes a place to hide findings
- The linter MUST be pinned to a minor range. The table records one
  version's findings, so a release adding rules to an already-selected
  family fails the gate on untouched code — the same reason a complexity
  gate pins its tool when the baseline format is version-sensitive
- A file MUST NOT be added to the table to make a gate pass, and an existing
  entry MUST NOT be widened. Without that rule the table becomes the global
  ignore list this whole approach exists to avoid

State the known cost rather than discovering it later: a file-level freeze
does not newly gate an existing file when it is edited. Line-level would,
and no widely available linter offers it.

### Where the gate cannot freeze per file

A freeze needs a per-file ignore mechanism and some gates have none — a
check written as a test, reading a corpus it enumerates itself. For those
the table above offers only "fix everything first", which the same table
rejects.

The inverse of the ratchet works instead. The gate ships carrying the list
of directories it examines, and each slice cleans one directory and widens
that list in the same change. The tree and the gate's reach move together,
so no slice merges unverified and the gate is green from its first commit
with no freeze table at all.

```
slice 1   ROOTS = ("scripts", "examples")     scripts/ and examples/ cleaned
slice 2   ROOTS = ("src", ...)                src/ cleaned
slice 3   ROOTS = ("src", "tests", ...)       tests/ cleaned
```

A ratchet freezes which instances fail and leaves the analysis whole; this
narrows the corpus and leaves the rule whole. Both are legitimate and they
suit different tools.

- The gate MUST assert a floor on the number of files it enumerated, and
  that floor is re-sized in the same change that widens the corpus. A
  configured scope is verified by coverage, not by exit status — a mistyped
  root enumerates nothing and reports a clean tree, which a narrowed corpus
  is otherwise indistinguishable from
- Widening MUST be the last thing a slice does, never the first. Widened
  before the directory is clean, the slice's own gate run is red and the
  author reads it as the gate being wrong
- The corpus MUST be one list read by the gate, not a filter repeated at
  each call site. A list that has to be widened in two places is widened in
  one, and the gate then reports on a corpus no document states

### Retiring a freeze

The table is the backlog and shrinking it is the migration. Which entry to
take next reads as a question the counts answer, and for one common class of
gate they answer it backwards.

- A freeze whose findings are raised where they are fixed comes off in any
  order, and cheapest-first is a reasonable heuristic. A freeze whose
  findings are raised at the *caller* — a strict type checker's
  unannotated-call code is the common one — comes off in dependency order,
  callees before callers
- Derive that order from the import graph before sizing the slices. A
  module's count is its own findings plus one for every call it makes into
  something still frozen, so a caller's count cannot fall while its callees
  are frozen. Cheapest-first lands on a leaf caller, which is then cleaned
  in full while its count barely moves
- State the retirement order at the freeze, not at the first slice. Nothing
  in the table records it and the counts point the other way, so an order
  left unstated is rediscovered at the cost of a wasted slice

The shape, with four modules and 514 findings taken root-first:

| Slice | Module | Own findings | Total remaining after |
| --- | --- | --- | --- |
| 1 | graph root | 330 | 152 |
| 2 | imports the root | 42 | 113 |
| 3 | imports both | 63 | 61 |
| 4 | leaf | 61 | 0 |

The first slice cleared 362 of the 514 while owning 330. The extra 32 were
caller-side findings in the three modules that import it, cleared without
touching them. Run cheapest-first, slice one is the 42 and clears well under
half of its own 42, which reads as the migration not working.

A slice starts before any code is touched, because the table is a record of
one day's findings and is never re-derived. A rule name outlives the findings
behind it — an unrelated refactor, a formatter pass, a dependency bump that
changes what a rule matches, another entry's cleanup — and a live entry and a
dead one are the same line of configuration.

- Empty the entry and re-run the gate first. A rule reporting nothing is
  deleted from the entry as a finding about the table, not as work done. The
  measurement costs one run per entry and is the first step of taking the
  slice on anyway, so it is free to whoever knows to read the result that way
- Read a stale entry as inverting the number the migration is planned
  against. The table says how much is suppressed and a maintainer sizes the
  next slice from it, so dead names make the work look larger than it is —
  the direction that keeps a migration parked
- Deleting a dead rule name from an entry is a hand edit, and the rule
  against curating the table by hand does not reach it. That rule forbids
  *widening*: an entry gaining a rule, or a file gaining an entry, to make a
  gate pass. Narrowing an entry to what the gate still reports is the
  migration itself

Retiring two entries in one downstream project found three of the thirty-two
rule codes they named had nothing behind them — a little under ten per cent,
in entries untouched since the linter was adopted. A project can be gated on
a rule it believes it is not gated on, which is harmless until someone reads
the table as a statement of what the codebase violates.

Sizing one rule family before taking it on is a question the table cannot
answer, since it suppresses exactly the findings being counted. The
destructive route — delete every entry naming the family, run the gate, read
the number, put the config back — edits the file the whole gate depends on in
order to size a decision, and is easy to restore imperfectly.

- Run the linter past its configuration instead, naming the family. Nothing
  is edited, the output is every finding the family hides, and the same
  command verifies the work afterwards by going to zero
- The family MUST be named. Bypassing the configuration drops the project's
  rule *selection* along with its ignores, so an unfiltered bypass measures
  the tool's defaults and prints a number that reads like the answer

```bash
# Sizes one rule family against the project's own gate without editing the
# freeze. The equivalents are `flake8 --isolated --select`, `eslint
# --no-eslintrc --rule`, `golangci-lint run --no-config --enable` and
# `pylint --rcfile=/dev/null --disable=all --enable`.
FAMILY="N802,N803"
ROOT="src"

if [ -z "$FAMILY" ]; then
  echo "FAIL: no rule family named -- an unfiltered bypass measures the"
  echo "tool's defaults, not this project's gate"
  exit 1
fi

echo "family: $FAMILY"
ruff check --isolated --select "$FAMILY" --statistics "$ROOT"
```

Pass condition: the command prints the family it measured, then a per-rule
count for it. Zero findings means the family is already clear and every entry
naming it is dead. An omitted family is refused rather than answered — the
two runs below both exit clean and only one of them is about this project:

```
ruff check --isolated --select N802,N803 src/   ->    0 findings, family clear
ruff check --isolated src/                      ->  366 findings, ruff defaults
```

Two different edits empty an entry and the gate cannot tell them apart. Take
one freezing a blind-except rule: using the caught exception silences the rule
while the blind handler stays exactly where it was, and narrowing the handler
to what its body can raise does the work the freeze stood in for. Both empty
the entry, both leave the gate green, and the cheap one is what a tired
migration reaches for.

- Where retiring an entry changes what the code catches, accepts or returns,
  name the test that would fail if the change went too far. Narrowing has a
  failure mode the gate cannot see: catch too little and a raw exception
  escapes through a clause nobody wrote, loosening the contract the module
  documents while every rule stays quiet
- A suite that passed before the slice is not that control. It passes
  afterwards for the same reason it passed before — none of its cases
  provokes the type the change stopped catching
- The control walks the family, not the site the slice touched. A contract
  test that builds every class in the hierarchy with a value the interface
  cannot carry, and asserts the declared error type comes back, reports the
  sites a per-file review does not reach

Narrowing seventy handlers in one downstream migration left four sites wrong:
three where a constructor argument is taken on trust, so a caller passing the
wrong object raises `AttributeError`, and one where arithmetic runs before the
encode and raises `TypeError`. All four were found by a contract test that
existed for its own reasons. Without it the slice would have merged green and
shipped a narrower error contract than the module documents.

### The suppression beside the table

The freeze answers "this file was already broken on adoption day". It does
not answer "this rule is wrong at this one line", and the two are different
claims. A project holding only the first has one mechanism for both, and
the rule forbidding a file being added to the table to make a gate pass
correctly blocks it — leaving an undocumented escape as the only move.

- A finding that is genuinely wrong at one site MUST be suppressed at that
  site, not by adding the file to the freeze table. Adding the file
  suppresses the rule for every other line in it, including lines nobody
  has written yet
- A site-local suppression MUST name the specific rule — `# noqa: B017`,
  `//nolint:errcheck`, `// eslint-disable-next-line no-unused-vars` — and
  MUST NOT be bare. A bare suppression silently absorbs every rule that
  later applies to the line; a named one keeps failing on the next
  finding, and that is the property that makes the escape safe to allow
- The reason MUST sit directly above the line, where `base-quality` puts a
  block comment. The directive itself is the one comment that trails to
  the right of code, which is why the reason cannot travel with it
- A config-level disable is reserved for a decision that is genuinely
  tree-wide. Reaching for it to settle one site is the global ignore the
  freeze exists to avoid, arriving by a different door

The case that shows the two are not interchangeable: a test deliberately
asserts on a broad exception because the narrower class varies by
interpreter version, which is what the testing rules ask for — where a test
asserts a misuse fails, assert that it fails, not how. The linter asks for
the opposite and is wrong there. Narrowing the assertion reintroduces the
platform dependence the rule exists to prevent, and freezing the file
suppresses the check for every other assertion in it. Only the site-local
escape resolves it, and only a named one keeps the line gated afterwards.

Pair the rule with a check, since a bare suppression is one character
shorter than a named one and decays toward the shorter form:

```bash
py - <<'EOF'
import pathlib, re

SUPPRESSIONS = (
    ("noqa", re.compile(r"noqa(?![:])")),
    ("nosec", re.compile(r"nosec(?![:]|[ ][A-Z][0-9])")),
    ("nolint", re.compile(r"nolint(?![:])")),
    ("eslint-disable-next-line",
     re.compile(r"eslint-disable-next-line(?![ ]*[a-zA-Z@])")),
)

HASH = (".py", ".sh", ".rb", ".yml", ".yaml")

# Vendored and installed code is not this project's to suppress in. Left
# in scope it dominates the count -- an environment directory carries
# thousands of files and hundreds of third-party suppressions, and the
# project's own handful is invisible among them.
SKIP = (".venv", "venv", "node_modules", "build", "dist", ".git", ".tox",
        "vendor", "site-packages")
files = [p for p in pathlib.Path(".").rglob("*")
         if p.is_file() and p.suffix in (".py", ".js", ".ts", ".go", ".jsx", ".tsx")
         and not any(part in SKIP for part in p.parts)]
print("files scanned: %d" % len(files))
total = 0
bare = []
for path in files:
    marker = "#" if path.suffix in HASH else "//"
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        # Only the comment half of the line can hold a directive. Scanning
        # the whole line makes the check match its own pattern table.
        if marker not in line:
            continue
        comment = line.split(marker, 1)[1]
        for name, pattern in SUPPRESSIONS:
            if name in comment:
                total += 1
                if pattern.search(comment):
                    bare.append("%s:%d: %s" % (path.as_posix(), i, line.strip()))
print("suppressions found: %d" % total)
print("bare (naming no rule): %d" % len(bare))
for entry in bare:
    print("  %s" % entry)

raise SystemExit(1 if bare else 0)
EOF
```

Pass condition: the check prints how many files it scanned and how many
suppressions it found, then `bare (naming no rule): 0`. A scanned count of
zero is a failure rather than a clean tree — it means the suffix list does
not match the project's languages, and every suppression in it went
unread. A found count of zero on a project that has adopted the freeze is
worth confirming rather than accepting.

---

## A gate bounding a length discovers its exemptions

[ID: quality-gates-length-bound-exemptions]

`quality-gates-retrofit-ratchet` and `quality-gates-scope-agreement` both
assume a gate whose findings can be listed on adoption day — that is what
makes a freeze table generatable. A gate that bounds a LENGTH does not
behave that way. Its exemptions are not knowable before it runs: they
surface one slice at a time, and a list that stopped growing while the
corpus is still growing is a finding rather than a finished adoption.

- Where a gate bounds a length, treat the exemption list as DISCOVERED
  rather than derived. Generating the freeze on adoption day is complete
  for a gate that finds instances; for one that bounds a length it is
  complete only for the slice adopted so far
- Test each candidate against one question: is the number of lines the
  author's choice? Where something else sets the count — a licence text,
  one label per line of code, a banner ruled top and bottom, a table whose
  rows are a published specification's fields — the bound is not measuring
  what it was written to measure, and the exemption is real
- Express the exemption as the SHAPE that makes the count external —
  ruled on both sides, rows naming byte offsets — never as the file or the
  directory it was found in. A path-scoped exemption absorbs every future
  violation in that neighbourhood, which is exactly what the freeze exists
  to avoid
- An exemption arriving in a later slice is not a defect in the earlier
  ones. Adopt in slices, and expect the list to grow while the corpus does

Measured on a project adopting a two-line comment bound and a ten-line
docstring-prose bound across roughly 99 files. Four exemptions surfaced
across two slices — a licence header, comments trailing consecutive lines
of code, a banner ruled top and bottom, and a wire-layout table — and all
four share the property that something other than the author sets the
count.

---

## Editing a test moves the standard, not the work

[ID: quality-gates-test-edit-boundary]

`quality-gates-retrofit-ratchet` bans turning a red gate green by narrowing
what it evaluates. Where the tests are the source of truth for correctness,
the same move is available one level up, and a merge-on-green policy does
not see it: the tests are both the standard and a set of files the change
may edit. A suite that was weakened still reports green, and that green
proves only that the code matches whatever the tests were reduced to — not
that the behaviour they guarded still works.

The boundary is between proposing work and redefining the standard the work
is measured against. Strengthening the specification needs no ceremony;
weakening it is a different act and takes a person.

- A change MAY strengthen the specification without escalation. Adding a
  test, or tightening an assertion, can only narrow what passes, so a green
  run afterwards means more than it did before
- A change that deletes, loosens or rewrites an existing test MUST state
  why, and MUST NOT merge on a green suite alone. It changes what correct
  means, and the suite cannot report that it has
- A change that deliberately loosens a gate MUST add an assertion for the
  case the loosening admits, in the same change. That case usually moves off
  a break list and onto nothing: it passes because a check stopped firing,
  not because anything says it should pass. Move it to a positive control
  rather than deleting it, and the gate keeps a test that fails if the
  loosening is reverted
- The assertion's message MUST name why the case is admitted. The stated
  reason otherwise lives in a pull request body and a decision record, and
  the suite consults neither; what the next reader meets is a comparison
  that looks careless — an off-by-one, a `>=` where a `>` was surely meant.
  Tightening it back is a one-character change that passes the whole suite,
  so the loosening is indistinguishable from a defect and reverting it is
  indistinguishable from a fix
- Where merges ride on green CI, separate the two mechanically: a diff
  touching an existing test file loses auto-merge or lenient-review
  eligibility, and a diff that only adds test files keeps it. The filter is
  the enforceable half; the stated reason is the half a reviewer reads
- Put the invariants that must not be renegotiated under code ownership —
  safety, authentication, authorisation — so weakening one needs the owner
  rather than the author

Classify a change against the project's test root, reporting what it
inspected as well as what it found:

```bash
BASE=origin/main
if [ "$(git rev-parse HEAD)" = "$(git rev-parse $BASE)" ]; then
  if [ -n "$(git status --porcelain)" ]; then
    echo "HEAD is at $BASE and the work is uncommitted; commit it and run again"
    exit 0
  fi
  echo "HEAD is at $BASE and the tree is clean; no change is under review, so this check does not apply"
  exit 3
fi
ALL=$(git diff --name-status $BASE...HEAD)
TESTS=$(git diff --name-status $BASE...HEAD -- 'tests/*')
LOOSENED=$(echo "$TESTS" | grep -vE '^A' || true)
NUMSTAT=$(git diff --numstat $BASE...HEAD -- 'tests/*')
ADDED=$(echo "$NUMSTAT" | awk '{ total += $1 } END { print total + 0 }')
REMOVED=$(echo "$NUMSTAT" | awk '{ total += $2 } END { print total + 0 }')
echo "files changed in range: $(echo "$ALL" | grep -c . || true)"
echo "test-file changes inspected: $(echo "$TESTS" | grep -c . || true)"
echo "changes that are not pure additions: $(echo "$LOOSENED" | grep -c . || true)"
echo "test-root lines added: $ADDED"
echo "test-root lines removed: $REMOVED"
echo "$LOOSENED" | grep . || true
```

The check's moment is a change under review, so it answers that first. On
the base with a clean tree there is no change to classify and it reports
that it does not apply, with exit status 3 — the reserved status for a
check answering that its moment is not in progress. On the base with an
uncommitted change it exits clean instead and says so in those words: the
operator has something to do, and a status meaning no reader is needed
would be wrong. The natural moment to run this is while writing the
change, and that run would otherwise report five zeros.

Pass condition: the five counts are the reading and the not-pure-additions
count MUST be zero; anything printed after them is the list of loosened
changes, and a change keeps the lenient path only while that list is empty.

The two line counts are for the person a non-empty list summons, not for
the gate. A deliberate loosening fails the pass condition by design, and
what the reviewer needs next is whether the admitted case was asserted:
lines removed from the test root exceeding lines added is the shape of a
weakening that shipped without its replacement. It stays a signal rather
than a threshold, because a rename or a reformat moves both counts — so it
is read, not scored.

The first count is what separates the two zeros. A test-file count of
zero under a non-zero range total is a real answer — the change touched
no tests, which needs no escalation. A range total of zero says the range
itself is empty, so the check inspected nothing and its second count
establishes nothing either. Reporting only the second, as this check once
did, makes those two indistinguishable.

This is governance, not a new pass/fail metric: it adds no threshold and
changes nothing about which gates run.

---

## Reading a gate verdict honestly

[ID: quality-gates-verdict-reading]

A gate verdict is a signal to interpret, not a conclusion to act on
blindly. Two failure modes sit on either side of the pass/fail line.

### Disaggregate verdict, plausibility, and accuracy

When a gate fires, its single verdict often conflates three judgments:

- **Verdict** — what the gate says (pass / fail / LOW)
- **Plausibility** — is the output *shape* consistent with priors,
  sanity checks, and schema invariants?
- **Accuracy** — does the output match ground truth where it exists?

A "LOW" can mean the output is inaccurate, the plausibility check is
unsound for this input class, or both — and each implies a different
fix (fix the producer / tune the check per-class / both). Separate them
before acting. Worked example: a gate's plausibility check flagged a
record whose output matched the reference on nearly every field — the
check's assumption was unsound for that input class, so the fix was a
per-class exception to the check, not a change to the producer. The
verdict alone pointed the wrong way.

### Lenient gates need a human residual check

The complement to a noisy gate is a lenient one: it passes, but a human
glance catches a defect the gate cannot. A single-sample dip in a curve
can pass a tolerance averaged across samples. Tightening the threshold
to catch it would mis-flag legitimate runs; instead keep the gate AND
document that the artifact type requires a maintainer-eye review before
commit. A passing gate is necessary, not sufficient.

---

## Gate scope agreement

[ID: quality-gates-scope-agreement]

In a polyglot repo where a secondary toolchain lives in a subdirectory
(e.g. a Python `tools/` directory inside a TypeScript static site), or
where captured test fixtures (scraped HTML/JSON representing real
external byte sequences) live in-tree, three failure modes silently
break the gate: the formatter walks files it should not touch, the
PR gate skips work the deploy gate runs unconditionally, and an
aggregated `gate` job reports success on skipped checks. The rules
below close those gaps.

### Ignore lists and CI path-filter MUST agree

- The formatter/linter ignore lists and the CI path-filter that
  triggers the gate MUST cover the same set of paths — a directory
  excluded from one MUST be excluded from the other
- A secondary toolchain with its own test runner is verified by that
  runner, not the primary stack's gate. Document the split in the CI docs;
  runner selection alone does not require an ADR
- Captured test fixtures (scraped HTML/JSON representing real external
  byte sequences) MUST be excluded from the formatter — they must
  stay byte-for-byte, and reformatting them changes the test input
- A gate scoped by an explicit path list MUST record why each candidate
  NOT on it is off it. Distinct from a collapsed scope: here the gate
  works as configured and the configuration was never complete. An
  author enumerates what they run, so ask which candidate someone else
  runs — that one has the weakest guarantee about its environment and
  is the likeliest omission

### Formatter-vs-generator escalation

When a generator (script, codegen, scaffolder) emits a file into a
directory that a commit-time formatter (prettier, black, gofmt) walks,
three things MUST hold together:

- The emitted path MUST appear in the formatter's ignore list
  (`.prettierignore`, black `force-exclude`, or equivalent)
- A CI staleness gate (`<generator> --check`) MUST run on the same
  paths (see `quality-gates-staleness`)
- Both MUST land in the same PR — the ignore line without the gate,
  or the gate without the ignore line, leaves silent drift

Without all three, the formatter mutates generator output between
commits and the generator's `--check` fails on a clean checkout — so
the staleness gate cannot even be wired into CI.

### Skipped is not passed

- When a code-touching change would skip the build job via a
  path-filter, the aggregation / `gate` job MUST NOT report success
  by default
- Distinguish "skipped because out of scope" from "skipped
  erroneously" — the former is a pass equivalent, the latter is a
  gap. An aggregator that treats them identically is the
  gate-by-omission anti-pattern
- A passing-because-skipped check looks identical to a passing
  check in the GitHub UI; the difference MUST be encoded in the
  workflow, not left to reviewer attention
- That encoding MUST be verified on the skipped path, not only on the
  failing one. A failed upstream trips a correct fan-in (comparing
  every result against success) and a naive one (comparing against
  failure) alike, so only a skipped upstream separates them. Make one
  upstream job skip temporarily, confirm the gate fails, and revert —
  the whole test is one commit and one revert

### A configured scope is verified by coverage, not exit status

A gate that ran, went green, and covered almost nothing renders
identically to a real pass. It is worse than a skip, because a skip is at
least visible as one. The check and the parameter setting its input scope
are separate things, and review usually looks only at the check:

| Gate | Scope parameter | Collapsed scope still exits zero |
|------|-----------------|----------------------------------|
| History secret scan | checkout fetch depth | scans the tip only |
| Linter | path filter or glob | lints zero files |
| Formatter check | ignore list | checks nothing |
| Test selector | marker or sampling rate | runs an empty selection |
| Coverage | measured package list | measures an empty set |

- A gate whose input scope is set by a configuration parameter MUST be
  verified by the coverage it reports, not by its exit status. Where the
  tool emits a count of what it covered, read that count; where it does
  not, the gate SHOULD be wrapped so it fails on an implausibly small one
- Widening what a check examines MUST widen its scope parameter in the
  same change — the two are one edit, and splitting them leaves a gate
  that reads stronger than it is
- A reviewer MUST NOT accept a green run as evidence that a scope change
  took effect

`security/devsecops.md` requires full history for the secret scan
specifically. This is the general rule that the specific one is an
instance of, and it holds whichever platform a project uses.

### Green CI does not prove environment independence

CI runs on a clean checkout in one controlled environment. A passing
gate is NOT "no bugs" when the check's input or behavior depends on the
developer environment:

- The test reads the working-tree filesystem (`readdirSync`, `glob`)
  rather than tracked files (`git ls-tree`, explicit imports), so local
  scratch or gitignored artifacts change its input — CI never sees them
- The test depends on line endings, locale, timezone, filesystem case
  sensitivity, or available binaries
- The CI matrix omits the OS or runtime contributors use locally

For such tests: prefer tracked-files enumeration over filesystem walks;
gate a directory on an explicit anchor file so local-only artifacts are
filtered out; document the dependency in a comment at the test; and run
the gate locally on the dev OS at least once per session — local-first
catches what a clean-room CI cannot.

---

## Promote a resistant case to a gated tier
[ID: base-quality-gates-tier-promotion]

Projects with a tiered test/fixture system separate gated cases (a
golden-output or ground-truth regression that fails the build) from
ungated ones (spot-checked CI runs, confidence priors, informally
verified internal calls). When a bug surfaces in an ungated case and the
quick-fix candidates all probe-falsify against the existing gated
anchors, promote the affected case into the next-strictest tier before
attempting the deep fix. Promotion converts a silent failure into a
measurable metric, so the eventual fix lands against a regression target
instead of working blind.

The shape generalizes: promote a flaky integration test to a contract
test with a stronger oracle; promote a tutorial example to a CI-verified
example the first time doc-rot slips through; promote a manual smoke test
to an automated regression the first time a regression escapes. When a
fix does not fit one session, measure first by elevating the case a tier;
the deep fix follows with the metric as the gating signal.

## Generated-file staleness gate

[ID: quality-gates-staleness]

When a project commits generated artifacts (rendered docs, generated
configs, resolved template chains, code-from-schema output) AND uses
the `--check` convention from `base-docs`, the `--check` invocation
MUST be wired into CI as a required status check on the relevant
paths.

- Ask first whether the content should be generated at all. A block that
  is derivable tool output — a file listing, a resolved chain, a table of
  counts — and was written by hand is not stale in this gate's sense. It
  sits outside the gate's subject, so the gate reports nothing about it
  while looking as though it governs the file. Put it behind a marker and
  generate it, and the gate covers it from then on
- A gate MUST account for what it covers, not only for what it found. One
  file can hold a generated section and a hand-maintained block
  reproducing tool output, and `--check` reports that file in sync while
  the hand-written half is wrong. Enumerate the derivable blocks inside
  each artifact, not just the artifacts in the repository. This is
  `quality-gates-check-runs`'s "state what it inspected, not only what it
  found" one level up, applied to a gate rather than to a command
- A worked example is where this lands most often: a document explaining
  a tool by showing its output, in a file whose other sections are
  generated. The example is reproducible by one call and reads as prose,
  so nobody wires it up, and it drifts from the moment the tool's output
  changes
- A generator writing into a declared destination MUST verify the
  destination exists and fail when it does not. Substituting nothing is
  not having nothing to substitute: a marker the file no longer carries
  matches nothing, so the text comes back unchanged and `--check`
  compares it against itself. Deleting a marker pair freezes that block
  permanently, gate green over it
- A banner naming the regenerate command is decorative without the
  gate — a stale file looks identical to a fresh one, and the
  regenerator can silently break for months unnoticed
- A staleness gate that is never run on the relevant paths is the
  gate-by-omission anti-pattern named in `quality-gates-scope-agreement`
  — passing-because-skipped is not passing
- "The relevant paths" are three input classes, and the filter MUST
  enumerate all of them: the generator or source code, any source assets
  the render consumes (images, schemas, fixtures), and the committed
  artifacts themselves. A hand-edit or an incomplete regeneration is
  drift the gate exists to catch, and it lives in the artifact rather
  than the generator. This is the enumerate-every-input rule from
  `quality-gates-scope-agreement`, stated where a staleness filter is
  actually written
- A filter scoped to the generator alone is the common shape of that
  mistake, because the issue asking for the gate usually names the
  generator's path and a straight reading stops there
- The gate MUST fail when the committed artifact differs from a fresh
  render, exactly as it fails on lint or type errors

---

## Pair a checkable constraint with its check

[ID: quality-gates-pair-check]

`quality-gates-staleness` is one case of a general rule: a stated
constraint without its check is decorative. It looks enforced and
decays silently, because a violating artifact looks identical to a
clean one. A constraint that travels into a generated project (a
template output constraint inherited by a generated `CLAUDE.md`) carries
this risk furthest — the project inherits the rule with no protocol to
self-check it.

- An output constraint that is mechanically checkable MUST name its
  agent-runnable check — the command to run and the pass condition. A
  line-length limit of 80, for example, pairs with:

```bash
awk 'length > 80' FILE
```

  Pass condition: no output. Any line printed is longer than the limit
- State the check next to the rule it verifies — not in a separate
  tooling file the generated project never receives. The rule and its
  check MUST travel together, so every artifact generated from the
  template inherits both
- The command MUST sit in a fenced block. The fence is what makes a
  check extractable: a tool can count the checks a document states, run
  them, and reconcile the two counts, and none of that reaches a command
  typed into a sentence. Prose introduces the check and carries its pass
  condition beside the fence; the runnable form lives inside one
- Naming no command states no check. A sentence describing an action
  ("install the project, then execute every file under the examples
  directory") reads as a check and is not one, and the fence rule does
  not reach it because there is nothing to move. An author who has
  written no command sees nothing to fence, so write the command first
- A tool reporting how many checks it ran MUST also report how many it
  could not see. A count taken over the parseable form alone is complete
  only by assumption, and that assumption is what fails: a green run
  over every extractable check coexists with a violated rule whose check
  was typed in prose, and nothing in the run says so
- A constraint that is inherently subjective (imperative tone, "no
  explanatory prose", heading-case judgment) stays declarative and
  relies on review. Do NOT invent a brittle check to satisfy this rule
- When the constraint guards a committed generated artifact, wire its
  check into CI as a required status check (see
  `quality-gates-staleness`)
- A check written against a pattern will find that pattern in its own
  source wherever the scan can reach the file it lives in, reporting
  findings that are not defects or absorbing ones that are. The failure
  and the test that catches it are stated once, in
  `quality-cross-validation` — it applies to every check a project
  carries, not only to the ones a gate runs

The unrunnable form is mechanically findable. A backticked command in a
sentence of running prose, introduced by a verification phrase or followed
by its verdict ("output must be empty"), with no fence beside it to hold
the runnable form, is a check no tool can extract. Match
over the paragraph and not over the line: prose wraps, so a check written
inline is split across two lines by the project's own line-width rule, and
a line-scoped detector reads each half as innocent. Two rules that are
individually correct combine into a blind spot, and every line-scoped
detector over a wrapped corpus carries that exposure.

```bash
py - <<'EOF'
import io, os, re

# Point ROOTS at the directories holding the project's rule documents --
# templates, context files, contributor guides. Anywhere a rule may state
# a check.
ROOTS = ["templates"]

# A stated check pairs a verification phrase with the command it
# introduces. The pair is matched over a paragraph, because a wrapped
# check puts the phrase on one line and the command on the next.
PHRASE = re.compile(
    r"(?:verify|check|confirm)\s+with"
    r"|(?:verified|checked|confirmed)\s+by"
    r"|pass condition"
    r"|\b(?:[\w-]+\s+)?checks?:",
    re.IGNORECASE)
COMMAND = re.compile(r"[`][^`]+[`]")

# The other order: the command comes first and its pass condition after
# it, with no announcing phrase at all.
VERDICT = re.compile(
    r"output\s+must\s+be\s+empty"
    r"|\bno\s+output\s+means"
    r"|\bis\s+done\s+when",
    re.IGNORECASE)

# A sentence boundary between the phrase and the command means the
# paragraph talks ABOUT a check and names a command somewhere else.
# Requiring the two to share a sentence is what separates a check stated
# in prose from prose that mentions one.
BREAK = re.compile(r"[.]\s")
WINDOW = 5

# Written rather than spelled literally: three backticks at the start of a
# line would close the block this check is quoted inside. Fenced lines are
# skipped, so the check does not match its own source either way.
FENCE = "`" * 3
BULLET = re.compile(r"\s*(?:[-*+]\s|\d+[.]\s)")

inspected, findings = 0, []

def examine(path, para, numbers, marks):
    """Record a finding where the paragraph states a check no fence holds."""
    if not para:
        return 0
    near = min(min(abs(m - n) for m in marks) for n in numbers) if marks \
        else WINDOW + 1
    if near <= WINDOW:
        return 1
    joined = " ".join(line.strip() for line in para)
    pairs = [(p, COMMAND.search(joined, p.end()))
             for p in PHRASE.finditer(joined)]
    pairs += [(c, VERDICT.search(joined, c.end()))
              for c in COMMAND.finditer(joined)]
    for first, second in pairs:
        if second and not BREAK.search(joined[first.end():second.start()]):
            findings.append("%s:%d %s" % (
                path, numbers[0], joined[first.start():second.end()]))
            break
    return 1

for root in ROOTS:
    for parent, _, names in os.walk(root):
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            path = os.path.join(parent, name)
            lines = io.open(path, encoding="utf-8").read().splitlines()
            marks = [n for n, line in enumerate(lines, 1)
                     if line.lstrip().startswith(FENCE)]
            fenced, para, numbers = False, [], []
            for number, line in enumerate(lines, 1):
                stripped = line.lstrip()
                skip = (stripped.startswith(FENCE) or not line.strip()
                        or stripped.startswith("|") or stripped.startswith("#"))
                if skip or (para and BULLET.match(line)):
                    inspected += examine(path, para, numbers, marks)
                    para, numbers = [], []
                if stripped.startswith(FENCE):
                    fenced = not fenced
                    continue
                if fenced or skip:
                    continue
                para.append(line)
                numbers.append(number)
            inspected += examine(path, para, numbers, marks)

print("prose paragraphs inspected: %d" % inspected)
print("checks stated outside a fence: %d" % len(findings))
for finding in findings:
    print("  " + finding)

raise SystemExit(1 if findings else 0)
EOF
```

Pass condition: the inspected count is above zero and the finding count is
zero. An inspected count of zero means `ROOTS` named nothing that exists,
which is the check reaching no input rather than a clean tree.

`PHRASE` and `VERDICT` are vocabularies, not patterns. Add a literal when a
check in the project is found announcing itself, or stating its verdict,
with wording the lists do not carry, and add it together with the instance
that motivated it; a phrase nobody writes widens the false positives and
finds nothing. Any edit to either MUST be controlled in both directions: a
check stated in prose is reported,
and that same check moved inside a fence is not.

A rule states intent; its paired check is what makes the intent hold.

---

## An ungated step beside a gated one reads as enforced

[ID: quality-gates-procedure-steps]

`quality-gates-pair-check` covers a constraint with no check, and
`quality-gates-check-runs` covers a check that was written and never
run. Neither covers a documented *procedure* whose steps are enforced
unevenly. Here the constraint is stated, the neighbouring check exists
and runs correctly, and what fails is the reader's inference across
steps — so no artifact is wrong until much later.

An operator runs the sequence top to bottom. One step's gate fires,
fails, is fixed, and passes, which is felt as the procedure checking the
work. The ungated step is simply not done and nothing reports it. A
procedure with no gates at all invites care; a procedure with one gate
invites trust in all of it.

- Enforcement is not transitive between adjacent steps. A gate covers
  the step it is attached to and says nothing about its neighbours,
  however the sequence reads
- Audit a procedure step by step, not procedure by procedure, recording
  against each step the check that enforces it or the fact that nothing
  does
- Either gate the remainder, or mark each unenforced step as unenforced
  where it is written, so an operator's confidence matches what is
  actually being verified
- Gate first the step whose omission cannot be corrected afterwards. The
  cost is asymmetric — re-cutting a published release to repair an
  omitted step is worse than the gap, so the archive keeps the gap
  permanently

---

## Run the check in the form it ships

[ID: quality-gates-check-runs]

`quality-gates-pair-check` requires a constraint to name its check. It
does not make that check work. A check that was written but never run is
the decoration the pairing rule exists to prevent, and it is worse than
none, because it looks enforced. A check that travels into a generated
project fails there, where nobody wrote it and nobody can debug it.

- A check MUST be run in the form it ships before the rule is merged.
  Extract it from the committed file and execute it — writing a check is
  not running it, and the file is a different medium from the editor
- The form is not the whole of it: a check whose subject is the change
  under review reads a tree the host constructs, and the run that proves
  it works is the first one in that environment. `base-git` states what
  that run has to show
- A check MUST state what it inspected, not only what it found. A command
  that reached zero files and a command that found zero violations print
  the same thing. Report the count of inputs examined. The same rule for
  an assertion inside a test suite is `testing-negative-assertion-coverage`
- A check that has read its whole corpus MUST report every finding it
  holds before it exits. Stopping at the first turns one review into as
  many runs as there are offenders, and the operator learns the size of
  the problem only by fixing it one item at a time. Where the check
  genuinely cannot continue past a finding, it MUST say so, or the one
  it names reads as the only one there is
- Where a check states both a verdict and a reading, which of its counts
  carry the verdict and which are for the reader it escalates to is
  governed by `quality-cross-validation`, together with the rule that a
  disposition is read from the stated pass condition rather than from a
  sample of the output
- Where an empty result means drift rather than health, the check MUST
  report it as a failure — no journal entries found means the heading
  format moved, not that the file is ordered
- A check MUST emit ASCII. One that reports an offending character MUST
  print its code point, never the character, or it dies on the console
  encoding while reporting exactly what it exists to detect
- A fenced check MUST NOT be indented more deeply than the first
  indentation level of the code inside it. A renderer strips the fence's
  own indentation from every line that has it, so a block indented five
  spaces under a numbered step turns a four-space nested line into a
  three-space one and the extracted body stops compiling. Put the check
  flush with the margin and point to it from the step
- A check MUST be negative-controlled before merge: name the break modes
  it catches, confirm each one is flagged, and confirm that a valid input
  is not. A negative control that silently matches nothing has tested
  nothing
- The break a control plants MUST be behavioural, leaving the interface
  intact. A control that trips on a signature, an import or a missing file
  has exercised the harness rather than the check: it fires convincingly
  and says nothing about whether the check detects the condition. Where
  the fix added a parameter, the control that discriminates is a version
  that accepts the parameter and ignores it — the shape a careless later
  edit takes — not one that removes it and raises a type error
- A control MUST show the plant reached the check, not only that the run
  failed. Where a layer sits in front — a parser, a schema, an auth check
  — the easiest thing to corrupt is what it inspects, so it raises there
  and the check never runs. Exit status is the same either way, so read
  which layer raised; corrupting a value rather than a structure gets
  past the earlier ones
- A control MUST also force the path under test to run. Satisfying the
  precondition is not the same as exercising it: a tool that writes only
  when its output differs does nothing to a file already in its target
  state, so the run reports clean having never executed, and that reads as
  the tool being innocent of what it is suspected of. Put the subject in a
  state the path must act on — stale the input the tool compares against,
  clear the cache it would reuse, invalidate the credential it would still
  accept — then confirm from the run's own output that it acted
- The step that plants a break MUST itself be verified. Planting is an
  edit, and an edit that matched nothing exits zero and prints nothing, so
  a break that never landed and a check that never fired produce identical
  evidence — one says the check is blind, the other says it is fine.
  Confirm the planted input differs from the clean one, by a diff, a
  re-read, or a fixture the edit returns, before reading the run. Prefer
  planting into a throwaway copy whose clean state is known, so the
  confirmation is a comparison rather than an inspection. Confirm it in
  the artifact the check reads, which is often not the one edited — a
  listing from git's index does not see the working tree, nor does one
  from a build output or a cache. A deletion confirmed on disk leaves an
  index-reading check green, which reads as the check being blind: the
  comfortable conclusion, and nothing later contradicts it
- The landing assertion MUST name the entity it mutated and compare that
  entity's value on both sides. An assertion that merely finds the planted
  value somewhere in the artifact passes when a sibling already carried it,
  so it holds whether or not the edit landed — the weakest link in a
  control is the step meant to prove it happened. Read the field, the row
  or the key by name before and after; a search across the whole artifact
  is not that read
- Stage or commit before running a control that mutates the tree. The
  revert step is usually a restore from the index, which discards unstaged
  work without saying so, and an uncommitted edit to the file under test is
  exactly what it destroys. Any revert reading a recorded state rather than
  a copy taken at the start of the control has this property; take the copy
  where the work is not yet recorded
- A fix with no observable effect on the tree it lands in MUST ship a
  check against a synthetic subject reproducing the condition. A
  preventive fix changes nothing measurable where nothing currently
  triggers it, so the suite prints the same output on both sides of it and
  a passing run is evidence for neither. Without the synthetic subject the
  fix is indistinguishable from a no-op — including to whoever later reads
  it as unnecessary and removes it
- Where the working tree can be put into the failing state, demonstrate
  the defect on the branch that fixes it. A check reporting zero with the
  fix's own edit still uncommitted, and the true count once it is
  committed, is the defect and its repair in one pair of runs over real
  inputs, at no cost beyond running the command twice
- Prefer a form that survives being copied. A heredoc whose delimiter is
  quoted passes escapes through untouched; an inline `-c` string loses
  them to shell expansion and arrives as a `SyntaxError`. Do not write the
  heredoc opener itself in prose — an extractor scanning for it reads the
  sentence as a check, the way a backticked directive is read as a real
  declaration
- A line continuation MUST be confirmed to have survived into the
  committed file. A trailing backslash can be dropped on the way from
  author to file, and when it is, the lines join and nothing reports it:
  the shell accepts the joined command, the compile gate accepts it, and
  only the text has changed. Reading the committed line back is the whole
  check: this break mode fails neither loudly nor closed
- SHOULD avoid needing the confirmation. Fold the command onto one line —
  a fenced block is exempt from the width limit precisely so that is
  available — or bind its parts to shell variables. Where a continuation
  is genuinely the clearest form, keep it and verify it; the construct is
  not the defect, the silent loss is
- The same silent loss applies to **quoting** such a line, not only to
  writing one. A search string, patch, fixture or prose example carrying
  the backslash is reconstructed by the same path, and the symptom
  inverts: an anchor that will not match text plainly present in the file.
  Construct the character with `chr(92)` rather than transcribing it
  wherever the reconstruction has to be exact
- An embedded check MUST NOT depend on a backslash escape surviving the
  authoring path at all. A lost continuation is detectable by
  construction — a line that was two is now one — but an escape lost from
  inside a pattern leaves a check that is the right length, parses, runs,
  and is wrong about what it matches. So the confirmation the rule above
  requires is not specific to continuations; it is the only thing that
  catches this family at all. Where a pattern needs an escape, express it
  without one:

  | Instead of | Write |
  |------------|-------|
  | `\d` | `[0-9]` |
  | `\w` | `[A-Za-z0-9_]` |
  | `\b` at each end | `(?<![A-Za-z0-9])` and `(?![A-Za-z0-9])` |
  | a literal backslash | `chr(92)` |

  A pattern holding no backslash cannot lose one. The two losses differ in
  what they say: a vanished `\b` still compiles and still matches, so the
  check reports confidently over a wider set than intended, while a
  degraded `\d` announces itself only as a `SyntaxWarning` on stderr —
  which a check whose pass condition reads stdout will not surface
- A violation count far larger than expected on a tree believed clean MUST
  be triaged as a possible defect in the check before it is worked as a
  backlog of fixes. A rule can be wrong rather than under-enforced

The first of these is itself mechanically checkable: every check embedded
in a rule file MUST compile when extracted the way a reader extracts it.
Adapt `ROOTS` to the files that carry the rules — the template tree in
this repository, the context file in a generated project:

```bash
py - <<'EOF'
import pathlib, re

# The files that carry rules and their checks.
ROOTS = ["templates"]

# A shipped check is a heredoc inside a fenced block. The fence may be
# indented under a list item, and a renderer strips that indent -- so
# strip it here too, or the extracted body will not compile.
FENCE = re.compile(r"^([ ]*)```")
found, broken, scanned = 0, [], 0
for root in ROOTS:
    for path in sorted(pathlib.Path(root).rglob("*.md")):
        scanned += 1
        lines = path.read_text(encoding="utf-8").splitlines()
        n = 0
        while n < len(lines):
            opened = FENCE.match(lines[n])
            if not opened:
                n += 1
                continue
            indent, body, n = len(opened.group(1)), [], n + 1
            while n < len(lines) and not FENCE.match(lines[n]):
                line = lines[n]
                body.append(line[indent:] if not line[:indent].strip() else line)
                n += 1
            n += 1
            text = chr(10).join(body)
            if "<<'EOF'" not in text:
                continue
            found += 1
            marker = chr(10) + "EOF"
            source = text.split("<<'EOF'", 1)[1].split(marker, 1)[0]
            source = source.lstrip(chr(10))
            try:
                compile(source, str(path), "exec")
            except SyntaxError as error:
                broken.append((path, error.lineno, error.msg))

print("markdown files scanned: %d" % scanned)
print("embedded checks found: %d" % found)
print("checks that do not compile: %d" % len(broken))
for path, lineno, msg in broken:
    print("%s: extracted body line %s does not compile: %s"
          % (path, lineno, msg))
if not found:
    print("no embedded checks found; the extraction pattern drifted")

raise SystemExit(1 if broken or not found else 0)
EOF
```

Pass condition: the first two counts MUST be non-zero and the third MUST
be zero; anything printed after them names a check that does not compile.
The scanned count is what makes the found count readable — twenty checks
found across two hundred files and twenty found across two are different
readings, and without the corpus the second is indistinguishable from an
extraction pattern that has drifted onto a subset.

A companion locator for the continuation rule. It cannot detect a
continuation that was already lost — once joined, the line is
indistinguishable from one written that way — so it reports where the
risk is instead, and the list is what gets read against the source:

```bash
py - <<'EOF'
import pathlib, re

# The files that carry rules and their checks.
ROOTS = ["templates"]

# A continuation only matters where a reader copies the block and runs
# it. The languages a check is written in are the corpus; a fenced
# workflow or a table of output is an example, and a line ending in a
# continuation is valid where it sits.
CHECK_LANGUAGES = ("bash", "sh", "python", "py")

FENCE = re.compile(r"^([ ]*)```(\w*)")
blocks, inspected, risky = 0, 0, []
for root in ROOTS:
    for path in sorted(pathlib.Path(root).rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        n = 0
        while n < len(lines):
            opened = FENCE.match(lines[n])
            if not opened:
                n += 1
                continue
            indent, language = len(opened.group(1)), opened.group(2)
            n += 1
            blocks += 1
            runnable = language in CHECK_LANGUAGES
            inspected += 1 if runnable else 0
            while n < len(lines) and not FENCE.match(lines[n]):
                line = lines[n]
                body = line[indent:] if not line[:indent].strip() else line
                if runnable and body.rstrip().endswith(chr(92)):
                    risky.append((path, n + 1))
                n += 1
            n += 1

print("fenced blocks found: %d" % blocks)
print("blocks in a check language: %d" % inspected)
print("lines ending in a continuation: %d" % len(risky))
for path, number in risky:
    print("%s:%d" % (path, number))
if not blocks:
    print("no fenced blocks found; the extraction pattern drifted")
elif not inspected:
    print("no block is in a check language; the language filter drifted")

# The continuation count is a reading, not a verdict: the check cannot
# tell a deliberate continuation from an accidental one, and a person
# reads the lines against what was written. An empty corpus is a verdict,
# because it means the extraction drifted rather than the tree being clean.
raise SystemExit(1 if not blocks or not inspected else 0)
EOF
```

Pass condition: the command reports how many fenced blocks it found, how
many of those are in a language a check is written in, and how many lines
in that subset end in a continuation, then lists them. A non-zero
continuation count is not a failure — it is the set to read against what
was written. Zero on either of the first two counts is a failure: the
first means the fence pattern drifted, the second means the language
filter did, and neither means the files carry no checks.

The two counts are separate because the narrowing is deliberate and has
to stay visible. The check's subject is a line a reader might copy and
run, so a fenced workflow or a table of output is not in scope and a
backslash in one is valid where it sits — this check reported two such
lines inside a documented `run:` step for as long as it scanned every
language. Collapsing the two counts into one would hide the exemption,
and an exemption nobody can see is indistinguishable from a pattern that
quietly stopped matching.

---

## A check reports the moment it ran

[ID: quality-gates-check-timing]

`quality-gates-check-runs` requires that the check be run. It does not
say when, and a check reports on the state at the instant it executes.
Run before the change it gates, it reports the state before the change,
and nothing in that output distinguishes it from a run against finished
work: the clean result is evidence about a tree that no longer exists.

- Run a check AFTER the change it gates, never before. Where the check's
  subject is committed history, "after" means after committing rather
  than after editing — a branch whose work is staged and uncommitted
  reports exactly what a compliant branch reports
- A check that repairs, rewrites or otherwise alters its own subject
  answers differently on its second run, and only the first invocation
  is honest. Fix it to inspect without mutating; until then, every
  negative control of it MUST specify a single fresh invocation, or the
  control measures the repair rather than the defect
- State the moment where the operator reads the result — in the pass
  condition beside the command, not only in the prose around it. A pass
  condition that enumerates the causes of an empty result MUST include
  "the change is not in the subject yet", which is the cause a reader
  hits while writing the change rather than after it
- The failure is silent by construction, so it does not show up as
  flakiness. A gate that passed early and a gate that passed on the
  finished work are the same line of output, and the second run that
  would have contradicted it is the run nobody makes

---

## A check selects its subject, and the subject can move

[ID: quality-gates-check-selection]

A check can run, exit zero and report on the wrong thing. Two ways: it
picks an arbitrary member of a set it assumed had one element, or it
filters on a property that the violation itself changes. Both degrade
silently, and in both the change that breaks the check lives in a
different file and touches neither the rule nor the command, so no
reviewer of that change has reason to look.

- A check MUST select its subject, not a count or a position. Selecting
  "the latest", "the most recent", the first line or index zero is correct
  only while exactly one instance of the thing exists. Derive the selector
  from what is under test — the commit, the ref, the artifact name — never
  from ordering
- A check MUST NOT filter on a property that the violation it detects can
  change. Where a tool classifies artifacts (text or binary, tracked or
  ignored, parseable or not) and the check selects on that classification,
  state what a violating artifact's classification becomes, and add a
  second command covering the reclassified case with its own pass condition
- A check that has never failed, on a rule that was never enforced, MUST be
  treated as blind until a planted violation makes it fail (see
  `quality-gates-check-runs`). This is the only evidence that separates a
  satisfied check from one whose filter no longer matches anything

Selecting a CI run by recency is correct until a second workflow is added
for an unrelated reason, after which the check reports whichever finished
last and hides the other — a contributor can read a green scan and call a
red build good. Selecting it by the commit under review stays correct at
one workflow or five.

A line-ending gate that counts index entries classified as CRLF has the
sharper version of the problem. A file that acquires a NUL byte is
reclassified as binary, which stops it being normalised — the violation —
and simultaneously stops it matching the gate's own filter. The count
stays at zero for exactly as long as the defect is present, and starts
failing only once someone fixes it. The second command covers the
reclassified population, excluding the paths that are legitimately binary.

---

## Convention-as-test

[ID: quality-gates-convention-as-test]

A specific shape of `quality-gates-pair-check`: when a convention takes
the form "every record satisfying property X MUST share derived
artifact Y", its check is a test that enumerates the X-satisfying
records and asserts Y-equality across them.

- A written-down "if X then Y" invariant MUST be encoded as a test when
  Y is mechanically comparable. The test enumerates every record
  satisfying X and asserts they share Y. Examples: entries sharing a
  canonical product URL MUST share their generated image file; build
  outputs in one locale MUST share a glossary file
- The test gates the invariant at commit time. A prose convention is
  forgotten and the next divergent record lands undetected; the test
  fails loud, naming the pair that broke it
- This applies only to mechanically checkable invariants. Conventions
  that genuinely cannot be tested (subjective code style, prose tone)
  stay declarative

---
