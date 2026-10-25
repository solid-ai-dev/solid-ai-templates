# Rationale: quality

Why the rules in `templates/core/quality.md` say what they say. The template
states each rule as one instruction; the reasoning, the failure it prevents
and the worked examples are here, one heading per section, named by ID
where the section has one.

## Principles

A deferral without a revisit trigger gets re-argued every time it comes up,
or is quietly forgotten; a deferral with a trigger is a decision. Examples:
"when this grows to N config values", "when a second call site appears".

Deleting a path that probing proved dead is distinct from YAGNI. YAGNI says
do not build speculative code; this says retract what probing made
speculative. "In case it's useful later" is sunk-cost reasoning: code with
no real case to anchor it rots, and confuses the next maintainer about which
path fires.

## Architecture

A hardcoded count is a stale count: the data changes and the number does
not.

## Naming

Names are the primary documentation. A name that needs reading the body to
understand a call site needs a better name or a split.

A public name that says which library sits behind a tier makes the caller
learn what each library is, and leaks: if swapping the implementation would
force a caller to change code, the name has leaked. `Transport.HTTP`, `JS`
and `HEADED` say when to pick each.

## Complexity

A boolean flag forces the caller to read the implementation to learn what
`true` means.

A threshold chosen by feel is too loose, masking bugs, or too tight,
breaking edge cases, with no record of why. Naming the data source lets a
maintainer rerun the analysis against fresh data.

## Dependencies

A silent local copy, written to dodge an import cycle, drifts from the
canonical version, for instance by skipping an upstream filter step, and
breaks later, invisibly.

A directional ban is distinct from the acyclic rule: two tiers that never
cycle can still cross a boundary the project declared closed, such as a
domain layer reaching into an adapter. The hook matches a dotted submodule
of a forbidden target as readily as the target itself.

A heavy or platform-limited dependency reached through one owning module
fails with the command that fixes it, and the CI leg without the extra
proves the package still imports.

## Errors

A wrong-but-plausible derived value, such as a 404 URL or a mismatched ID,
emitted without warning is worse than a script that refuses to run until the
data is correct.

An unbounded wait for a signal a failing worker will never send does not
fail; it hangs, and the reason lands where the caller cannot act on it: a
bind error on the worker's stderr under a caller spinning on a readiness
flag. The symptom, a hang, is unrelated to the cause, which is what makes it
expensive to diagnose.

A type per raise site re-encodes the messages as class names and serves the
tests, not the callers: a type earns its place when a caller would handle it
differently. Swapping a raise's built-in type breaks every caller catching
the built-in, so the catch contract wins.

A caller-side filter tighter than the function's real preconditions lets the
function rot on the excluded inputs, which no test exercises. A filter that
happens to exclude broken inputs is a buried defect.

## Deprecation and renames

Aliasing the outer name of a call alone produces a call that resolves and
then fails on its own arguments, naming a symbol the caller never wrote. The
half-aliased middle comes from deciding per symbol, because the cost is
uneven: a map entry for a class, a wrapper for a method, a `**kwargs` shim
for a keyword argument. Nothing catches it: the suite is written in the new
spelling, so the broken call never runs.

An open ticket body, a plan or a draft change description is a delayed
write: implemented verbatim later, it reintroduces a retired concept into
the files the retirement stripped.

## Module structure

A central constants module orphans each constant's provenance from the code
that uses it.

## quality-library-output

The host decides where output goes. A test runner that installs its own
handler hides a library's default, so only a fresh process shows it.

## Encoding and line endings

A Cyrillic `а` in a variable name reads as Latin `a` and matches nothing; a
name is typed, searched and compared. Only a tokenizer can tell an
identifier from the prose around it, so the check is per language. A rule
reaching comments or documentation buys a house typography at the cost of
everything else, and a generator whose strings draw a diagram is writing a
document.

Inheriting the console's encoding turns a correct string into mojibake on
another machine. The line ending fails worse because silently: a trailing
carriage return makes every downstream comparison miss, and the consumer
reports a confident zero rather than an error.

`.gitattributes` enforces LF at commit and checkout. `text=auto` is a
heuristic: one stray carriage return makes git file the blob as binary and
skip conversion. A file with CRLF and a
lone carriage return is filed `i/-text`, so a check naming `i/crlf` misses
the worst case. The check filters by extension because `i/-text` is right
for an image and a finding for Markdown, and splits on the tab because only
the path is tab-delimited.

## Comments

A comment explaining why something is safe is a load-bearing claim: the
code stays correct while the predicate it cites goes false. A cited number
inherits the cited item's lifecycle; a reader tracing a stale number lands
on a dead thread. Code outlives the tracker, so code never cites numbers,
while Markdown docs cross-reference them as their job. A source (author,
year, method, such as "Rappé 1992") ages gracefully where a number does not.

## Debug code

A probe that lands becomes code nobody maintains; its findings belong where
the change that used them is explained.

## quality-rejected-mechanism-sweep

A comment explaining why one module avoids a construct is evidence the
construct is wrong everywhere. Someone diagnosed a shared mistake, fixed the
module they were in, and had no reason to check the others. Where the sweep
finds hits, a design note was an unfixed bug with a known diagnosis. This is
the discovery half of verifying every call site.

## quality-constraint-corpus-sweep

A constraint is written for what gets authored next. A change that does not
ask about what exists ships green over its own violations, the state that
looks most like compliance.

## quality-destructive-ownership

The inputs a destructive operation decides from are what fail: an empty
configurable path resolves somewhere unintended, and a before-and-after
sample attributes a process that merely appeared. Paired with a filter on a
generic property, either destroys something nobody offered. The ownership
filter looks redundant inside the directory it was written for, so the next
reader will call it dead code, right about the common case and wrong about
why it exists. The path bug still happens; it stops being destructive.

## quality-cross-validation

A systematic tool bug masquerades as data divergence, and applying the
tool's values corrupts correct data. A rule weakened until its check goes
green stops describing the defect it was written for.

## Enforcement

A `lint --fix` pass at the consumer end hides the generator's
responsibility, makes every re-emit a noisy diff, and confuses contributors
who regenerate and see unexplained changes.
