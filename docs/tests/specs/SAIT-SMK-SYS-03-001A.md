---
id: SAIT-SMK-SYS-03-001A
title: Every template file has a corresponding manifest entry
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
tags: [structure, manifest, coverage]
---

## Short description

> **Given** the repository is cloned and all template files are present
> **When** every `.md` file in the template directories is checked
> **Then** each file has a corresponding entry in `templates/manifest.yaml`

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every template file has a manifest entry |
| FAILED | One or more template files have no manifest entry |
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

### Execution

1. Collect all `.md` files from template directories
2. Collect all `file` values from manifest entries
3. Report any template file not present in the manifest

### Assertions

1. Assert every template `.md` file has a manifest entry

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-MNF-01-001A` (reverse check)
