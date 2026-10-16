---
id: SAIT-E2E-STK-18-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567836
title: Full interview produces a correct CLAUDE.md for a Node.js library project
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
tags: [e2e, output, nodejs, library, npm]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/nodejs-lib.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Node.js library–specific rules
> without server or deployment sections

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Node.js library rules (ESM/CJS dual publish, package.json exports map, semantic versioning, Vitest or Jest); base rules present; no Express or HTTP rules present |
| FAILED | Output includes HTTP server rules; packaging conventions absent |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/nodejs-lib.md`, `core/agents.md`
3. Interview answers:
   - Project name: parsekit
   - Language: TypeScript
   - Distribution: npm package
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Node.js / TypeScript with no HTTP framework
2. Assert `package.json` `exports` map referenced for dual ESM/CJS publishing
3. Assert semantic versioning rules documented
4. Assert Vitest or Jest referenced for testing
5. Assert no Dockerfile or HTTP server rules present
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-10-001A`, `SAIT-E2E-STK-15-001A`