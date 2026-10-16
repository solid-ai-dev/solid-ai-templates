---
id: SAIT-E2E-FMT-01-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567810
title: Full interview produces a correct CLAUDE.md for a FastAPI project
product: sait
type: e2e
area: FMT
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, claude-md, claude-code]
---

## Short description

> **Given** `INTERVIEW.md`, `stack/python-fastapi.md`, and `core/agents.md`
> are attached to an agent
> **When** the agent conducts the interview and generates output
> **Then** the result is a valid `CLAUDE.md` formatted per `core/agents.md`
> containing all required sections

## Results

| Result  | Condition                                                                                                    |
|---------|--------------------------------------------------------------------------------------------------------------|
| PASSED  | Output file is named `CLAUDE.md`; all required sections present; formatting follows `core/agents.md` rules |
| FAILED  | Output uses a different format; required sections missing; wrong filename                                    |
| SKIPPED | No agent available                                                                                           |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing                                                                            |
| ERROR   | Agent fails to load template files or produce output                                                         |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available
- Same interview answers as `SAIT-E2E-STK-01-001A` (OrderService / FastAPI)

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-fastapi.md`, `core/agents.md`

### Execution

1. Ask the agent:
   ```
   Using INTERVIEW.md and stack/python-fastapi.md, generate a CLAUDE.md
   for this project. Use core/agents.md for formatting rules.
   ```
2. Provide the same interview answers as `SAIT-E2E-STK-01-001A`
3. Save the generated output

### Assertions

1. Assert output filename is `CLAUDE.md`
2. Assert formatting follows `core/agents.md` rules
3. Assert all required sections are present
4. Assert FastAPI-specific rules are present
5. Assert base rules from `core/git.md` and `core/quality.md` are present

### Teardown

1. Delete the generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-01-001A`, `SAIT-E2E-FMT-02-001A`
- Implements: `core/agents.md` formatting rules