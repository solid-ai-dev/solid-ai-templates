# Base — Quality Attributes

[ID: base-quality]

How code is designed, kept clean, swept and checked.

## Principles

- Keep one authoritative representation of each piece of knowledge (DRY);
  the third copy is a bug
- Choose the simplest solution a stated requirement justifies (KISS)
- Build what is needed now, never for a hypothetical requirement (YAGNI)
- Record beside every deferral the concrete condition that reopens it
- Delete a path in the same commit when probing real data shows it never
  fires; git history keeps it

## Revisit triggers

[ID: quality-revisit-trigger]

- Reopen a deferral in the change whose step fires its trigger, as a
  superseding record or a ticket carrying the evidence (MUST)
- Search the records for triggers naming a piece of state before changing
  it
- Write triggers in one consistent, greppable form
- State what would detect each trigger: a scheduled check, a failing gate,
  or a person looking
- Re-verify a trigger against the system, not by re-reading its record,
  and state that check beside the condition

## Architecture

- Keep editable content in a data directory, never in source modules
- Compute derived counts and statistics from the data; never hardcode them
- Remove unused modules, assets and data files promptly

## Naming

- Name a function with a verb, a class or module with a noun, and a boolean
  with `is`, `has` or `can`
- Rename a name that needs a comment to explain it
- Name a function so a call site reads without its body
- Use a single-letter name only for a loop counter or an ecosystem
  convention such as `err` or `e`
- Abbreviate only what the domain abbreviates universally (`url`, `id`)
- Use the same name for the same concept in every module
- Name a public enum member, CLI flag or result discriminator for the
  capability it offers, never the library behind it: `Transport.HEADED`,
  not `Transport.PLAYWRIGHT` (MUST). A private symbol MAY name its library

## Complexity

- Keep cognitive complexity at or under 15 per function, enforced by the
  analyser `base-<language>-tooling` binds
- Nest at most three levels; use guard clauses and early returns
- Prefer a positive condition (`if is_enabled`) to a negated one
- Replace a boolean flag that selects behaviour with an enum or two named
  functions
- Replace a flag that selects how many rules apply with an operation
  returning findings, each naming its rule, plus a guard that raises when
  the findings are not empty
- Name every magic number and magic string as a constant
- Size a numeric threshold from the measured distribution of its quantity
  (p95, p99, maximum legitimate), and name the data source in the
  constant's docstring

## Dependencies

- Keep the module graph acyclic; break a cycle with a third module or an
  interface, never with a divergent local copy
- Keep coupling shallow: a change inside one module MUST NOT require
  changes in unrelated modules
- Talk only to direct dependencies, and keep together what changes together
- Reach a heavy, native or platform-limited dependency through one module
  that owns its import and names the install command when it is missing
- Import the package without that extra in one CI leg (MUST)
- Declare a directional import ban where one part of the tree must not
  import another, and check it

```bash
pre-commit run find-import-bans --all-files --verbose
```

Pass condition: the bans-declared and modules-inspected counts are above
zero and `import-ban violations` is zero. Each ban is a
`--forbid IMPORTER:IMPORTED` argument; `not applicable` means none is
declared.

## Hierarchies

- Never declare a variadic parameter (`*args`, `**kwargs`) on an abstract
  or overridable operation
- Give a capability its own name where a class part-way down a hierarchy
  offers what its own subtypes must not; never widen the shared operation
- Check overrides with a strict type checker's override rule, bound in
  `base-<language>-tooling`, and shrink its variadic findings first
- Where that checker is frozen, keep a contract test walking every
  concrete class: each override keeps its member kind and first parameter,
  only appends parameters, and declares no variadic
- Read each override through `inspect.getattr_static`, unwrapping
  `staticmethod` and `classmethod` by hand

## Errors

- Validate input at boundaries and fail at once on invalid state
- Read a value from its source-of-truth field, and raise when the field is
  missing; never fall back to a value derived from a slug, name or hash
- Bound every wait on another thread, process or connection, report why it
  gave up, and check the worker's liveness as well as the deadline
- Derive every deliberate raise from one package base, each type also from
  the built-in its site raised before
- Split an error type only where a caller could act differently
- Keep a test that walks every raise in the package and fails on one
  outside the hierarchy
- Never let a caller-side input filter stand in for a precondition: widen
  the filter, or assert the precondition inside the function

## Deprecation and renames

- Deprecate a public symbol, naming its replacement, before a later change
  removes it
- Deprecate every part of one call site together, such as a method and its
  keyword arguments, or break the whole call; never alias the outer name
  alone
- Keep a one-line shim under the old name when widening a return type, and
  remove it in a later change
- Retire a concept by sweeping every surface that still instructs its use,
  tickets and plans included, until a search returns only historical
  records

## Module structure

- Build an internal module ready for extraction: inject host values as
  constructor parameters, and give it its own public API, README, tests and
  requirements (MUST)
- Wrap a library in a thin CLI; never make the CLI the product
- Split an oversized module into a package behind its existing import path,
  re-exporting through `__init__`, and leave the test suite untouched as
  the regression oracle
- Split along a cohesive seam, each submodule importing only earlier
  stages and never the package `__init__`
- Keep constants beside the functions that use them
- Reshape first, then split mechanically, where a split would change a
  signature
- Search the suite for code that reads module identity before splitting
- Run the static gates (undefined names, an import smoke check, test
  collection) before the full suite
- Prove a split neutral with the untouched suite and a byte-identical
  output diff

## Ports and variants

- Port a function into another language byte for byte: the same operation
  order, character classes and edge cases, citing the original
- Decompose a ported procedural script into small modules an orchestrator
  dispatches on a declared type
- Prefer a per-configuration flag with a safe default to a global
  auto-detect, unless inputs partition cleanly on a measurable signal

## Library output

[ID: quality-library-output]

- Never write to the host's standard output or error from a library, and
  never configure logging beyond the library's own logger (MUST)
- Make the library's logger injectable, falling back to its module logger
- Check the silence in a fresh process; a test runner's handler hides the
  default

## Encoding and line endings

- Encode every committed file in UTF-8, with LF line endings (MUST)
- Keep identifiers ASCII (MUST); comments, docstrings, strings and
  documentation carry no charset restriction

```bash
pre-commit run check-ascii-identifiers --all-files --verbose
```

Pass condition: the inspected count is above zero and
`non-ASCII identifiers` is zero. The hook reads Python; `not applicable`
means the project tracks none.

- Set a program's output encoding explicitly, and pin its line ending where
  another program reads the output. In Python, at the entry point:
  `sys.stdout.reconfigure(encoding="utf-8", newline="\n")`
- Commit an `.editorconfig` and a `.gitattributes` with `* text=auto`,
  adding `eol=lf` for hard LF
- Mark a text path exempt from LF with `-text` in `.gitattributes`
- Let a linter format on save; keep manual style rules to a minimum

```bash
git ls-files --eol | awk -F'\t' '
  $2 ~ /\.(md|py|ya?ml|json|txt|toml|cfg|ini|sh|sql|css|js|ts)$/ {
    seen++
    if ($1 !~ /^i\/lf/) { bad[++n] = $0 }
  }
  END {
    printf "text files inspected: %d\n", seen + 0
    printf "files not filed i/lf: %d\n", n + 0
    for (i = 1; i <= n; i++) print "  " bad[i]
  }'
```

Pass condition: the inspected count is above zero and the count of files
not filed `i/lf` is zero. It matches "not `i/lf`" so a file git filed as
`i/-text` for a stray carriage return is caught too.

- Refresh a checkout older than `.gitattributes` by rewriting its files or
  re-cloning; the index being right does not make the checkout right

```bash
eol() { git ls-files --eol | awk -F'\t' "$1"; }
total=$(eol '$1 ~ /^i\/lf/' | wc -l)
drifted=$(eol '$1 ~ /^i\/lf/ && $1 !~ /w\/lf/' | wc -l)
echo "text files tracked: $total"
echo "checked out against a different convention: $drifted"
eol '$1 ~ /^i\/lf/ && $1 !~ /w\/lf/ { print "  " $2 }'
if [ "$total" -eq 0 ]; then
  echo "no text file reached; the extension or index pattern drifted"
  exit 1
fi
[ "$drifted" -eq 0 ] || exit 1
```

Pass condition: the first count is above zero and the second is zero;
either failing exits non-zero.

## Comments

- Prefer code that needs no comment; comment only intent the code cannot
  express
- Re-verify a comment explaining why something is safe whenever the code
  is next read
- Never cite a ticket, PR or ADR number in a code comment, docstring or
  commented configuration; state the substance (MUST NOT)
- Name a source (author, year, method) where non-obvious or scientific
  logic needs one (MAY)
- Enforce the citation ban with a test that greps comments, docstrings and
  commented configuration for `#\d+` and `ADR\s*\d+`
- Audit the citations to an item when closing or superseding it, and fix
  each one left pointing at it

```bash
rg -n "#<number>\b"
```

Pass condition: no line it prints still points at the closed item.

- Place a block comment directly above the item it documents: never to
  the right of code, tool directives excepted, and never separated from the
  item by a blank line (MUST)
- Separate comment-plus-item groups with one blank line; a comment opening
  a block or bracket needs none above it
- Wrap comment prose to the project's line-length limit, in commented
  configuration too

```bash
pre-commit run check-comment-layout --all-files --verbose
```

Pass condition: the files-checked count is above zero and
`layout violations` is zero. The hook reads Python, tracked and untracked
but never ignored; whether a comment sits above the right item takes a
person.

## Debug code

- Commit no debug output (`print()`, `console.log()`) and no hardcoded
  breakpoint
- Delete commented-out code
- Gate debug tooling behind a flag or environment variable, off by default

### Probe scripts

- Write a probe, a throwaway script that measures data or behaviour,
  rather than guess
- Name a probe as temporary (`probe_*.py`, `scratch_*.ts`), and delete it
  before the commit that uses its findings (MUST)
- Keep findings in source comments, decision records or docs, never in
  the probe
- Use a probe for a uniform edit across many call sites; review the diff,
  then delete the probe

### Scripts directory

- Keep a file under `scripts/` only while a documented command invokes it,
  CI runs it, or such a file imports it; delete it otherwise (MUST)
- Hold `scripts/` to the review and formatting rules of shipped source

```bash
pre-commit run find-unreferenced-scripts --all-files --verbose
```

Pass condition: the scripts-inspected and files-searched counts are above
zero and `unreferenced` is zero. `--dir` names the directory;
`not applicable` means it holds no script.

## Rejected mechanisms

[ID: quality-rejected-mechanism-sweep]

- Grep the codebase for a construct a comment records as not working,
  before moving on: `grep -rn '<the construct>' <source root>`
- Read every hit as a suspected instance of the same defect, not a style
  question

## Exemption docs

[ID: quality-exemption-doc-duty]

- Treat changing what a check exempts as a documentation edit: sweep the
  documents for the check's name and re-read every hit
- Sweep for the name a document would use, not only the source identifier
- Point prose at the exemption constant rather than enumerate it (SHOULD)
- Write an enumeration without a cardinal in front of it

```bash
# The check whose exemptions are changing, named as a document would
# refer to it.
module="<check-name>"

scanned=$(git ls-files '*.md')
echo "documents scanned: $(echo "$scanned" | grep -c .)"
naming=$(echo "$scanned" | xargs grep -l "$module")
echo "documents naming ${module}: $(echo "$naming" | grep -c .)"
echo "$naming"
```

Pass condition: the scanned count is above zero, and every listed document
is read against the new exemption set. A naming count of zero is a real
answer.

## New constraints

[ID: quality-constraint-corpus-sweep]

- Run a new constraint (a rule, a check, a tightened bound, a narrowed
  exemption) against the existing corpus before it merges (MUST)
- Record in that change where the sweep looked, how many items it
  inspected, how many violate, and what was done (MUST)
- Name what a partial sweep left out (MUST)
- State whether the violations were fixed or frozen; a freeze names each
  instance, gates new work and reports an instance that stops violating
- Run and record the sweep on an immutable corpus too, such as decision
  records or released changelog sections, and state the boundary the
  constraint binds forward from
- Record a constraint shipped without a check as such, with the instances
  already known

## Destructive operations

[ID: quality-destructive-ownership]

- Delete, truncate, overwrite or kill only what the operation can prove it
  created: process ancestry, a key scheme, a filename prefix, a marker file
  or an ownership tag; never a path, a configuration value or a file
  extension
- Find nothing where the proof is unavailable: no error, no prompt, no
  guess
- Validate the input as well: reject an empty configuration value, and
  match the key scheme
- Apply this to every reaper: a cache clean, an output-directory clear, a
  log rotation, a temp-file sweep

```
match on ".html"              wrong directory -> README.html deleted
match on "[0-9a-f]{16}.html"  wrong directory -> nothing matched
```

## Expensive computations (if applicable)

[ID: quality-expensive-compute]

A step built on an iterative numerical routine (a fixed-point solver, an
optimizer) or on a memory-heavy intermediate fails in ways that produce a
plausible answer rather than an error. These rules keep the failure loud
and the cost paid once.

### Verify convergence — escalate, then fail loud

- A routine that exposes a convergence flag but does not force the caller
  to read it MUST be wrapped in one helper that checks the flag. An
  unconverged result handed back as if it were valid feeds a wrong number
  straight downstream
- On failure, escalate through progressively stronger and slower
  stabilization strategies, cheapest first, before raising a descriptive
  error naming what would not converge. The ladder fires ONLY on
  non-convergence, so the path that already converges is untouched
- Keep the ladder unit-testable without the heavy engine: each
  stabilization step is a small function, the driver is pure
  orchestration, and a stub with scripted per-attempt convergence
  exercises every rung

### An output-changing approximation is opt-in and off by default

- A speed knob that shifts the numbers (a lower-rank approximation, a
  coarser grid) MUST default off, so the canonical output is never
  silently perturbed
- Carry it as a per-run field in the same single source of truth as the
  rest of the run's parameters, so a run that needs it is self-reproducing

### Size the budget to the box; spill or refuse, never OOM

- A memory-heavy step detects its real budget (env override → container
  cgroup limit → physical RAM, scaled for headroom) rather than assuming
  a fixed library default
- Estimate the large intermediate up front: keep it in RAM while it fits,
  stream it to a disk scratch path beyond that, refuse past a hard
  ceiling. A diagnosable error beats an OOM crash
- The scratch path MUST be real disk, not a RAM-backed tmpfs

### Persist the reusable intermediate, not just the scalar read off it

- When already paying for an expensive computation, persist its reusable
  internal state to a checkpoint, not only the scalar this caller needed.
  Discard the state and the next question about the same input forces a
  full re-run
- Make it opt-in (a checkpoint-path parameter, default off) so cheap
  callers pay nothing, and store the checkpoint with the other
  regenerable artifacts (gitignored)
- Validate the round-trip once on a small case before trusting a long
  batch to it — including any wrapper or proxy layer around the engine,
  which can silently swallow the checkpoint parameter

## Calibration discipline

[ID: quality-calibration]

When a tool is calibrated against reference data (test fixtures with
known-correct outputs, benchmark expected results, eval data, decision
thresholds), the calibration is silently invalidated by suspect ground
truth, by a threshold tuned to mask a broken measurement, and by
reference values produced by the same actor that runs the tool. The
rules below govern that, and what a calibrated pipeline may then emit:
a value it cannot justify is worse than a gap.

### Ground truth comes from raw artifacts, not suspect data

- When calibrating a pipeline against existing committed data, verify
  the data was not produced by an earlier version of the same pipeline
- If it was, and the pipeline has known or suspected bugs, the
  committed data is NOT ground truth — calibrating against it bakes
  the existing bugs into the new gate
- Build the calibration set from raw artifacts (source images, raw
  exports, captured fixtures), recording the verified value alongside
  each entry
- A small hand-built reference set from raw artifacts beats a large
  set carried over from a suspect pipeline
- When a reference set flips from tool-seeded to independently verified
  values (the de-circularization above), grep the codebase in the same
  change for comments, guard conditions, and thresholds whose rationale
  cites the OLD data, and re-verify each against the new ground truth —
  or file an issue per survivor. The reasoning citing the stale values
  keeps steering the code long after the data is corrected; the sweep is
  one grep at a well-defined moment (the ground-truth-flip change)

### Honest absence beats a recovered wrong value

- When a fix flips an extractor from a wrong value to an honest absence
  (`None`, empty, no-reading) because the source genuinely has no data
  at that point, the absence is the correct output — not a regression
  to recover
- Update the reference / ground-truth framing in the same change: any
  prior expected value at that point MUST be re-marked as extrapolation
  past the data, never carried forward as a hit-this target the
  extractor "should" reach
- Distinguish the two absences in logs and reference notes: `None`
  because the extractor failed (a defect to fix) versus `None` because
  the source carries no value there (the correct answer) — the two
  demand opposite responses, and conflating them sends a maintainer to
  "fix" a correct absence

### Report a derived quantity only where it is well-defined

Distinct from the absence rules above, which cover a source that carries
no value. Here the value is computable and the arithmetic succeeds — the
condition that gives the result meaning is what fails.

- A derived quantity is often well-defined only under a condition (a
  non-zero denominator, a minimum sample size, a non-degenerate input).
  Report it only where that condition holds
- Where it does not hold, leave the cell empty — not zero, not a
  placeholder, not the condition-violating value. An empty cell states
  "undefined here"; a number computed outside its domain is
  indistinguishable from a measurement and pollutes every downstream
  aggregation
- The check belongs at the point of emission. A consumer cannot recover
  the condition from the value alone, which is exactly why the artifact
  must not carry it

### A user-visible artifact takes its bar from the strictest consumer

- When a derived or extracted artifact feeds several consumers of
  differing strictness AND is itself user-facing (rendered or displayed,
  not only an internal input), its acceptance bar is set by the strictest
  **visible** consumer
- Do NOT loosen it to match a coarser downstream consumer, and do NOT
  lower it for throughput. Coarsening the acceptance metric to a bucketed
  score, or dropping a label only the visible artifact reads, is correct
  for the score and corrupts the table a user looks at
- The compatible throughput lever is honest gaps, not a looser bar: an
  ambiguous cell is blanked per the rule above, never emitted wrong

### Thresholds move, not the measurement

- When a measurement and a threshold disagree, the threshold is the
  cheaper thing to change — but ONLY after the measurement is verified
  sound
- Order of operations on disagreement: (1) verify the measurement
  against an independent check, (2) tune the threshold if the
  measurement is sound, (3) change the measurement implementation
  ONLY when steps 1 and 2 fail to resolve the disagreement
- A threshold picked from theory and never validated against data is
  not a calibrated threshold — it is a guess; tuning it against the
  data on first disagreement just hides the original guess
- This rule applies wherever measurements meet thresholds: CI quality
  gates, performance budgets, ML decision boundaries, extractor
  agreement scores

### Reference data MUST carry provenance

- Each entry in a reference set MUST record `source: agent | user |
  external` (who produced the value) and `verified: true | false`
  (whether a human has reviewed it)
- An agent MAY produce reference values to speed calibration, but
  MUST set `source: agent` and `verified: false` until the user
  reviews — the user MAY veto, replace, or accept; accepting flips
  `verified: true`
- Calibration metrics computed against the reference set MUST report
  a coverage caveat alongside the headline numbers (e.g.
  "verified: 12/40"), so unverified reference data cannot silently
  dominate the metric
- Synthetic test inputs (faker-style data, generated fixtures) are
  out of scope — this rule covers reference *outputs* compared
  against tool *outputs*, not test inputs

### Diagnose before tuning

- Before changing a parameter whose value was set by a calibration
  step or carries a tuning rationale, first PROBE to confirm the
  parameter is the actual constraint — do not tune-and-see
- Trace the value where it is computed and read the real intermediate
  inputs from a real sample (a probe script, or a trace-not-propose
  investigation), never a synthetic case
- Tuning is valid once the probe shows the parameter is genuinely the
  constraint; the wasteful move is changing code on "this might help"
  without probing, which burns time and risks regressing unrelated
  calibrated anchors

### A detector's precision is not its cost

- A false-positive rate says how often the verdict is wrong and nothing
  about what a wrong verdict destroys. A heuristic that gates an
  expensive fallback MUST be evaluated on both, because a detector with
  an excellent rate can still be unshippable
- Ask first whether a positive verdict discards the cheap result or
  holds it. Where the cheap tier returns a sentinel instead of its body,
  the result is destroyed at the moment the heuristic fires, and the
  fallback's availability becomes part of the heuristic's correctness
  rather than an operational detail
- Ask what the system returns when the fallback cannot run — an optional
  dependency absent from a default install is the common deployment, not
  the rare one. Where the answer is "nothing", the heuristic's failure
  mode is data loss, and that is not the precision bar of a heuristic
  which merely costs time
- Prefer preserving the cheap result, so an unavailable fallback
  degrades to a result plus a warning rather than to nothing. That is
  also what returns the question to one about latency, where the
  false-positive rate is the right measure
- No amount of tuning finds this. It is a property of the surrounding
  control flow, and it can invert a decision that looked like a
  threshold problem

### A spike reports the corpus it did not have

- A spike that cannot clear its own evidentiary bar with the available
  data records the corpus gap as its finding, rather than lowering the
  bar to produce a shippable answer
- A rule that survives every case in a set the rule's own author wrote
  is fitted to that set, not measured against it. Count the cases that
  were captured independently of the rule; that count is the evidence,
  and the rest is illustration
- "The evidence does not exist yet, and here is exactly what would have
  to be captured" is a deliverable. State that it is one, because it
  reads as a non-answer otherwise

### Calibration aids MUST NOT depict the system's own output

- Any artifact that informs a human-verifies-machine signal (a human
  reading values from a source document, code review against a generated
  patch, audit grading against a candidate report) MUST render only the
  reference data plus the maintainer's reading guides
- The candidate output goes in a separate artifact, opened only after
  the independent reading is captured — surfacing it alongside the
  reading task biases the reading toward the candidate and turns the
  calibration into a self-confirming loop
- Name the candidate-output artifact distinctly (`*-overlay.png`,
  `*-trace.svg`, `*-prediction.md`) so it cannot be confused with the
  reading aid
- Comparison views opened AFTER the independent reading is captured
  (diff viewers, side-by-side dispute resolution) are out of scope —
  they are downstream of the signal and do not bias it

## Check trust

[ID: quality-cross-validation]

### Tools

- Confirm a validation, scraping, migration or codemod tool is correct
  before acting on its output in bulk
- Treat a physically implausible output as a tool defect: fix it, re-run,
  then apply
- Cross-check an independent source before overwriting stored data with a
  source that looks wrong

### Distinguish source-silent from source-says-false

- A stored default (e.g. `absent boolean = false`) and source
  silence (the source did not mention the field) are NOT the same
  thing — treating them as equivalent produces a flood of
  false-positive mismatches that bury real errors
- The extractor MUST return a field ONLY when the source
  affirmatively states it
- The differ MUST compare a field ONLY when present on both the
  stored and source sides — source-silence skips comparison, never
  becomes a confirmed value
- This keeps stored-default conventions (`absent = false`,
  `null = unknown`) intact while making cross-validation meaningful
- The trap is non-obvious: the stored-default convention and the
  verification semantics pull in opposite directions, and the naive
  implementation looks correct until run against real data

### Self-match

- Test a check whose scan can reach its own source: run it from a tree with
  and without that source; the inspected count rises and the findings stay
  identical
- Constrain the scan to where the pattern can legitimately appear, such as
  the comment half of a line, rather than excluding a path
- Name what an unavoidable exclusion excludes, and why (MUST)
- Constrain by the narrowest property separating a real occurrence from a
  quoted one

### Verdicts and readings

- Report what a judgement check inspected and found, in the record a
  person reads (MUST)
- Report that a check tied to a moment does not apply, with exit status 3,
  when the moment is not in progress; detect the moment, never the empty
  input (MUST)
- Refuse, as a finding and never as exit 3, when the command that should
  yield a comparison baseline yields none, and print the baseline on its
  own line (MUST)
- Reach an automatic verdict on every threshold a check declares; the
  judgement is what remains (MUST)
- Read that threshold from the check's pass condition, never from a sample
  of its output (MUST)
- Say which counts carry the verdict and which are for a reader, where a
  check carries both (MUST)
- Record beside each judgement disposition what takes a person (MUST)
- Report what a check saw whatever its verdict (MUST)
- Carry a shipped check's verdict in its exit status, and prove the status
  separates a planted violation from a clean tree (MUST)
- Say beside a check whose verdict takes a person what that judgement is
- Keep exit 3, the check answering this run, apart from a skip a person
  records in advance
- Separate readings, verdicts and not-applicable answers in a run's summary
  (MUST)
- Never wire a governance signal as a build gate where the project's own
  rules oblige the change that trips it (MUST NOT)
- Never weaken the rule behind a check to make it green or quiet

## Enforcement

- Enforce these conventions through the gates: editor, pre-commit, CI
- Make a generator emit output that passes the linters natively; a needed
  `lint --fix` is a generator bug (MUST)
- Merge to `main` only with passing tests
