---
id: SAIT-E2E-STK-11-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567829
title: Full interview produces a correct CLAUDE.md for a Flask project
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
tags: [e2e, output, flask, python]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/python-flask.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Flask-specific rules
> alongside python-service and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Flask-specific rules (blueprints, application factory, Flask-SQLAlchemy, pytest-flask); python-service and base rules present |
| FAILED | Flask-specific rules absent; output indistinguishable from a generic Python service |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-flask.md`, `core/agents.md`
3. Interview answers:
   - Project name: ReportingAPI
   - Language: Python
   - Database: PostgreSQL via Flask-SQLAlchemy
   - Auth: JWT
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Flask, Python, Flask-SQLAlchemy
2. Assert application factory pattern documented (`create_app()`)
3. Assert blueprint registration rules present
4. Assert pytest-flask referenced in testing section
5. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-01-001A`, `SAIT-E2E-STK-03-001A`