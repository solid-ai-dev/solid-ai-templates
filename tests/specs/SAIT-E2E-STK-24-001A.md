---
id: SAIT-E2E-STK-24-001A
uuid: 83aba6b7-8501-4e91-8f91-47c05efbff8e
title: Full interview produces a correct CLAUDE.md from the fixture stack
product: sait
type: e2e
area: STK
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-10-16
author: Branimir Georgiev
product-version: "2.x"
tags: [e2e, output, fixture, canary]
---

## Short description

> **Given** `INTERVIEW.md` and `fixture/stack.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` carrying the fixture's sections and
> the core tier's rules, with the fixture's placeholders substituted

This is the canary: the default live test, run at every release cut. It reads
the fixture stack, so it keeps an input when the concrete stacks move to forks.

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output carries Commands and Project structure from the fixture, `make test`, and the core tier's git and testing rules; no `[any]` placeholder remains |
| FAILED | A fixture section or a core-tier rule is absent, or a placeholder survives |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-MNF-02-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `fixture/stack.md`, `core/agents.md`
3. Interview answers:
   - Project name: echo
   - Language: Python
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `Commands` and `Project structure` sections are present
2. Assert `make test` is named as the test command
3. Assert base git conventions present, including the `feat:` commit type
4. Assert testing rules present
5. Assert no `[any]` placeholder remains

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-15-001A`
