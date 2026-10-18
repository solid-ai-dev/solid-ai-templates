---
id: SAIT-SMK-SYS-21-001A
title: A fork's own key and its core-tier additions resolve
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-18
author: Branimir Georgiev
product-version: "2.x"
tags: [tooling, resolver, manifest, composition, fork]
---

## Short description

> **Given** a manifest with templates under a key no tool names, and a
> `fork_core` list adding one of them to every chain
> **When** the resolver is asked for a stack depending on the other
> **Then** the chain carries the upstream core file, the fork's own
> dependency and the fork's core addition, because a fork MUST NOT edit
> upstream's keys and has nowhere else to put a template

## Results

| Result | Condition |
|--------|-----------|
| PASSED | The planted stack resolves at status 0 and its chain names all three files |
| FAILED | The resolver exits non-zero, or the chain omits one of the three files |
| FAILED | The output arrives inside a traceback |
| FAILED | No case was run |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

— (the check writes its planted manifest to a temporary directory)

### Execution

1. Write `FORK_MANIFEST`: `core: [base-a]`, `fork_core: [fork-readme]`, an
   `acme:` key holding `fork-readme` and `fork-lib`, and `stack-fork`
   depending on `fork-lib`
2. Resolve `stack-fork` through `resolve.py`'s own entry point, with the
   planted manifest in place of the real one

### Assertions

1. Assert the exit status is 0 and the chain names
   `templates/core/quality.md`, the upstream core file and the control that
   the chain resolved at all
2. Assert it names `templates/core/git.md`, the fork's own dependency read
   from a key no tool names
3. Assert it names `templates/core/docs.md`, the fork's core-tier addition
4. Assert the case count is non-zero, per ADR-034

### Negative controls

1. **The defect that motivated the check.** The resolver read five fixed
   keys. Run against that resolver, the planted manifest exits 1 with
   "Missing dependency: stack-fork depends on fork-lib", so the fork's
   template was invisible

## Related

- ADR-049: a fork appends under keys of its own and never edits upstream's
- SAIT-SMK-SYS-20-001A: the check that a fork leaves upstream's keys alone
