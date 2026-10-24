# Backend — gRPC
[ID: backend-grpc]
[DEPENDS ON: templates/backend/auth.md, templates/backend/observability.md]

Cross-cutting rules for gRPC services backed by Protocol Buffers. Applies
regardless of implementation language. Language-specific stacks extend this
file with runtime conventions, project structure, and tooling.

## When to use gRPC

- Use gRPC for synchronous service-to-service communication where performance,
  strong typing, or streaming are required
- Use gRPC when a shared proto schema across multiple language runtimes is
  preferable to maintaining multiple OpenAPI specs
- Do NOT use gRPC as the primary API for browser clients — use REST or GraphQL
  at the edge and gRPC internally

## Proto design
[ID: grpc-proto]

- Package all protos under a versioned namespace: `package [org].[service].v1`
- Keep one proto file per service — do not mix unrelated services in one
  file
- Name fields in `snake_case` — generated code adapts to each language's
  conventions
- Use `google.protobuf.Timestamp` for all timestamps — never raw integers
- Use `google.protobuf.FieldMask` for partial update (patch) operations
- Never renumber a field, or reuse a removed field's number or name
- Deprecate a field in place with `[deprecated = true]`, keeping its number
- Remove only a deprecated field, and reserve its number and name:
  `reserved 4; reserved "old_name";`
- Require a new package version (`v2`) for a breaking change; serve the old
  version until all consumers have migrated

## Service implementation
[ID: grpc-implementation]

- Keep service handlers thin — decode the request, call a domain service
  function, encode the response
- Never put business logic in the handler
- Keep gRPC imports out of domain service functions, so they stay
  independently testable
- Validate request messages at the handler entry point; return
  `INVALID_ARGUMENT` for missing or malformed fields
- Return every error as the gRPC status code that fits it, never as an
  HTTP status or a problem JSON body; put structured detail in
  `google.rpc.Status` details

### Status codes

The common cases; take any other from the full gRPC status code list.

| Situation | Code |
|-----------|------|
| Missing or invalid field | `INVALID_ARGUMENT` |
| Resource not found | `NOT_FOUND` |
| Caller not authenticated | `UNAUTHENTICATED` |
| Caller lacks permission | `PERMISSION_DENIED` |
| Conflicting state | `ALREADY_EXISTS` / `ABORTED` |
| System not in the state the call needs | `FAILED_PRECONDITION` |
| Quota or rate limit hit | `RESOURCE_EXHAUSTED` |
| Deadline passed before completion | `DEADLINE_EXCEEDED` |
| Transient infrastructure error | `UNAVAILABLE` |
| Unexpected error | `INTERNAL` |

## Interceptors
[ID: grpc-interceptors]

- Validate the token on every call in the **auth** interceptor — reject with
  `UNAUTHENTICATED` before the handler runs
- Exempt the `grpc.health.v1.Health` methods from it; they report
  serving status and nothing else
- Exempt the account sign-up, sign-in and account-recovery methods the
  project declares public
- Exempt no other method from the auth interceptor
- List each exempt method by its full name in the interceptor, never by a
  prefix or a whole service
- Serve the Health methods on the same TLS listener as the business RPCs, and
  probe with a client that speaks TLS (such as `grpc_health_probe -tls`)
  rather than opening a plaintext port
- Log method name, request ID, caller identity, duration, and status code
  for every call in the **logging** interceptor
- Propagate W3C `traceparent` via gRPC metadata in the **tracing**
  interceptor, using OpenTelemetry gRPC instrumentation
- Catch unhandled panics or exceptions in the **recovery** interceptor —
  return `INTERNAL`, never crash the server process
- Register all interceptors as a chain at server startup — not inside handlers

## Authentication
[EXTEND: backend-auth]

- Pass credentials via gRPC metadata: key `authorization`, value
  `Bearer <token>`
- Validate in the auth interceptor — not in service handlers
- Use mutual TLS (mTLS) for service-to-service calls in production
- Manage certificate rotation at the infrastructure layer (cert-manager,
  Vault)
- Use plaintext only in local development — never in staging or production

## Observability
[EXTEND: backend-observability]

- Expose Prometheus metrics on a separate HTTP port (`/metrics`):
  - `grpc_server_handled_total` — labelled by method and status code
  - `grpc_server_handling_seconds` — histogram, labelled by method
- Implement the standard gRPC Health Checking Protocol
  (`grpc.health.v1.Health`) — orchestrators and load balancers probe it
- Propagate trace context through gRPC metadata for distributed tracing

## Testing
[ID: grpc-testing]
[EXTEND: base-testing]

- Test domain service functions in unit tests, independently of gRPC — pass
  plain request structs/objects, assert plain response structs/objects
- Start an in-process gRPC server for integration tests and call it with a
  real client
- Test each method in integration tests for success, invalid argument, and
  auth failure
- Name tests `<MethodName>_<state>_<expected>`,
  e.g. `GetUser_UserNotFound_ReturnsNotFoundStatus`

## Proto tooling
[ID: grpc-tooling]

- Lint protos with `buf lint` in CI — enforce naming, field numbering, and
  style consistency
- Detect breaking changes with `buf breaking --against` in CI — reject PRs
  that introduce wire-incompatible changes without a version bump
- Generate stubs in CI
- Regenerate and commit stubs in the same PR as the proto change if generated
  code is committed; never let protos and stubs diverge
