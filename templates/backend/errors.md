# Backend — Error Handling
[ID: backend-errors]
[DEPENDS ON: templates/backend/http.md, templates/backend/observability.md]

Classification, propagation and recovery of errors; the response format
and logging rules come from the HTTP and observability templates.

## Error classification

Classify every error before handling it; the class sets the response, the
log level and the recovery:

| Class | Cause | HTTP range | Log level |
|-------|-------|------------|-----------|
| **Validation** | Invalid input from the caller | 400, 422 | INFO |
| **Authentication** | Missing or invalid credentials | 401 | WARN |
| **Authorization** | Valid credentials, insufficient permission | 403 | WARN |
| **Not found** | Resource does not exist | 404 | INFO |
| **Conflict** | State violation (duplicate, stale write) | 409 | INFO |
| **Infrastructure** | DB, cache, or queue unavailable | 503 | ERROR |
| **External** | Third-party API or service failure | 502, 504 | ERROR |
| **Unexpected** | Unhandled exception, programming error | 500 | ERROR |

- Never map an infrastructure or unexpected error to a 4xx; it blames the
  caller
- Never map a validation error to a 5xx; the caller must learn the request
  was rejected

## Propagation through layers

- Raise typed errors from data-access code (`RecordNotFound`,
  `ConnectionError`); never expose ORM or driver exceptions above it
- Re-raise them as domain errors with business context (`OrderNotFound`,
  `PaymentServiceUnavailable`)
- Map domain errors to HTTP responses in one central mapper; no ad-hoc
  `try/except` per route
- Log an error once, at the handler or middleware boundary

## Recovery and graceful degradation

- Put a timeout on every outbound call (HTTP, DB, cache, queue)
- Wrap repeated calls to an external service in a circuit breaker: fail
  fast past a failure threshold, recover after a cool-down
- Serve a reduced response when a non-critical dependency is down, such as
  cached data, rather than fail the request
- Leave the system consistent when a non-idempotent operation fails midway
  (MUST): use transactions or compensating actions

## External service failures

- Never pass a third-party error message to the caller; translate it into
  a domain error with a message you control
- Return 504 when an external call times out and 502 when it is refused
- Log the full external error at ERROR level; return the caller only a
  safe, generic message
- Retry transient external failures with exponential backoff and jitter;
  never retry an external 4xx

## Unexpected errors

- Catch every unhandled exception at the outermost middleware (MUST); none
  reaches the framework's default handler
- Return a generic 500 with a trace ID; never a stack trace, internal path
  or message that reveals implementation details
- Treat every unexpected error as a bug — create a ticket, do not suppress
