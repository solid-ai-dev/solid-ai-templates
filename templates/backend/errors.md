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
| **Infrastructure** | Required DB or queue unavailable | 503 | ERROR |
| **External** | Third-party API or service failure | 502, 504 | ERROR |
| **Unexpected** | Unhandled exception, programming error | 500 | ERROR |

- Never map an infrastructure or unexpected error to a 4xx; it blames the
  caller
- Never map a validation error to a 5xx; the caller must learn the request
  was rejected

## Propagation through layers

- Raise or return typed errors from data-access code (`RecordNotFound`,
  `ConnectionError`); never expose a storage library's errors above it
- Translate them into domain errors with business context (`OrderNotFound`,
  `PaymentServiceUnavailable`)
- Map domain errors to responses in one central mapper; never map them in
  each handler

## Recovery and graceful degradation

- Wrap repeated calls to an external service in a circuit breaker
- Make the breaker fail fast past a failure threshold and recover after a
  cool-down
- Serve a reduced response, such as cached data, when a non-critical
  dependency is down
- Leave the system consistent when a non-idempotent operation fails midway
  (MUST): use transactions or compensating actions

## External service failures

- Never pass a third-party error message to the caller
- Translate a third-party error into a domain error with a message you
  control
- Return 504 when an external call times out and 502 when it is refused
- Retry a transient external failure with exponential backoff and jitter,
  only where repeating the call is safe
- Treat an idempotent call as safe to repeat
- Treat any other call as safe to repeat only when every attempt reuses
  one idempotency key
- Count that key only where the destination honours it for the whole
  retry window
- Never retry an external 4xx other than 408 or 429
- Wait at least as long as a `Retry-After` header asks

## Unexpected errors

- Catch every unhandled error at the outermost handler layer (MUST); none
  reaches the framework's default handler
- Treat every unexpected error as a bug to fix; never suppress it
