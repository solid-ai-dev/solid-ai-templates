# Backend — Observability
[ID: backend-observability]

## Logging

### Log levels

- Set the default log level to **INFO** in all environments
- Never enable DEBUG or TRACE in production by default (MUST NOT)
- Never put debug or trace information in INFO (MUST NOT) — keep it operational

### Log format

- Use structured logging in all environments: JSON in production,
  human-readable in development
- Include in every log entry: timestamp, level, message, properties (MUST)
- Include a request ID in all log entries for a given request lifecycle
- Keep the message constant and its variable values in structured
  properties, so entries can be grouped by message

### Rules

- Log errors once — at the top of the call stack, not at every level
- Never log sensitive data: passwords, tokens, API keys, PII; the one
  exception is the client IP, in the security log only
- Log a failure the caller caused, such as invalid input, at INFO
- Log authentication and authorisation failures at WARN
- Log a failure the service caused at ERROR
- Log every unhandled error with enough context to reproduce the issue (MUST)

## Distributed tracing

- Keep the **trace ID** of a valid incoming W3C trace context at the service
  boundary, and create a new span for each hop
- Start a new trace only where the incoming context is absent, invalid or
  deliberately rejected, such as at an untrusted public edge
- Propagate the trace context on every outbound call and message, such as
  in HTTP headers or queue metadata
- Propagate it in a format the receivers accept, such as W3C Trace Context
  or B3 through OpenTelemetry propagators
- Include the trace ID in every log entry for that request — use the same
  field name across all services, such as `trace_id`
- Instrument through a vendor-neutral API, such as OpenTelemetry; avoid
  vendor-specific SDKs in application code
- Choose the telemetry backend in configuration, never in application code
- Create spans for inbound requests, outbound calls, database queries,
  cache operations and background job execution
- Keep span names low-cardinality (MUST) — use route templates, not URLs
  with IDs (e.g. `GET /users/{id}`, not `GET /users/42`)

## Health check

- Expose a health check the orchestrator or load balancer probes
- Report healthy when the service is ready to handle traffic
- Report unhealthy when a dependency no request can be served without,
  such as the primary database, is unavailable
- Never fail the health check on an optional dependency, such as a
  cache: every instance leaves rotation at once (MUST NOT)
- Never require authentication for the health check (MUST NOT)
- Make the health check the first thing that passes before traffic is
  routed to a new instance (MUST)

## Error visibility

- Return the trace or request ID in every error response, so a client can
  report it to support
- Never expose internal state, stack traces, or file paths in error responses
