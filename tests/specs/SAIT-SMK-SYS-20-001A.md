---
id: SAIT-SMK-SYS-20-001A
title: A fork leaves upstream's manifest keys as it last merged them
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
tags: [manifest, fork, composition, merge]
---

## Short description

> **Given** a fork's manifest and the upstream revision the fork last merged
> **When** the keys upstream owns — `core`, `base`, `backend`, `frontend` —
> are compared between the two
> **Then** any entry added, removed or changed under them fails, naming the
> key and the entry, because that edit is what turns the fork's next
> upstream merge into a conflict

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every planted case yields exactly its owed findings, and the real manifest's upstream keys match the baseline |
| FAILED | A planted case yields findings other than those it owes |
| FAILED | An upstream key's entry is added, removed or changed against the baseline |
| FAILED | `SAIT_UPSTREAM_REF` is set and shares no history with HEAD, or the baseline manifest cannot be read |
| FAILED | No planted case or no upstream key was compared |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | PyYAML is not installed |

## Steps

### Prerequisites

- Repository cloned locally, with git
- Python 3 and PyYAML
- In a fork: a ref holding upstream's history, named in `SAIT_UPSTREAM_REF`

### Setup

— (operates on the committed tree and the working manifest)

### Execution

1. Compare each planted fork manifest in `OWNERSHIP_CASES` with the planted
   upstream manifest, and compare the findings with those the case owes
2. Take the baseline: with `SAIT_UPSTREAM_REF` set, the manifest at the
   merge base of HEAD and that ref; unset, the working manifest itself
3. Compare the working manifest's upstream keys with the baseline's
4. Report the planted-case count, the upstream keys compared, and the
   baseline used

### Assertions

1. Assert a planted fork that appends a stack and a platform, and adds a
   key of its own, yields no finding — the control that legal appends pass
2. Assert planted edits yield one finding each: the core tier changed, an
   upstream entry changed, an entry added under an upstream key, and an
   upstream entry removed
3. Assert the real manifest's upstream keys match the baseline
4. Assert both counts are non-zero, per ADR-034

### Negative controls

1. **The defect that motivated the check.** A fork edits an upstream key
   and nothing notices until its next upstream merge conflicts. Run with
   `SAIT_UPSTREAM_REF` at a revision before an upstream-key change and the
   check names that entry
2. **A comparison that finds nothing.** A comparison that returns no
   findings passes upstream's run against itself; the planted edits fail
   against it, each by its owed finding

## Related

- ADR-049 — a fork appends under `stacks:`, `platform:` and its own keys,
  and never edits upstream's
- ADR-034 — why the counts are reported and floored
