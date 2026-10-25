# Backend — Inbound Webhook Handling
[ID: backend-webhooks]
[DEPENDS ON: templates/backend/http.md, templates/backend/messaging.md]
[DEPENDS ON: templates/security/security.md, templates/backend/observability.md]

Rules for receiving provider callbacks under bursty load, on top of the
messaging rules for idempotency, retries, DLQs and backpressure.

## Intake

- Expose one intake URL per provider; never multiplex providers onto one
  endpoint
- Scope failures, authentication and metrics to that URL

## Verify at the edge

- Authenticate each delivery before any work, with the provider's
  credential, such as a signature, a shared token or a client certificate
- Reject a forged or malformed delivery before parsing, persisting or
  enqueueing it
- Check a body signature against the exact bytes received, never a
  re-serialised copy

## Respond fast

- Return 2xx within the provider's timeout: acknowledge, then process
  asynchronously; never run heavy work inline on the request path
- Persist or enqueue the event before responding so an acknowledged
  event is never lost

## Survive provider retries

- Assume a non-2xx response or a timeout brings a resend; a slow or
  failing handler then multiplies inbound load
- Return 2xx for an event skipped on purpose (duplicate, irrelevant)
- Return 5xx only where redelivery is wanted
- Deduplicate on a stable event key, such as the provider's event ID; the
  same event can arrive more than once

## Testing
[EXTEND: base-testing]

- Test authentication rejection: a tampered body or a missing or invalid
  credential MUST be rejected before any side effect occurs
- Test idempotency: deliver the same event twice and assert a single effect
- Test the fast-ack path: the handler returns 2xx without waiting for
  downstream processing to complete
