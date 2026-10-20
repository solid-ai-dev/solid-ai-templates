# Base — Quality Gates

[ID: base-quality-gates]
[DEPENDS ON: templates/core/quality.md, templates/core/git.md]
[DEPENDS ON: templates/core/testing.md, templates/core/config.md]

What to gate, how to build the check, how to adopt a gate on existing
code, and how to read and change one afterwards. When gates run, and
against which thresholds, is the project's choice.

## Paired checks

[ID: quality-gates-pair-check]

A stated constraint without its check is decorative: a violating artifact
looks like a clean one. A constraint a generated project inherits carries
that risk furthest.

- Name the agent-runnable check of an output constraint that is
  mechanically checkable: the command to run and the pass condition (MUST)
- State the check next to the rule, so the two travel together into every
  generated artifact
- Put the command in a fenced block; prose carries the pass condition
  beside it
- Write the command first; a sentence describing an action is not a check
- Report how many checks a tool could not see, not only how many it ran
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

Find a check stated outside a fence. Match over the paragraph, not the
line, because prose wraps:

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

- Add a literal to `PHRASE` or `VERDICT` only together with the check in
  the project that motivated it
- Control any edit to either both ways: a check stated in prose is
  reported, and the same check inside a fence is not

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
- Apply the same move elsewhere: a flaky integration test to a contract
  test, a tutorial example to a CI-verified one, a manual smoke test to an
  automated regression

## Running a check

[ID: quality-gates-check-runs]

### Reporting

- Run a check in the form it ships before merging the rule: extract it
  from the committed file and execute it
- Run a check whose subject is the change under review in the environment
  that builds its tree; `base-git` states what that run has to show
- Report what a check inspected, not only what it found; the test-suite
  form of this rule is `testing-negative-assertion-coverage`
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
- Ship a check against a synthetic subject with a fix that has no
  observable effect on the current tree
- Demonstrate the defect on the fixing branch where the tree can be put in
  the failing state

### Extraction

- Never indent a fenced check deeper than the first indentation of its
  code; put it flush and point to it from the step
- Prefer a quoted heredoc to an inline `-c` string, and never write the
  heredoc opener itself in prose
- Confirm that a line continuation survived into the committed file
- Fold a command onto one line, or bind its parts to shell variables,
  rather than continue it (SHOULD)
- Build an exact backslash in quoted text with `chr(92)` rather than
  transcribing it
- Write patterns without backslash escapes:

  | Instead of | Write |
  |------------|-------|
  | `\d` | `[0-9]` |
  | `\w` | `[A-Za-z0-9_]` |
  | `\b` at each end | `(?<![A-Za-z0-9])` and `(?![A-Za-z0-9])` |
  | a literal backslash | `chr(92)` |

Every embedded check MUST compile when extracted the way a reader extracts
it. Adapt `ROOTS` to the files that carry the rules:

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
The scanned count shows the corpus the found count covers.

This locator reports where a continuation could be lost. It cannot detect
one already lost, so read its list against the source:

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

Pass condition: it reports the fenced blocks found, those in a check
language, and the lines among them ending in a continuation, then lists
them. A non-zero continuation count is a list to read, not a failure. Zero
on either of the first two counts is a failure: an extraction drifted.

## Check timing

[ID: quality-gates-check-timing]

- Run a check after the change it gates, never before
- Where the check's subject is committed history, run it after committing,
  not after editing
- Fix a check that alters its own subject to inspect without mutating
- Until then, control it with a single fresh invocation
- State the moment in the pass condition beside the command
- List "the change is not in the subject yet" among the causes of an empty
  result

## Check subject

[ID: quality-gates-check-selection]

A check can exit zero and report on the wrong thing. The change that breaks
it usually lives in another file, so its reviewer has no reason to look.

- Select a check's subject by what is under test — the commit, the ref,
  the artifact name — never by recency or position
- Never filter on a property the violation can change
- State what a violating artifact's classification becomes, and cover that
  case with a second command and its own pass condition
- Treat a check that has never failed, on a rule never enforced, as blind
  until a planted violation makes it fail

## Gate scope

[ID: quality-gates-scope-agreement]

In a polyglot repo, or one holding captured fixtures, a gate breaks
silently three ways: the formatter walks the wrong files, the PR gate skips
work, and an aggregate job passes on skipped checks.

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

A gate that ran green over almost nothing looks like a real pass. Its scope
parameter is separate from the check, and review usually reads the check:

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

`security/devsecops.md` requires full history for the secret scan; that is
one instance of this rule.

### Environment independence

CI runs one clean environment. A check whose input depends on the
developer's environment passes there and fails on a laptop.

- Enumerate tracked files (`git ls-tree`, explicit imports), never the
  working-tree filesystem
- Gate a directory on an explicit anchor file, so local-only artifacts are
  filtered out
- Comment at the test any dependency on line endings, locale, timezone,
  case sensitivity or available binaries
- Run the gate locally on the development OS once per session where the CI
  matrix omits it

## Retrofitting a gate

[ID: quality-gates-retrofit-ratchet]

- Make a red gate green by exempting failing instances, never by narrowing
  what it evaluates: removing a compared field, disabling a strict sub-flag
  or loosening a matcher
- Retire an exemption whose remedy is known by applying the remedy
- Fix a genuine defect when the fix is small, instead of narrowing the check
- Clear a finding by changing the condition it describes, never the input
  the gate reads
- When a finding is false, fix the gate and record why in the same change

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

Pass condition: it prints the family, then a per-rule count. Zero means the
family is clear and every entry naming it is dead. It refuses an omitted
family, because both runs below exit clean:

```
ruff check --isolated --select N802,N803 src/   ->    0 findings, family clear
ruff check --isolated src/                      ->  366 findings, ruff defaults
```

- Where retiring an entry changes what code catches, accepts or returns,
  name the test that fails if the change goes too far
- Never count a suite that passed before the slice as that test
- Control the whole hierarchy: build every class with a value the
  interface cannot carry, and assert the declared error type comes back

### Site-local suppressions

- Suppress a finding that is wrong at one site at that site, never by
  adding the file to the freeze table
- Name the rule in every suppression, such as `# noqa: B017` or
  `//nolint:errcheck`, and put the reason directly above the line

Scan for a bare suppression:

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

Pass condition: it prints the files scanned and the suppressions found, then
`bare (naming no rule): 0`. Zero files scanned is a failure: the suffix list
misses the project's languages. Confirm a found count of zero, not accept it.

## Length-gate exemptions

[ID: quality-gates-length-bound-exemptions]

- Treat a length gate's exemption list as discovered, not derived
- Exempt a case only when something other than the author sets the count:
  a licence text, one label per line of code, a banner ruled top and
  bottom, a table of a published specification's fields
- Express the exemption as the shape that makes the count external, never
  as the file or directory that holds it
- Adopt in slices, and expect the list to grow while the corpus does

## Test edits

[ID: quality-gates-test-edit-boundary]

Tests are both the standard and files a change may edit. Strengthening
them needs no ceremony; weakening them redefines correct, and takes a
person.

- Strengthen the specification freely: add a test or tighten an assertion
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

Classify a change against the project's test root:

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

Pass condition: the not-pure-additions count MUST be zero. Anything printed
after the five counts lists the loosened changes, and a change keeps the
lenient path only while that list is empty.

On the base with a clean tree the check exits 3: no change is under review.
On the base with uncommitted work it exits 0 and asks for a commit.

The line counts are a reading, not a verdict. More lines removed than added
under the test root is the shape of a weakening shipped without its
replacement. A range total of zero means the check inspected nothing.

## Verdict reading

[ID: quality-gates-verdict-reading]

- Before acting on a failing verdict, decide whether the output is wrong,
  which the producer fixes, or the check is unsound for that input class,
  which a per-class fix to the check repairs
- Treat a passing gate as necessary, not sufficient, and name the artifact
  types a lenient gate leaves to a maintainer's review
