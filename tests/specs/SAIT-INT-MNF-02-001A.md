---
id: SAIT-INT-MNF-02-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567820
title: All stacks resolve to valid, non-empty file lists
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
tags: [manifest, resolution, dependency-graph]
---

## Short description

> **Given** the repository is cloned and `manifest.yaml` is present
> **When** every stack entry in the manifest is resolved via the
> dependency algorithm (core tier + recursive deps)
> **Then** every resolved file path exists and is non-empty

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every stack resolves to a non-empty file list; all files exist and are non-empty |
| FAILED | One or more stacks resolve to an empty list, or a resolved file is missing or empty |
| SKIPPED | `manifest.yaml` is absent or PyYAML is not installed |
| BLOCKED | `SAIT-INT-MNF-01-001A` is failing |
| ERROR | YAML parser fails; file system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3 with PyYAML installed

### Execution

1. Load `manifest.yaml` and build the entry lookup
2. For each stack entry, resolve the full dependency chain:
   a. Add all core tier IDs
   b. Recursively resolve the stack's `depends_on` tree
3. For each resolved file, verify it exists and is non-empty

### Assertions

1. Assert every stack produces a non-empty file list
2. Assert every resolved file path exists on disk
3. Assert every resolved file has size > 0

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-MNF-01-001A`, `SAIT-INT-MNF-03-001A`
- Implements: docs/architecture/08-crosscutting-concepts.md §8.1, manifest.yaml
