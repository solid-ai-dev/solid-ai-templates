# Backend — HTTP Conventions
[ID: backend-http]

## Port binding

- Bind the service to a port the process opens itself; never depend on a
  web server injected at runtime
- Read the port from an environment variable such as `PORT`; never
  hardcode it (MUST)
- Use a well-known default in development, and the port the platform
  assigns in production

## Process lifecycle

- Start fast — keep initialisation short (MUST)
- Shut down gracefully on `SIGTERM` in order: stop accepting new
  requests, let in-flight ones finish until the drain deadline, cancel
  what remains, wait up to a bounded cancellation period, release
  resources, then exit (MUST)
- Release resources when the cancellation period ends, even when some
  cancelled work is still running
- Force-exit when the whole shutdown, from draining to releasing
  resources, passes its hard deadline (MUST)
- Set the drain deadline plus the cancellation period below the hard
  deadline, leaving time to release resources
- Fit the hard deadline inside the grace period the platform allows
  before it kills the process
- Recover cleanly when a process is killed without warning (`SIGKILL`,
  power loss) (MUST)
- Keep no state in the process; use external stores, so any instance can
  be replaced

## Admin processes

- Run one-off tasks (migrations, data fixes, REPL sessions) with the
  application's code, config and dependencies (MUST)
- Commit admin scripts to the repository; never run them as ad-hoc shell
  commands (MUST)
- Prefer idempotent scripts — safe to re-run
- Never run an admin task against production without a tested rollback plan

## Handler design

- Keep handlers thin: decode request → call service → encode response
- Never put business logic in a handler; delegate it to a service layer
- Validate all incoming request data before processing
- Set a timeout on every outbound call (HTTP clients, database queries)

## URI design

A project's own API style guide governs naming; without one, use these
defaults.

- Name resources with nouns, never verbs: `/orders` not `/getOrders`
- Use plural nouns for collections: `/orders`, `/products`
- Address an individual resource under its collection: `/orders/{orderId}`
- Nest a sub-resource under its parent: `/customers/{id}/orders`
- Write path segments in lowercase with hyphens between words (SHOULD)
- End no URI with a trailing slash (SHOULD)
- Spell path words in full, in one variant of English (SHOULD)

## Query parameters

- Name query parameters in one case across the API, camelCase by default
  (SHOULD)
- Use query parameters for filtering, sorting, and pagination
- Never use a query parameter for resource identity; use a path segment
  for that
- Reserve one set of names for pagination and expansion, such as `limit`,
  `offset` and `expand`, and never repurpose them
- Parse a typed query parameter explicitly so you can distinguish three
  states: absent (use the default), present-and-valid (use it), and
  present-but-invalid (raise 400)
- Never rely on a framework's type-coercing helper that returns the
  default on a malformed value (e.g. Flask
  `request.args.get('n', type=int)`); it silently turns a client error
  into a successful default-valued 200

## Request headers

- Spell a header name in Hyphenated-Pascal-Case in specs and docs, such as
  `Api-Correlation-Id`
- Leave a header's case on the wire to the HTTP library; HTTP/2 and HTTP/3
  require lowercase (RFC 9113)
- Read every header name case-insensitively, as RFC 9110 defines them
  (MUST)
- Avoid the `X-` prefix on custom headers (SHOULD NOT); RFC 6648
  deprecated this convention
- Use a vendor or application-specific prefix on a custom header instead
  (SHOULD)

## HTTP methods

| Method | Use for | Idempotent |
|--------|---------|-----------|
| GET | Retrieve a resource or collection — no side effects | Yes |
| POST | Create a new resource — server assigns URI | No |
| PUT | Replace a resource entirely | Yes |
| PATCH | Partially update a resource | No |
| DELETE | Remove a resource | Yes |

## Resource representation

These rules apply to a REST endpoint. A gRPC call carries protobuf
messages and a GraphQL request its own response format, each under its
specification.

- Use JSON as the default serialisation format (MUST)
- Use XML where the consuming system explicitly requires it (MAY)
- Make field types conform to the relevant ISO standard (MUST):
  - Date and time values: ISO 8601
  - Language codes: ISO 639
  - Country codes: ISO 3166-1 alpha-2
  - Currency codes: ISO 4217
- Serialise any integer outside ±(2^53 − 1), -9007199254740991 to
  9007199254740991, as a string (MUST); JavaScript cannot represent one
  beyond that range precisely, in either direction
- Reject non-finite values in an endpoint that serialises computed floats
  (MUST); `NaN`/`Infinity` are not valid RFC 8259 JSON
- Configure the encoder to reject them (e.g. `allow_nan=false`) so it
  fails loud at the serialisation boundary (a 500) instead of emitting a
  bare `NaN` token that strict parsers reject
- Represent an undefined computed float as `null`, normalised before
  serialisation
- Document such a field as nullable in the contract
- Return only the fields the caller needs (MUST); never pad a payload
  with fields that are not consumed

## HATEOAS

- Embed hyperlinks in responses to enable resource discovery (SHOULD)
- Use the project's link format; without one, a `links` array with `href`,
  `rel`, `type`, and `media` fields:
  ```json
  "links": [
    {
      "href": "invoices/f9c3b2a1-0d4e-4f8b-9c7a-1e2d3f4a5b6c",
      "rel": "invoice",
      "type": "paymentSummary",
      "media": "application/pdf"
    }
  ]
  ```
- Support at minimum: `self`, `next`, `prev` relations on paginated collections

## Error responses

- Use consistent error response shape across all endpoints
- Never return stack traces, internal paths, or implementation details to the
  client

### REST and JSON errors

These rules apply to a REST endpoint. A gRPC call carries its error
in a gRPC status code, sent over HTTP 200; a GraphQL request carries it
in the response's `errors` array, under GraphQL-over-HTTP's status rules.

- Follow RFC 9457 (`application/problem+json`) for error format
- Use 4xx for client errors, 5xx for server errors — never use 200 for errors
- Set an explicit `Content-Type` on every JSON response:
  `application/problem+json` on an error, `application/json` otherwise

## Authentication and authorisation

- Serve all API traffic over HTTPS outside local development (MUST);
  plain HTTP is not acceptable in staging or production
- Give access tokens a finite lifetime (MUST)
- Use JWT or an equivalent short-lived token mechanism for access tokens
- Enforce both authentication and authorisation on every external API
  endpoint (MUST), except a read endpoint the project declares public
- Declare each public endpoint in the route definition and the API
  contract, in the change that makes it public; a public catalogue stays
  public, the account records beside it stay protected
- Require authentication at minimum on internal API endpoints (SHOULD)
- Never make a write endpoint accessible without a valid authenticated
  identity (MUST NOT)
- Apply authentication and authorisation before any business logic runs
- Rate-limit public endpoints — never expose an unbounded write operation
