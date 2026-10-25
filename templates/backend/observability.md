# Backend — Observability
[ID: backend-observability]

## Logging

### Log levels

Use the correct level — do not elevate debug information to INFO:

| Level | When to use | Examples |
|-------|-------------|---------|
| FATAL | App cannot continue — imminent shutdown | Out of memory, missing critical dependency at startup, DB schema mismatch |
| ERROR | Operation failed — normal flow disrupted | Failed DB write, file not found, unhandled exception in request handler |
| WARN | Unexpected but recoverable — may lead to error | Low disk space, slow response, retry attempt, deprecated endpoint accessed |
| INFO | Normal operation — confirm correct functioning | Order accepted, service started, payment processed, scheduled job completed |
| DEBUG | Technical detail for debugging — not for production | Query results, data mapping steps, connection established |
| TRACE | Most verbose — step-by-step tracing, development only | Function parameters, pipeline steps, request/response payloads |

- Set the default log level to **INFO** in all environments
- Never enable DEBUG or TRACE in production by default (MUST NOT)
- Never put debug or trace information in INFO (MUST NOT) — keep it operational

### Log format

- Use structured logging in all environments: JSON in production,
  human-readable in development
- Include in every log entry: timestamp, level, message, properties (MUST)
- Include a request ID in all log entries for a given request lifecycle
- Keep the message template beside the rendered message, and its values
  as structured properties, so entries can be grouped by template

### Rules

- Log errors once — at the top of the call stack, not at every level
- Never log sensitive data: passwords, tokens, API keys, PII; the one
  exception is the client IP, in the security log only
- Log client errors (4xx) at INFO; log authentication and authorisation
  failures at WARN
- Log server errors (5xx) at ERROR
- Log every unhandled error with enough context to reproduce the issue (MUST)

## Distributed tracing

- Keep the **trace ID** of a valid incoming W3C trace context at the service
  boundary, and create a new span for each hop
- Start a new trace only where the incoming context is absent, invalid or
  deliberately rejected, such as at an untrusted public edge
- Propagate the trace ID in all outbound calls (HTTP headers, message queue
  metadata) using the W3C `traceparent` header or OpenTelemetry context
- Include the trace ID in every log entry for that request — use the same
  field name across all services (`trace_id`)
- Use OpenTelemetry as the instrumentation standard
- Avoid vendor-specific SDKs in application code
- Export to the backend of choice (for example Jaeger, Tempo or Datadog)
  via the OTel collector
- Create spans for: inbound HTTP requests, outbound HTTP calls, DB queries,
  cache operations, and background job execution
- Keep span names low-cardinality (MUST) — use route templates, not URLs
  with IDs (e.g. `GET /users/{id}`, not `GET /users/42`)
- Return the trace ID in error responses (`Trace-Id` header) so clients
  can report it to support

## Health check

- Expose a health check endpoint: `/health` or `/healthz`
- Return HTTP 200 when the service is ready to handle traffic
- Return HTTP 503 when a dependency no request can be served without,
  such as the primary database, is unavailable
- Never fail the health check on an optional dependency, such as a
  cache: every instance leaves rotation at once (MUST NOT)
- Never require authentication for the health check (MUST NOT)
- Make the health check the first thing that passes before traffic is
  routed to a new instance (MUST)

## Error visibility

- Distinguish between client errors (4xx) and server errors (5xx) in logs
- Include correlation/request IDs in error responses to enable log tracing
- Never expose internal state, stack traces, or file paths in error responses
