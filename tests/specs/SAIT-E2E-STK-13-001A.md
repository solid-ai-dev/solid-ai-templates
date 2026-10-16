---
id: SAIT-E2E-STK-13-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567831
title: Full interview produces a correct CLAUDE.md for a Python gRPC service
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
tags: [e2e, output, grpc, python, protobuf]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/python-grpc.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Python gRPC-specific rules
> alongside python-service and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Python gRPC rules (protobuf schemas, grpcio-tools generation, interceptors, servicer implementation); python-service and base rules present |
| FAILED | gRPC-specific rules absent; output indistinguishable from a generic Python HTTP service |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-grpc.md`, `core/agents.md`
3. Interview answers:
   - Project name: MLInferenceService
   - Language: Python
   - Communication: gRPC (internal service-to-service)
   - Auth: mTLS
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Python, gRPC, Protocol Buffers
2. Assert `.proto` files referenced as source of truth
3. Assert `grpcio-tools` or `buf` referenced for code generation
4. Assert servicer implementation pattern documented
5. Assert interceptor usage documented (logging, auth)
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-01-001A`, `SAIT-E2E-STK-08-001A`