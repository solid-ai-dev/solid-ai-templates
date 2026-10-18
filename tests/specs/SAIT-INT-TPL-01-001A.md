---
id: SAIT-INT-TPL-01-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567803
title: DEPENDS ON chain assembles a complete, non-contradictory rule set
product: sait
type: int
area: TPL
priority: p0
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [composition, depends-on, inheritance]
---

## Short description

> **Given** a concrete stack template with a multi-level DEPENDS ON chain
> **When** an agent loads the stack template and all its declared dependencies
> **Then** every rule from every template in the chain is present in the
> assembled rule set and no rule is silently dropped

## Results

| Result  | Condition                                                                                                     |
|---------|---------------------------------------------------------------------------------------------------------------|
| PASSED  | All sections from all templates in the dependency chain appear in the assembled output; no section is missing |
| FAILED  | One or more sections from a parent template are absent from the assembled output                              |
| SKIPPED | No agent available to run the assembly                                                                        |
| BLOCKED | `SAIT-SMK-SYS-01-001A` is failing — DEPENDS ON paths do not resolve                                           |
| ERROR   | Agent fails to load or process the template files                                                             |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code or equivalent agent available
- `fixture/stack.md` and its full dependency chain accessible: the core
  tier, `core/config.md`, `core/quality-gates.md` and
  `security/security.md`. The fixture is the one stack upstream keeps

### Setup

1. Open Claude Code in the repository root
2. Attach `fixture/stack.md` to the conversation

### Execution

1. Ask the agent:
   ```
   List every template in the full DEPENDS ON chain for fixture/stack.md,
   then list every section heading that will appear in the assembled rule set.
   ```
2. Record the list of templates and sections returned

### Assertions

1. Assert the dependency chain includes all of the following:
   - `core/quality.md`, `core/git.md`, `core/docs.md`, `core/testing.md`
   - `core/review.md`, `core/oop.md`, `core/config.md`
   - `core/quality-gates.md`, `security/security.md`
2. Assert section headings from every template in the chain are present
3. Assert no template in the chain is referenced but not loaded

### Teardown

— (read-only check, no teardown required)

## Related

- Related procedures: `SAIT-INT-TPL-02-001A`, `SAIT-INT-TPL-03-001A`
- Implements: SPEC.md §Inheritance model
