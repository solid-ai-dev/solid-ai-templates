# Rationale: testing

Why the rules in `templates/core/testing.md` say what they say. The template
states each rule as one instruction; the reasoning, the failure it prevents
and the worked examples are here, one heading per section, named by ID
where the section has one.

## Test types

The boundary crossed is what changes the failure modes a test can see, so
it decides the type; the tool that drives the test and the asset that feeds
it do not. A test fed from the product specification is still an
integration test if it crosses one component boundary. Regression is a
selection of existing tests rather than a type of its own, which is why its
rule is about when each subset runs.

## Coverage

Fabricated inputs cover the cases the author imagined. One run against real
production data exposes the structural holes nobody fabricated; it does not
replace the unit suite, it shows where the suite needs a regression test
per invariant.

## Testability

Code that is hard to test is hard because of its design: a function mixing
logic with I/O needs mocks for the I/O before the logic can be reached. A
pure centre with thin adapters at the edges makes the centre unit-testable
and the edges integration-testable. More than two mocks is the usual sign
of more than one responsibility.

## base-testing-general

Environment variables and other process-global state are shared across the
whole test process. A module that mutates them at import time leaks into
every test, and import order is not guaranteed, so a test that depends on a
variable being set, or unset, has to say so itself.

Host damage is a distinct class from in-process leakage and more severe:
the failure is damage to the developer's machine, not a flaky test, and a
suite doing it can pass every assertion while leaving only a line on
stderr. A fake at one seam does not neutralise a real call at another,
which is why every seam that reaches the host is stubbed.

## testing-external-definition

A suite can be blind by construction. Where the code under test and the
code asserting on it share an assumption, every assertion agrees and the
assumption is never tested; coverage reports the lines as covered, by a
witness that cannot disagree. Three defects of this shape shipped in one
library and survived a fully passing suite: a checksum written and read high
byte first where the format sends it low byte first; a length-prefixed
frame read as whatever one socket read returned, which coincides on a local
link and diverges across a router; an identifier written as a constant and
never compared on read.

An assertion phrased against a runtime detail tests the runtime.
`threading.Lock` is a type on Windows and a builtin function on Linux, and
entering the unconstructed class raises `AttributeError` on Python 3.10 and
`TypeError` on 3.13; both assertions written to catch one defect varied by
platform and version. Exercising the object (acquire, release, enter) does
not. An error type the interface declares is different: it is part of the
contract callers handle, so asserting it tests the code, not the runtime.

## testing-guard-is-used

Whether a guard works and whether the code uses it look identical from a
test run and from a coverage report. The shape is a field built, exposed
through a public method, and never consulted: a lock never acquired, a stop
event set and never read, a validator never invoked. The constructor line
runs, so it is covered; the field works, so a test of it passes. One library
shipped a lock and a stop event in this state across two public classes,
with four passing tests about those locks.

A recording wrapper puts the guard and the work in one log, and the order
says whether the work happened inside the guard. A "stopped component does
nothing" test passes against a component that never does anything, so the
not-stopped control is what gives it meaning. One inert primitive is
grounds to sweep for its siblings, because one author usually wired them
the same way.

## testing-assert-provenance

Sometimes the defect is not that a value is wrong but that it is not the
code's own: it is inherited from a platform, a library default or a parent
process, and happens to be right today. A TLS client that set no minimum
protocol version took its floor from the linked OpenSSL. The obvious test,
asserting the floor is TLS 1.2, passed before and after the fix, because
that OpenSSL already defaulted to 1.2. Injecting a context whose floor
starts at TLS 1.0 and asserting the library raises it fails against the
unfixed code, which is what the test was for.

A standard-library type's own methods may resolve their class through a
module attribute, so replacing `ssl.SSLContext` on the `ssl` module sent the
setter back into the double and it recursed; redirecting only the name the
module under test reads was the working seam.

## testing-name-what-pinned

An intended improvement that legitimately moves a number fails a threshold
test in the same way a regression does. Unless the test says what the
threshold pins and how it was calibrated, nobody can tell whether to lower
the bar, update the test or revert. Compare "Expected ≥ 0.85, got 0.81"
with a message naming the property and its calibration.

## testing-negative-assertion-coverage

A test asserting nothing was found passes identically when nothing was
examined. A citation gate asserting `found == []` passed on every run while
twelve citations sat in commented configuration, because its roots were
Python-only. A first-match scan undercounts, and the count is what a reader
uses to decide whether the work is done.

A floor cannot be derived from the corpus it guards: comparing a set
against its own size is vacuous. An enumeration that breaks returns nothing
rather than a fraction, so any floor above zero catches every break, and a
generous margin for ordinary deletions costs no detection.

Enumerations break in ways the assertion cannot see: a pattern anchored at
the start of a line misses indented lines, and a listing of the index cannot
see an unstaged file. The controls that test a check's own reach are
procedure for whoever writes checks, and live in `docs/playbook.md`,
"Control-test a check you are changing".

## testing-platform-fault-injection

A test that fails on one platform does not run for anyone who is not on it.
The dangerous case is an investigation concluded on the author's platform
and recorded as settled. A socket teardown helper was suspected during a
connection-reset fix, tested on Windows where `shutdown()` on a reset
socket is silent, and recorded as cleared. On Linux the same call raises
`ENOTCONN`; the helper was the remaining half of the bug, and the closed
issue kept reproducing on the only platform CI runs.

A transient-fault double left armed fails every call the same way, so the
retry path never runs and the test written for it passes having reached
nothing.

## testing-unique-resource-allocation

A counter on a base class stops being unique once the class is subclassed:
`type(self).counter += 1` reads the inherited value and writes a new
attribute on the subclass, so every subclass restarts the sequence. Three
test classes all bound the same ports, and where a socket lingered this
produced a ten-minute CI hang: the second bind failed inside a worker thread
and the caller waited on it with no timeout.

## testing-worker-leak-guard

A leaked worker damages the run after the test that caused it: the culprit
passes and something unrelated fails, or a traceback beside the summary
reads as a failure. Review does not catch it, because a fixture that calls
stop and sleeps looks like teardown. A per-test assertion names the culprit,
and enumerating live threads costs one list comprehension per test.

## testing-shared-path-breadth

A fix to a shared path can surface latent bugs at call sites that were
silent before. "Expected unchanged" is the bug case, so it is verified
rather than assumed. A stale derived artifact reads as the fix not working,
which is why the consumers are re-run.

## testing-fix-fires-on-real-data

Indirect green signals lie independently: unit tests pass because the
synthetic input took the new branch, the suite passes because nothing
regressed, staleness checks pass because no artifact changed. The new code
can still never fire on the real case, because the real input lacks the
shape the fix assumed.

## testing-verify-the-render

A design token can resolve unexpectedly, a more specific rule can win the
cascade, a deploy can lag its source, a cache can serve an old copy. The
before-capture confirms the problem exists at all. Golden-output tests pin
structure and text but cannot say whether something is black, centred or on
screen.

## testing-drift-guard

Some facts unavoidably live twice. Without a guard the copies drift, which
is the failure single-source-of-truth exists to prevent. A Python `__all__`
holds strings, so an entry can name nothing; ruff `F822` reports that in a
plain module and stays silent in `__init__.py`, where export lists live.
Languages whose compiler sees the export (Rust `pub use`, Go capitalised
names) need no guard.

## testing-container-e2e

Hardcoding Docker and a fixed sleep breaks on rootless Podman, in CI
without Docker, and on a slow start. Ryuk and similar reapers assume a
privileged Docker. Local multi-service composition belongs to
`containers.md`.

## testing-tier-by-directory

A hand-applied marker drifts from where the test lives; a tier derived from
the directory cannot. A tier layout puts modules one level down and repeats
basenames across tiers, and the runner's import rules decide whether that
collects. The decision is cheap before the first file moves and a rewrite of
every helper import after.
