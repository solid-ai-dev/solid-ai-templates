---
id: SAIT-INT-TPL-05-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567810
title: Agent surfaces a conflict when two templates OVERRIDE the same section ID
product: sait
type: int
area: COMP
priority: p1
status: draft
environment: [local]
automatable: manual
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [composition, override, conflict]
---

## Short description

> **Given** two stack templates both declare `[OVERRIDE: <same-id>]` for the
> same parent section ID and are both included in a single composition
> **When** an agent assembles the rule set
> **Then** the agent detects the conflict, presents both competing overrides
> to the user, and asks which takes precedence before proceeding

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Agent explicitly flags the conflict, shows both OVERRIDE rules, and asks the user to choose before generating output |
| FAILED | Agent silently picks one OVERRIDE without notifying the user; or agent produces output without resolving the conflict |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-03-001A` is failing |
| ERROR | Agent fails to load or process the template files |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available
- Two test template files with conflicting OVERRIDEs prepared (see Setup)

### Setup

1. Create a temporary test template `test-stack-a.md`:
   ```markdown
   # Test Stack A
   [DEPENDS ON: stack/go-lib.md]

   ## Stack
   [OVERRIDE: go-lib-stack]
   - Language: Go 1.22+
   - HTTP: gin
   ```
2. Create a temporary test template `test-stack-b.md`:
   ```markdown
   # Test Stack B
   [DEPENDS ON: stack/go-lib.md]

   ## Stack
   [OVERRIDE: go-lib-stack]
   - Language: Go 1.22+
   - HTTP: echo
   ```
3. Open Claude Code and attach `stack/go-lib.md`, `test-stack-a.md`,
   and `test-stack-b.md`

### Execution

1. Ask the agent:
   ```
   Compose a rule set using go-lib.md, test-stack-a.md, and test-stack-b.md.
   Both stack files override the same section. How do you resolve the conflict?
   ```
2. Record the agent's response

### Assertions

1. Assert the agent identifies that both templates override `go-lib-stack`
2. Assert the agent presents the content of both competing OVERRIDEs
3. Assert the agent asks the user to choose which override applies
4. Assert the agent does not produce final output until the conflict is resolved

### Teardown

1. Delete `test-stack-a.md` and `test-stack-b.md`

## Notes

This tests the conflict resolution rule defined in the spec, chapter 8.3:
"Two templates both OVERRIDE the same ID → Error — the agent MUST surface
this conflict to the user and ask which override to apply."

## Related

- Related procedures: `SAIT-INT-TPL-03-001A`
- Implements: docs/architecture/08-crosscutting-concepts.md §8.3
