---
id: SAIT-SMK-SYS-04-001A
title: DEPENDS ON headers match manifest depends_on
product: sait
type: smoke
area: SYS
priority: p0
status: ready
environment: [local, ci]
automatable: yes
created: 2026-05-07
author: Branimir Georgiev
product-version: "2.x"
tags: [structure, depends-on, manifest, drift]
---

## Short description

> **Given** the repository is cloned and all template files are present
> **When** every template's `[DEPENDS ON: ...]` header is compared
> to its manifest `depends_on` list
> **Then** both sources list the same set of dependencies

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every template's file header matches its manifest entry |
| FAILED | One or more templates have mismatched dependencies |
| SKIPPED | manifest.yaml not found or PyYAML not installed |
| BLOCKED | — |
| ERROR | File system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally
- PyYAML installed

### Setup

1. Change to the repository root
2. Load `templates/manifest.yaml`
3. Build a map of manifest ID to file path

### Execution

1. For each template file, extract file paths from `[DEPENDS ON: ...]`
2. For the same file, resolve manifest `depends_on` IDs to file paths
3. Compare the two sets

### Assertions

1. Assert file header dependencies equal manifest dependencies
2. Report differences as "header only" or "manifest only"

### Teardown

— (read-only check, no teardown required)

## Notes

SPEC.md file header policy: `[DEPENDS ON: ...]` headers MUST list
direct dependencies only — matching the manifest's `depends_on`.

## Related

- Related procedures: `SAIT-SMK-SYS-01-001A`, `SAIT-INT-MNF-01-001A`
