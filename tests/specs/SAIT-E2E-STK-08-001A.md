---
id: SAIT-E2E-STK-08-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567823
title: Full interview produces a correct CLAUDE.md for a Go gRPC service
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
tags: [e2e, output, grpc, go, protobuf]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/go-grpc.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing gRPC-specific rules
> alongside go-service and base rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains gRPC-specific rules (protobuf schemas, code generation, interceptors, error codes); go-service and base rules present |
| FAILED | gRPC-specific rules absent; output indistinguishable from a plain Go HTTP service |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/go-grpc.md`, `core/agents.md`
3. Interview answers:
   - Project name: PaymentGateway
   - Language: Go
   - Communication: gRPC (internal service-to-service)
   - Auth: mTLS
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Go, gRPC, Protocol Buffers
2. Assert protobuf schema authoring rules present (`.proto` files as source of truth)
3. Assert code generation workflow documented (`protoc` or `buf`)
4. Assert interceptor usage documented (logging, auth, recovery)
5. Assert gRPC status codes referenced instead of HTTP status codes
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-04-001A`