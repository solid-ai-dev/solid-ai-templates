---
id: SAIT-E2E-STK-04-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567819
title: Full interview produces a correct CLAUDE.md for a Node Express project
product: sait
type: e2e
area: STK
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, express, nodejs]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/node-express.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Express-specific rules
> alongside base and backend layer rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Express-specific rules (middleware, Zod validation, Supertest); base and backend rules present |
| FAILED | Express-specific rules absent; output indistinguishable from a generic backend service |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/node-express.md`, `core/agents.md`
3. Interview answers:
   - Project name: NotificationService
   - Language: TypeScript
   - Database: PostgreSQL
   - Auth: JWT
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Node.js, Express, TypeScript, Zod
2. Assert middleware rules present (error handler, request ID, validation)
3. Assert Zod validation rules present
4. Assert Supertest referenced in testing section
5. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-02-001A`