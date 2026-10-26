---
id: SAIT-SMK-SYS-25-001A
title: A load directive names a listed task, in its heading's tags
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-26
author: Branimir Georgiev
product-version: "3.x"
tags: [tooling, manifest, composition, delivery]
---

## Short description

> **Given** a template heading carrying a load directive
> **When** smoke reads every template and the manifest's task kinds
> **Then** the directive names a listed kind or `check`, sits among its
> heading's tags, is the heading's only load and not under a loaded
> heading, and no template that guards data, credentials or
> authentication carries one, because the directive decides whether a
> rule is in context on every turn

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every planted case yields the findings it owes, and no real template carries an unknown, misplaced, doubled, nested or guarded directive |
| FAILED | A real template carries such a directive |
| FAILED | A planted case yields findings other than those it owes |
| FAILED | No planted case was run, or the manifest lists no kind |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

— (operates on `templates/` and `templates/manifest.yaml`, and on planted
texts)

### Execution

1. For each text in `LOAD_CASES`, collect the load findings against the
   planted kinds and compare them with those the case owes
2. Read the task kinds from `templates/manifest.yaml`
3. Collect the load findings for every template, and count the directives,
   which may be zero

### Assertions

1. Assert a listed kind and `check` yield no finding
2. Assert a kind no task lists yields one finding naming it
3. Assert a directive after a rule yields one finding
4. Assert a heading's second directive yields one finding
5. Assert a directive under a loaded heading yields one finding
6. Assert a directive inside a fence is not read
7. Assert a directive in a guarded template yields one finding
8. Assert the real templates yield no finding
9. Assert the planted-case and kind counts are non-zero, per ADR-034

### Negative controls

1. **An unknown kind in a real template.** A `nowhere` directive under the
   first section of `templates/core/git.md` fails with "names nowhere,
   which no task lists"
2. **A directive in a guarded template.** A `check` directive under the
   first section of `templates/security/security.md` fails as a guarded
   template

## Related

- ADR-058: templates place each rule, and task procedures load on demand
- The spec, chapter 8.1: the load directive and the manifest's `tasks:`
