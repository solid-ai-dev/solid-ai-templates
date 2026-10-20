# Rationale: quality gates

Why the rules in `templates/core/quality-gates.md` say what they say. The
template states each rule as one instruction; the reasoning, the failure it
prevents and the worked examples are here, one heading per section ID.

---

## quality-gates-pair-check

A constraint that travels into a generated project, such as a template output
constraint inherited by a generated context file, carries the decorative risk
furthest: the project inherits the rule with no way to check it.

The fence makes a check extractable: a tool can count the checks a document
states, run them, and reconcile the two counts. A count over the parseable
form alone is complete only by assumption, and a green run coexists with a
violated rule whose check was typed in prose.

The detector matches over a paragraph because the project's own width rule
splits an inline check across two lines, and a line-scoped detector reads each
half as innocent. Two individually correct rules combine into a blind spot. A
phrase added to its vocabulary without an instance widens the false positives
and finds nothing.

---

## quality-gates-convention-as-test

A prose convention is forgotten and the next divergent record lands
undetected; a test enumerating the records fails loudly, naming the pair. For
example, entries sharing a canonical product URL share their generated image
file, and build outputs in one locale share a glossary file.

---

## quality-gates-staleness

Hand-written content reproducing tool output is not stale in the gate's sense:
it sits outside the gate's subject, so the gate reports nothing about it while
appearing to govern the file. One file can hold a generated section and a
hand-written block, and `--check` reports it in sync while the hand-written
half is wrong. Worked examples of a tool's output are the most common case.

A marker the file no longer carries matches nothing, so the text comes back
unchanged and `--check` compares it with itself; deleting a marker pair
freezes that block permanently. Without the gate a stale file looks identical
to a fresh one. The issue asking for a gate usually names only the generator's
path, which is why filters scoped to it are the common mistake.

---

## quality-gates-procedure-steps

An operator runs a procedure top to bottom. One step's gate fires, is fixed
and passes, which feels like the procedure checking the work, and the ungated
step is simply not done. A procedure with no gates invites care; one gate
invites trust in all of it. Re-cutting a published release to repair an
omitted step is worse than the gap, so the archive keeps the gap.

---

## base-quality-gates-tier-promotion

Promotion converts a silent failure into a measurable metric, so the eventual
fix lands against a regression target instead of working blind. When a fix
does not fit one session, measure first by elevating the case a tier.

---

## quality-gates-check-runs

A check that was written but never run is the decoration the pairing rule
exists to prevent, and it is worse than none because it looks enforced.

- **Inputs, not just findings.** A command that reached zero files and one
  that found zero violations print the same thing.
- **Every finding.** Stopping at the first turns one review into as many runs
  as there are offenders.
- **Controls.** A control tripping on a signature, an import or a missing file
  exercises the harness, not the check; the discriminating plant accepts a new
  parameter and ignores it. A layer in front, such as a parser or schema, can
  raise before the check runs, with the same exit status. A tool that writes
  only on a difference does nothing to a file already in its target state, so
  a clean run proves nothing until the subject is put in a state it must act
  on.
- **Landing.** A plant that matched nothing exits zero, so a missed plant and a
  blind check give identical evidence. Confirm it in the artifact the check
  reads: a listing from git's index does not see the working tree. An
  assertion that finds the planted value anywhere passes when a sibling
  already carried it. A revert that restores from the index discards unstaged
  work silently.
- **Preventive fixes.** A fix with no effect on the current tree prints the
  same output on both sides, so without a synthetic subject it is
  indistinguishable from a no-op, including to whoever later removes it.
- **Counts far above expectation** can mean the rule is wrong, not
  under-enforced.
- **Shipped checks.** A script copied out of a template stops following the
  rule when the rule changes upstream. A pinned hook runs the check the rule
  names, and the template carries the command instead of the code.

---

## quality-gates-check-timing

Run before the change, a check reports the state before the change, and
nothing in the output distinguishes it from a run against finished work. A
check that repairs its own subject answers differently the second time. The
failure is silent by construction: an early pass and a final pass are the
same line of output, and the run that would contradict it is the one nobody
makes.

---

## quality-gates-check-selection

Selecting a CI run by recency is correct until a second workflow is added for
an unrelated reason; then the check reports whichever finished last and hides
the other, and a contributor can read a green scan and call a red build good.

A line-ending gate counting index entries classified as CRLF is the sharper
case. A file that gains a NUL byte is reclassified as binary, which stops it
being normalised and stops it matching the gate's filter. The count stays zero
exactly while the defect is present.

---

## quality-gates-scope-agreement

A directory excluded from the formatter but not from the CI filter, or the
reverse, leaves part of the tree checked by one gate and not the other.
Captured fixtures must stay byte-for-byte; reformatting them changes the test
input. A path-scoped gate that works as configured can still be incomplete,
because an author enumerates what they run; the candidate someone else runs
has the weakest guarantee about its environment.

A formatter that rewrites generator output makes the generator's `--check` fail
on a clean checkout, so the staleness gate cannot even be wired into CI.

A passing-because-skipped check looks identical to a passing one in the CI
interface. A failed upstream trips both a correct fan-in, which compares every
result against success, and a naive one, which compares against failure; only
a skipped upstream separates them.

A gate that ran green over almost nothing is worse than a skip, because a skip
is at least visible. The full-history secret-scan rule is one instance.

CI runs on a clean checkout in one environment. A test reading the working
tree sees local scratch and ignored artifacts CI never sees, and a test
depending on line endings, locale, timezone, case sensitivity or binaries
passes in CI and fails locally. Running locally first catches what a
clean-room CI cannot.

---

## quality-gates-retrofit-ratchet

Ratcheting a complexity gate is the familiar case, and it generalises. Its
look-alike is far more tempting because it is smaller: writing a baseline is
work, while deleting a field from a comparison is one line and the diff reads
as a simplification. Both turn a red gate green. Only one leaves a gate.

- **Reversal cost tells them apart.** A baseline entry is deleted and the case
  is checked again. A narrowed comparison leaves no record that the property
  was ever checked, so nothing prompts anyone to restore it.
- **An exemption is a holding position.** It stops the gate reporting the
  instance and changes nothing about the instance, so the gate is green over
  the defect it was added to catch. An honest, documented list is still a list
  of defects.
- **A narrowed check is a permanent price for a temporary problem.** Where the
  failing case is a real defect with a small fix, the fix is cheaper.
- **The same pressure reaches the gate's data.** Editing a tracker field or a
  fixture to retire a finding leaves the gate green over a repository now also
  wrong about itself, and nothing later tells that from a finding answered
  properly. A gate whose cheapest remedy is falsifying its input is defective.

### Linters

A modern linter on an existing codebase reports too much to adopt as
written. Two responses work and two are traps:

| Response | Outcome |
|----------|---------|
| Fix everything first | Buries the gate change under a mechanical diff no reviewer can separate from a behavioural one, and gates untouched code the change was never about |
| Ignore the offending rule families globally | Never ends. New code is ungated on exactly the rules the project says it wants, nothing ever fails, so nothing is ever fixed |
| Freeze per file | Works |
| Narrow the gate's corpus, widening it per slice | Works, where the tool has no per-file ignore |

A per-file freeze gates a new file on everything, stops an existing file
getting worse, and makes shrinking the table the migration. A hand-maintained
table drifts and becomes a place to hide findings, and an unpinned linter
fails untouched code when a release adds rules to a selected family. The known
cost: a file-level freeze does not re-gate an existing file when it is edited.
Line-level would, and no widely available linter offers it.

### Per-slice corpus

A ratchet freezes which instances fail and leaves the analysis whole; widening
the corpus per slice narrows the corpus and leaves the rule whole. Both are
legitimate and suit different tools. The floor on enumerated files matters
because a mistyped root enumerates nothing and reports a clean tree. Widening
first makes the slice's own run red, and the author reads that as the gate
being wrong. A corpus repeated at two call sites is widened at one.

### Retiring a freeze

A caller-side finding, such as a strict type checker's unannotated-call code,
counts once for every call into something still frozen, so a caller's count
cannot fall while its callees are frozen. Cheapest-first lands on a leaf
caller, which is cleaned in full while its count barely moves. The shape, with
four modules taken root-first and 514 findings between them:

| Slice | Module | Own findings | Total remaining after |
| --- | --- | --- | --- |
| 1 | graph root | 330 | 152 |
| 2 | imports the root | 42 | 113 |
| 3 | imports both | 63 | 61 |
| 4 | leaf | 61 | 0 |

The first slice cleared 362 of the 514 while owning 330: the extra 32 were
caller-side findings in the three importing modules. Run cheapest-first, slice
one is the 42 and clears well under half of them, which reads as the migration
not working.

The table records one day's findings and is never re-derived, so a rule name
outlives the findings behind it. Retiring two entries in one downstream
project found three of the thirty-two rule codes they named had nothing behind
them. Dead names make the remaining work look larger than it is, the direction
that keeps a migration parked. Deleting one is not widening, so the hand-edit
ban does not reach it.

Sizing a family by deleting its entries edits the file the whole gate depends
on in order to size a decision, and is easy to restore imperfectly. Running
past the configuration measures without editing, but drops the rule selection
too, so an unnamed family measures the tool's defaults.

Two edits empty a blind-except entry: using the caught exception silences the
rule while the blind handler stays, and narrowing the handler does the real
work. Narrowing can go too far and let a raw exception escape. A suite that
passed before passes after for the same reason, so it is not the control.
Narrowing seventy handlers in one downstream migration left four sites wrong;
a contract test walking the whole hierarchy found all four.

### Site-local suppressions

A project holding only the freeze has one mechanism for two claims, and the
rule against adding a file to the table correctly blocks the second, leaving
an undocumented escape as the only move. Adding a file suppresses the rule for
every other line in it. A named suppression keeps failing on the next rule
that applies to the line; a bare one absorbs it. The directive is the one
comment that trails code, so its reason cannot travel with it.

The case that shows the two are not interchangeable: a test asserts a broad
exception because the narrower class varies by interpreter version. The linter
is wrong there. Narrowing reintroduces the platform dependence, and freezing
the file suppresses the check for every other assertion in it.

---

## quality-gates-length-bound-exemptions

A freeze table is generatable because a gate that finds instances can list
them on adoption day. A gate bounding a length cannot: its exemptions surface
one slice at a time, and a list that stopped growing while the corpus grows is
a finding. A path-scoped exemption absorbs every future violation in that
neighbourhood, which is what the freeze exists to avoid.

Measured on a downstream project of about a hundred source files, adopting a
two-line comment bound and a ten-line docstring bound: four exemptions surfaced
across two slices, a licence header, comments trailing consecutive lines of
code, a ruled banner and a wire-layout table. In all four something other than
the author sets the count.

---

## quality-gates-test-edit-boundary

Where tests are the source of truth, a merge-on-green policy cannot see a
weakened suite: it still reports green, which proves only that the code
matches whatever the tests were reduced to. Adding or tightening a test can
only narrow what passes, so green afterwards means more.

A deliberately loosened case usually moves off a break list onto nothing: it
passes because a check stopped firing, not because anything says it should.
Asserting it keeps a test that fails if the loosening is reverted. Without the
reason in the assertion, the loosening looks like an off-by-one, and
tightening it back is a one-character change that passes the whole suite.

The file filter is the enforceable half and the stated reason the half a
reviewer reads. The check reports five counts so a zero is readable: a
test-file count of zero under a non-zero range total means no tests were
touched, while a range total of zero means nothing was inspected. Exit 3 is
the reserved status for a check whose moment is not in progress. This is
governance, not a new threshold.

---

## quality-gates-verdict-reading

A "LOW" verdict can mean the output is inaccurate, the plausibility check is
unsound for this input class, or both, and each implies a different fix. In
one case a plausibility check flagged a record whose output matched the
reference on nearly every field; the fix was a per-class exception to the
check, not a change to the producer.

A lenient gate is the complement: a single-sample dip in a curve passes a
tolerance averaged across samples. Tightening the threshold would mis-flag
legitimate runs, so the gate stays and a human glance covers the residue.
