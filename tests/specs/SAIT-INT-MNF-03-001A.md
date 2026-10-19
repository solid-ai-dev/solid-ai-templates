---
id: SAIT-INT-MNF-03-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567821
title: All resolved chains include core tier files
product: sait
type: int
area: MANIF
priority: p0
status: ready
environment: [local, ci]
automatable: yes
created: 2026-05-06
author: Branimir Georgiev
product-version: "2.x"
tags: [manifest, resolution, core-tier]
---

## Short description

> **Given** the repository is cloned and `manifest.yaml` is present
> **When** every stack entry is resolved via the dependency algorithm
> **Then** every core tier ID appears in the resolved set

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every stack's resolved chain includes all core tier IDs |
| FAILED | One or more core IDs are missing from a stack's resolved chain |
| SKIPPED | `manifest.yaml` is absent or PyYAML is not installed |
| BLOCKED | `SAIT-INT-MNF-02-001A` is failing |
| ERROR | YAML parser fails; file system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3 with PyYAML installed

### Execution

1. Load `manifest.yaml` and extract the `core:` list
2. For each stack, resolve the full dependency chain
3. Verify every core ID appears in the resolved set

### Assertions

1. Assert every core ID from `manifest.yaml` is present in
   every stack's resolved chain

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-MNF-02-001A`, `SAIT-INT-MNF-04-001A`
- Implements: docs/architecture/05-building-block-view.md §5.3
