# Backend — Inbound Webhook Handling
[ID: backend-webhooks]
[DEPENDS ON: templates/backend/http.md, templates/backend/messaging.md]
[DEPENDS ON: templates/security/security.md, templates/backend/observability.md]

Rules for receiving provider callbacks under bursty load, on top of the
messaging rules for idempotency, retries, DLQs and backpressure.

## Intake

- Expose one intake URL per provider or connection; never multiplex
  providers onto one endpoint
- Scope failures, signature handling and metrics to that URL

## Verify at the edge

- Verify the provider signature before any work; reject a forged or
  malformed payload before parsing, persisting or enqueueing it
- Verify the exact bytes received, never a re-serialised copy
- Treat the raw body as untrusted until its signature checks out

## Respond fast

- Return 2xx within the provider's timeout: acknowledge, then process
  asynchronously, never inline on the request path
- Persist or enqueue the event before responding so an acknowledged
  event is never lost

## Survive provider retries

- Expect a non-2xx response to make the provider resend, so a slow or
  failing handler multiplies inbound load
- Return 2xx for an event skipped on purpose (duplicate, irrelevant)
- Return 5xx only where redelivery is wanted
- Deduplicate on the provider's event ID; at-least-once delivery sends the
  same event more than once

## Testing
[EXTEND: base-testing]

- Test signature rejection: a tampered body or invalid signature MUST be
  rejected before any side effect occurs
- Test idempotency: deliver the same event twice and assert a single effect
- Test the fast-ack path: the handler returns 2xx without waiting for
  downstream processing to complete
