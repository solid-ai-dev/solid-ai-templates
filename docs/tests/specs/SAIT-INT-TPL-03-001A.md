---
id: SAIT-INT-TPL-03-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567805
title: OVERRIDE directive replaces parent section entirely in the assembled output
product: sait
type: int
area: TPL
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [composition, override, inheritance]
---

## Short description

> **Given** a stack template section marked `[OVERRIDE: <id>]` referencing a
> parent section tagged `[ID: <id>]`
> **When** an agent assembles the rule set for that section
> **Then** the output contains only the rules from the OVERRIDE section —
> the parent section rules are fully replaced

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Assembled section contains only the OVERRIDE rules; no rules from the parent section appear |
| FAILED | Parent section rules appear alongside or instead of the OVERRIDE rules |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load or process the template files |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code or equivalent agent available
- Test pair: `core/testing.md` (contains `[ID: testing-verify-the-render]`) and
  `fixture/stack.md` (contains `[OVERRIDE: testing-verify-the-render]`)

### Setup

1. Open Claude Code in the repository root
2. Attach `core/testing.md` and `fixture/stack.md`

### Execution

1. Ask the agent:
   ```
   Show me the assembled rendered-output section for the fixture stack.
   fixture/stack.md overrides it from core/testing.md.
   Which rules appear?
   ```
2. Record the assembled output

### Assertions

1. Assert the assembled section contains the rules from
   `fixture/stack.md` `[OVERRIDE: testing-verify-the-render]`
2. Assert the rules from `core/testing.md` `[ID: testing-verify-the-render]` do
   NOT appear
3. Assert the section is not empty

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-TPL-01-001A`, `SAIT-INT-TPL-02-001A`
- Implements: docs/architecture/08-crosscutting-concepts.md §8.1
