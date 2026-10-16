---
id: SAIT-E2E-STK-16-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567834
title: Full interview produces a correct CLAUDE.md for a generic Go service
product: sait
type: e2e
area: STK
priority: p2
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, go, service]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/go-service.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing shared Go service rules
> that all Go HTTP stacks inherit from

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains shared Go service rules (net/http, structured logging, graceful shutdown, testify); base rules present; no framework-specific rules present |
| FAILED | Framework-specific rules (Echo, Gin) appear despite no framework being selected; shared rules absent |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/go-service.md`, `core/agents.md`
3. Interview answers:
   - Project name: HealthCheckService
   - Language: Go
   - Framework: none (standard library only)
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Go with no HTTP framework
2. Assert `net/http` referenced as transport layer
3. Assert structured logging conventions present (slog or zap)
4. Assert graceful shutdown pattern documented
5. Assert testify referenced for assertions in tests
6. Assert no Echo, Gin, or other framework rules present
7. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-02-001A`, `SAIT-E2E-STK-08-001A`