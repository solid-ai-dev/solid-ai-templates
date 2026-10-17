---
id: SAIT-SMK-SYS-19-001A
title: resolve.py names a missing dependency and a dependency cycle
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-17
author: Branimir Georgiev
product-version: "2.x"
tags: [tooling, resolver, cli, composition, fork]
---

## Short description

> **Given** a manifest whose chains name an ID with no entry, or loop back
> on themselves
> **When** the resolver is asked for each of those roots
> **Then** it exits non-zero with a message naming what broke — the
> missing ID and the entry naming it, or the cycle as a path — because a
> fork's stacks depend on upstream IDs the fork does not control

## Results

| Result | Condition |
|--------|-----------|
| PASSED | The valid root resolves at status 0, and each broken root exits 1 with its own message and no traceback |
| FAILED | A case exits with an unexpected status |
| FAILED | A case exits as expected and its message does not carry the phrase, so the status may be right for the wrong reason |
| FAILED | The message is right but arrives inside a traceback |
| FAILED | The check read no cases |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

1. Write a planted manifest to a temporary directory: one valid stack, one
   whose `depends_on` names `base-nowhere`, and one whose chain reaches
   `base-b -> base-c -> base-b`

### Execution

1. Run the resolver's own `main()` once per case in `BROKEN_CASES`, with
   `resolve.MANIFEST` pointed at the planted manifest, capturing status,
   stdout and stderr
2. Compare the status against the case's expectation
3. Assert the case's phrase appears in the combined output, and that no
   traceback does
4. Report how many cases were exercised

### Assertions

1. Assert the valid root resolves at status 0 and prints its stack file —
   the control that the planted manifest loads
2. Assert the missing-ID root exits 1 with `Missing dependency:
   stack-missing depends on base-nowhere`
3. Assert the cycle root exits 1 with `Dependency cycle: base-b -> base-c
   -> base-b`
4. Assert the case count is non-zero, per ADR-034

### Negative controls

1. **The defects that motivated the check.** The resolver skipped an ID
   with no entry and resolved a shorter chain at exit 0, and recursed on a
   cycle until Python raised `RecursionError`, naming no ID. Both broken
   cases fail against that behaviour
2. **A status right for the wrong reason.** A planted manifest that fails
   to load also exits non-zero; the valid root's status 0 and each case's
   phrase separate the two

## Related

- `SAIT-SMK-SYS-14-001A` — the resolver's handling of its arguments
- ADR-034 — why the case count is reported and floored
