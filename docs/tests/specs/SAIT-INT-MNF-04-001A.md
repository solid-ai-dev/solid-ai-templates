---
id: SAIT-INT-MNF-04-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567822
title: Prompt builds for all stacks
product: sait
type: int
area: MANIF
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-05-06
author: Branimir Georgiev
product-version: "2.x"
tags: [manifest, resolution, prompt-assembly]
---

## Short description

> **Given** the repository is cloned and `manifest.yaml` is present
> **When** every stack's resolved file chain is read and concatenated
> with the output format template
> **Then** the assembled prompt is non-empty and above a minimum
> character threshold

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every stack produces a prompt above 500 characters |
| FAILED | One or more stacks produce a prompt below 500 characters or a file read fails |
| SKIPPED | `manifest.yaml` is absent or PyYAML is not installed |
| BLOCKED | `SAIT-INT-MNF-02-001A` is failing |
| ERROR | YAML parser fails; file system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3 with PyYAML installed

### Execution

1. Load `manifest.yaml` and resolve deps for each stack
2. Read every resolved file and the output format template
3. Concatenate into a prompt string
4. Verify the prompt length exceeds 500 characters

### Assertions

1. Assert no file read raises an exception
2. Assert every assembled prompt is at least 500 characters

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-MNF-02-001A`, `SAIT-INT-MNF-03-001A`
- Implements: ADR-007 §E2e tests validate templates, not generation
