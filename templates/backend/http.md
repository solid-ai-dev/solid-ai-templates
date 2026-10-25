# Backend — HTTP Conventions
[ID: backend-http]

## Port binding

- Read the port from an environment variable such as `PORT`; never
  hardcode it (MUST)
- Use a well-known default in development, and the port the platform
  assigns in production

## Process lifecycle

- Start fast — keep initialisation short (MUST)
- Shut down gracefully on a stop signal (`SIGTERM`) in order: stop
  accepting new requests, let in-flight ones finish until the drain
  deadline, cancel what remains, wait up to a bounded cancellation period,
  release resources, then exit (MUST)
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
- Keep no state in process memory that a restart cannot rebuild; put it in
  an external store, so any instance can be replaced

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

## Query parameters

- Parse a typed query parameter explicitly so you can distinguish three
  states: absent (use the default), present-and-valid (use it), and
  present-but-invalid (raise 400)
- Never rely on a parsing helper that returns the default on a malformed
  value; it silently turns a client error into a successful default-valued
  200

## Request headers

- Read every header name case-insensitively, as RFC 9110 defines them
  (MUST)
- Avoid the `X-` prefix on custom headers (SHOULD NOT); RFC 6648
  deprecated this convention
- Use a vendor or application-specific prefix on a custom header instead
  (SHOULD)

## HTTP methods

- Never let a GET or HEAD request change resource state; RFC 9110 defines
  both as safe
- Make every PUT and DELETE idempotent, as RFC 9110 defines them

## Resource representation

- Make a text payload's field types conform to the relevant ISO standard
  (MUST):
  - Date and time values: ISO 8601
  - Language codes: ISO 639
  - Country codes: ISO 3166-1 alpha-2
  - Currency codes: ISO 4217
- Serialise any JSON integer outside ±(2^53 − 1), -9007199254740991 to
  9007199254740991, as a string (MUST); JavaScript cannot represent one
  beyond that range precisely, in either direction
- Reject non-finite values in an endpoint that serialises computed floats
  to JSON (MUST); `NaN`/`Infinity` are not valid RFC 8259 JSON
- Configure the encoder to reject them, so it fails loud at the
  serialisation boundary (a 500) instead of emitting a bare `NaN` token
  that strict parsers reject
- Represent an undefined computed float as `null`, normalised before
  serialisation
- Document such a field as nullable in the contract
- Return only the fields the caller needs (MUST); never pad a payload
  with fields that are not consumed

## Error responses

- Use consistent error response shape across all endpoints
- Never return stack traces, internal paths, or implementation details to the
  client
- Use 4xx for client errors, 5xx for server errors — never use 200 for errors
- Carry a gRPC or GraphQL error the way its protocol defines instead: a
  gRPC status code over HTTP 200, a GraphQL `errors` array under
  GraphQL-over-HTTP's status rules
- Set an explicit `Content-Type` on every JSON response

## Authentication and authorisation

- Serve all API traffic over HTTPS outside local development (MUST);
  plain HTTP is not acceptable in staging or production
- Give access tokens a short, finite lifetime (MUST)
- Enforce both authentication and authorisation on every external API
  endpoint (MUST), except a public endpoint the project declares
- Make a public endpoint only a declared read, or a declared write that
  must run before the caller has an identity, such as a sign-up, sign-in,
  account recovery or a contact form
- Declare each public endpoint in the route definition and the API
  contract, in the change that makes it public; a public catalogue stays
  public, the account records beside it stay protected
- Require authentication at minimum on internal API endpoints (SHOULD)
- Never make any other write endpoint accessible without a valid
  authenticated identity (MUST NOT)
- Apply authentication and authorisation before any business logic runs
- Rate-limit each public endpoint per client — never expose an unbounded
  write operation
- Return no account data from a public write
- Rate-limit a sign-in or recovery endpoint per account and per client
- Answer a sign-up or recovery request the same way, in content and
  timing, whether or not the account exists
- Make each recovery token single-use, short-lived and bound to one account
