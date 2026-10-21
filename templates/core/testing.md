# Base — Testing

[ID: base-testing]

What to test, how to keep tests honest, and how to prove a change.

## Test types

Classify a test by the boundary it crosses, not by who runs it or which
tool drives it.

| Type | Boundary crossed | Focus |
| --- | --- | --- |
| Unit | None | One function or class in isolation |
| Integration | Process or component | Interaction with a real dependency |
| System | System | The product against its requirements |
| Regression | Any, reusing existing tests | Unintended change |
| Exploratory | Any, unscripted | Unexpected behaviour |

- Replace a unit's dependencies with doubles
- Use the real dependency for the boundary an integration test covers;
  double only the unrelated ones
- Run system tests against documented requirements, in an environment
  representative of production
- Cover the critical user journeys with automated end-to-end tests
- Sign off acceptance manually against documented criteria; automation
  supports the sign-off, never replaces it
- Run smoke regression on every commit, quick regression on every merge
  request and full regression on each release candidate; automate smoke and
  quick fully
- Turn every defect exploratory testing finds into a regression test
  (SHOULD)

## Coverage

- Cover every happy path the functional requirements define
- Cover negative inputs and edge cases as well (SHOULD)
- Cover each dependency's faults at every tier: unavailable, malformed
  response, timeout, degraded operation (SHOULD)
- Meet the project's coverage threshold for new code before merging
- Never let coverage regress between releases
- Run every automated test from CI, with no human step
- Name a test so the name alone states the unit, the input and the expected
  outcome (SHOULD)
- Run a unit that reads a structured external artifact against real
  production data once before calling its suite complete, and add a
  regression test for each gap it shows

## Testability

- Keep business logic in pure functions, and push I/O to thin adapters at
  the edges (SHOULD)
- Inject dependencies rather than construct them in the code under test
  (SHOULD)
- Split a function that needs more than two mocks to test (SHOULD)
- Treat code that is hard to test as a design problem

## Isolation

[ID: base-testing-general]

- Test behaviour, not implementation details
- Keep each test independent, with no shared mutable state
- Set or clear every environment variable a test depends on, in that test;
  never rely on the ambient process state
- Treat a test that passes or fails by run order as an isolation bug
- Never enumerate, signal or terminate a process the test did not start
  (MUST NOT)
- Never mutate host state outside the working directory: the process
  table, system services, the registry, the user's applications (MUST NOT)
- Stub every seam through which the code under test reaches the host, even
  when its subject is already faked
- Investigate a failing test before anything else; never skip or suppress
  one without a documented reason
- Check the test's own logic first when it behaves unexpectedly

## External definitions

[ID: testing-external-definition]

- Assert at least one case against a fixed vector the specification
  publishes, wherever a format is defined outside the codebase (MUST)
- Never take a round trip through your own encoder and decoder as proof
  that either is correct
- Assert what an object does, not the type or exception class the runtime
  reports for it
- Assert that a misuse fails, not how it fails

## Guard use

[ID: testing-guard-is-used]

- Assert that the code under test takes a guard, not only that the guard
  works, where the guard exists for other code to take (MUST)
- Prefer a behavioural assertion, such as "a stopped component does no
  work"
- Otherwise wrap the real guard in a recorder that logs entry and exit, and
  assert the order of the work against it
- Pair every "does nothing" assertion with its "does something" control
- Sweep the module for sibling guards when one proves inert

```bash
MODULE=<module-under-review>
FIELD=<guard-field-name>
echo "references to $FIELD in $MODULE: $(grep -c "$FIELD" "$MODULE" || true)"
grep -n "$FIELD" "$MODULE" || true
```

Pass condition: the count is at least two and the listed lines include a
consumer. A count of one is the assignment alone: the guard is built and
never consulted.

## Provenance

[ID: testing-assert-provenance]

- Assert the source of a value, not the value, where a fix changes where it
  comes from: inject a source that yields a different value and assert the
  code overrides it
- Treat a new test that passes against the unfixed code as aimed at the
  wrong property, not as proof the fix was unnecessary
- Substitute at the name the module under test reads, not on the module
  that defines the type

## Thresholds

[ID: testing-name-what-pinned]

- State, beside every threshold assertion, the property it gates, the
  conditions it was calibrated under and what to do when an improvement
  moves it
- Name the property in the failure message, not only the observed value

## Empty results

[ID: testing-negative-assertion-coverage]

### Reach

- Assert that a test expecting no violations reached its inputs: compare
  the files it discovered against what its roots should cover (MUST)
- Fail on that comparison; never print a count for a reader to notice
- Report every occurrence, not the first per line or per file
- Fail an "every item holds" assertion when the set shrinks unexpectedly
- Give the coverage assertion its own test and its own message (SHOULD)
- Assert that each item declares its own value where a permissive default
  exists; prefer a default that is not a legal value

### Floors

- Assert a known floor, not mere non-emptiness
- Size the floor from a measurement, and state the derivation beside the
  constant
- Use the measured count for an append-only corpus, and a stated margin
  below it for one that churns

## Fault injection

[ID: testing-platform-fault-injection]

- Reproduce a fault that depends on the OS, filesystem, locale or
  interpreter with a double at the real call's seam; never wait for the
  platform to supply it (MUST)
- Clear a transient fault as it fires; give a permanent fault its own
  double (MUST)
- Name the platform the evidence came from wherever a test clears a
  suspected component
- Retest an exonerated suspect on the platforms that were not covered

## Unique resources

[ID: testing-unique-resource-allocation]

- Allocate a per-test port, directory, database or queue from a
  module-level counter or a fixture, never from a counter on a class other
  tests inherit (MUST)

## Worker leaks

[ID: testing-worker-leak-guard]

- Assert after every test, in an automatic fixture, that no thread,
  subprocess or server the suite started survives it (MUST)
- Run the assertion per test, not once at session end
- Name the leak in the message, and the fix: join with a timeout, never
  sleep
- Leave the assertion on permanently

## Call sites

[ID: testing-shared-path-breadth]

- Exercise every call site of a changed shared path, not only the reported
  case (MUST)
- Run the ground-truth comparison on every entity that uses the path
- Re-run every consumer that derives a committed artifact from the changed
  surface, and keep that list beside the surface

## Real data

[ID: testing-fix-fires-on-real-data]

- Run the real pipeline on the input a fix targets, and diff its output
  against the expected values
- Never take passing unit tests, suites and staleness checks as proof that
  the fix fired

## Refactors

[ID: testing-characterization-fingerprint]

- Hash the full-precision output before a behaviour-preserving refactor,
  and compare the hash after it
- Seed every nondeterministic source before taking the hash
- Discard the hash once the refactor lands; commit invariant property tests
  instead

## Rewrites

[ID: testing-ast-equivalence]

- Compare syntax trees before and after a whole-tree rewrite, such as a
  formatter adoption, with the language's own parser
- State the normalisation applied before the comparison
- Require the compared count to equal the number of files the rewrite
  touched
- Inspect and account for every file whose tree changed

## Rendered output

[ID: testing-verify-the-render]

- Verify a visual change on its rendered output, read headless off the
  pixels or the resolved DOM, never off the source (MUST)
- Capture the render before the change as well as after it (SHOULD)
- Confirm the build is fresh before re-editing a change that still looks
  wrong

## Contract tests

[ID: testing-ast-contract]

- Enforce the public-API contract with a test that parses each module: every
  public parameter and return annotated, every public function documented
- Report each failure as `file:line name(param)`
- Roll the test out behind an allowlist, module by module, and flip the
  global gate last

## Drift guards

[ID: testing-drift-guard]

- Give every fact stored in two places a test that fails when the copies
  diverge: a documented limit and its constant, live routes and the API
  contract, the runtime version and the package metadata, an export list
  and the module's bindings
- Introspect the live artifact; never hardcode the expected value
- Assert one direction: the derived copy matches the source of truth

## In-process server

[ID: testing-in-process-server]

- Serve the real app in a thread on port 0 and drive it over real HTTP,
  where a framework test client bypasses the server stack (SHOULD)
- Derive the base URL from the assigned port, and stop the server in a
  `finally`
- Share one serving helper between scripts and browser tests
- Reserve a container for tests that need the built image or sidecar
  services

## Container e2e

[ID: testing-container-e2e]

- Drive containers through a library that speaks the Docker API, so one
  test runs on Docker or rootless Podman
- Poll the health endpoint against a deadline; never sleep
- Skip cleanly where the optional e2e dependency is not installed
- Disable the resource reaper on rootless runtimes

## Test tiers

[ID: testing-tier-by-directory]

- Derive a test's tier from its directory with one collection hook: unit,
  integration, e2e
- Make the default run the fast tiers; gate container and browser tests
  behind an opt-in marker and an optional dependency extra
- Settle how test modules import one another before moving any into tier
  directories
