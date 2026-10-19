---
id: SAIT-INT-TPL-02-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567804
title: EXTEND directive adds stack rules on top of parent section without removing base
rules
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
tags: [composition, extend, inheritance]
---

## Short description

> **Given** a stack template section marked `[EXTEND: <id>]` referencing a
> parent section tagged `[ID: <id>]`
> **When** an agent assembles the rule set for that section
> **Then** the output contains all rules from the parent section followed by
> all rules from the EXTEND section — no base rules are removed

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Assembled section contains all base rules AND all stack extension rules; order is base first, extension second |
| FAILED | One or more base rules are absent; or extension rules replace rather than extend base rules |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load or process the template files |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code or equivalent agent available
- Test pair: `core/testing.md` (contains `[ID: base-testing-general]`) and
  `fixture/stack.md` (contains `[EXTEND: base-testing-general]`)

### Setup

1. Open Claude Code in the repository root
2. Attach `core/testing.md` and `fixture/stack.md`

### Execution

1. Ask the agent:
   ```
   Show me the assembled general testing rules for the fixture stack.
   Include all rules from core/testing.md and all rules from the
   EXTEND in fixture/stack.md.
   ```
2. Record the assembled output

### Assertions

1. Assert all rules from `core/testing.md` `[ID: base-testing-general]` are
   present
2. Assert all rules from `fixture/stack.md` `[EXTEND: base-testing-general]`
   are present
3. Assert base rules appear before extension rules
4. Assert no base rule is missing or overwritten

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-TPL-01-001A`, `SAIT-INT-TPL-03-001A`
- Implements: docs/architecture/08-crosscutting-concepts.md §8.1
