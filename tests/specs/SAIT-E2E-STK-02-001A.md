---
id: SAIT-E2E-STK-02-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567808
title: Full interview produces a correct CLAUDE.md for a Go Echo project
product: sait
type: e2e
area: STK
priority: p0
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, go-echo, claude-md]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/go-echo.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` that contains all required sections
> with rules drawn from the correct templates in the dependency chain

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Generated `CLAUDE.md` contains all required sections; base rules, go-service rules, and go-echo-specific rules are all present; no section is empty or contradictory |
| FAILED | One or more required sections are missing; base rules absent; go-echo-specific rules absent; sections are contradictory |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available
- Interview answers prepared (see Setup)

### Setup

1. Open Claude Code in any working directory
2. Attach the following files:
   - `INTERVIEW.md`
   - `stack/go-echo.md`
   - `core/agents.md`
3. Prepare the following interview answers:
   - **Project name**: MetricsHub
   - **Owner**: Infrastructure team
   - **Repo**: github.com/acme/metricshub
   - **Deployment**: Docker → Kubernetes (cloud)
   - **Database**: PostgreSQL via sqlc + pgx
   - **Auth**: JWT bearer tokens
   - **Feature flags**: yes — OpenFeature Go SDK
   - **Messaging**: no
   - **Output format**: CLAUDE.md

### Execution

1. Ask the agent:
   ```
   Using INTERVIEW.md and stack/go-echo.md, generate a CLAUDE.md
   for this project. Use core/agents.md for formatting rules.
   ```
2. Provide the prepared interview answers when the agent asks
3. Save the generated output as `CLAUDE.md` in a temp directory

### Assertions

1. Assert the output contains all required top-level sections:
   - `## Stack`
   - `## Architecture`
   - `## Commands`
   - `## Git conventions`
   - `## Code conventions`
   - `## Testing`
2. Assert `## Stack` lists Go 1.22+, Echo v4, sqlc, and pgx
3. Assert `## Architecture` contains the `cmd/` and `internal/` layout
   (from `stack/go-service.md`)
4. Assert `## Code conventions` includes Echo routing and middleware rules
   (from `stack/go-echo.md`)
5. Assert `## Code conventions` includes concurrency and graceful shutdown
   rules (from `backend/concurrency.md` via `go-service.md`)
6. Assert `## Code conventions` includes feature flag rules using OpenFeature
   (from `backend/features.md`)
7. Assert `## Git conventions` includes `go.sum` committed rule
   (from `stack/go-lib.md`)
8. Assert no section references placeholder text such as `[service]`
   without substitution

### Teardown

1. Delete the temporary `CLAUDE.md` generated during the test

## Related

- Related procedures: `SAIT-E2E-STK-01-001A`
- Implements: SPEC.md §How an agent uses the system