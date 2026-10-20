---
id: SAIT-SMK-SYS-01-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567801
title: All DEPENDS ON file paths in stack templates resolve to existing files
product: sait
type: smoke
area: SYS
priority: p0
status: ready
environment: [local, ci]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [structure, depends-on, paths]
---

## Short description

> **Given** the repository is cloned and all template files are present
> **When** every `[DEPENDS ON: ...]` header in every stack template is read
> **Then** each listed file path resolves to an existing file in the repository

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every path listed in every `[DEPENDS ON: ...]` header exists as a file in the repository |
| FAILED | One or more paths listed in a `[DEPENDS ON: ...]` header do not resolve to an existing file |
| SKIPPED | Repository cannot be cloned or accessed |
| BLOCKED | — |
| ERROR | File system is inaccessible; `find` or equivalent tool fails |

## Steps

### Prerequisites

- Repository cloned locally
- Shell access with `grep` and file listing tools available

### Setup

1. Change to the repository root
2. Confirm the `stack/` directory is present

### Execution

1. Extract all `[DEPENDS ON: ...]` lines from every file in `stack/`:
   ```bash
   grep -r "DEPENDS ON" stack/
   ```
2. For each file path listed in the extracted lines, verify the file exists:
   ```bash
   # Example: verify stack/go-service.md depends resolve
   ls stack/go-lib.md backend/config.md backend/http.md
   ```
3. Repeat for every stack file

### Assertions

1. Assert every path extracted from `[DEPENDS ON: ...]` exists in the repository
2. Assert no path is a directory — all references must point to `.md` files

### Teardown

— (read-only check, no teardown required)

## Notes

Semi-manual because no automated parser for `[DEPENDS ON: ...]` exists yet.
A future CI step should automate this check using `manifest.yaml` as the
source of truth.

## Related

- Related procedures: `SAIT-SMK-SYS-02-001A`, `SAIT-INT-MNF-01-001A`
