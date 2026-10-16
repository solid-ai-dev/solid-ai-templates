---
id: SAIT-SMK-TPL-04-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567809
title: All EXTEND and OVERRIDE directives reference existing section IDs
product: sait
type: smoke
area: COMP
priority: p0
status: ready
environment: [local, ci]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [structure, extend, override, ids]
---

## Short description

> **Given** the repository is cloned and all template files are present
> **When** every `[EXTEND: <id>]` and `[OVERRIDE: <id>]` directive in every
> template is collected
> **Then** each referenced ID matches an `[ID: <id>]` tag declared somewhere
> in the template tree

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every ID referenced by EXTEND or OVERRIDE exists as an `[ID: ...]` tag in at least one template file |
| FAILED | One or more EXTEND or OVERRIDE directives reference an ID that does not exist in any template file |
| SKIPPED | Repository cannot be cloned or accessed |
| BLOCKED | `SAIT-SMK-SYS-02-001A` is failing |
| ERROR | File system is inaccessible; grep fails |

## Steps

### Prerequisites

- Repository cloned locally
- Shell with `grep` available

### Setup

1. Change to the repository root

### Execution

1. Collect all declared IDs:
   ```bash
   grep -rh "\[ID:" core/ security/ workflow/ infra/ data/ language/ backend/ frontend/ stack/ | \
     grep -oP '(?<=\[ID: )[^\]]+' | sort > /tmp/declared_ids.txt
   ```
2. Collect all EXTEND and OVERRIDE references:
   ```bash
   grep -rh "\[EXTEND:\|\[OVERRIDE:" core/ security/ workflow/ infra/ data/ language/ backend/ frontend/ stack/ | \
     grep -oP '(?<=\[(EXTEND|OVERRIDE): )[^\]]+' | sort > /tmp/ref_ids.txt
   ```
3. Find references with no matching declaration:
   ```bash
   comm -23 /tmp/ref_ids.txt /tmp/declared_ids.txt
   ```

### Assertions

1. Assert the output of step 3 is empty — every referenced ID is declared

### Teardown

1. Delete `/tmp/declared_ids.txt` and `/tmp/ref_ids.txt`

## Related

- Related procedures: `SAIT-SMK-SYS-02-001A`
- Implements: SPEC.md §Override mechanism