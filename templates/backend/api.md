# Backend — API Design
[ID: backend-api]
[DEPENDS ON: templates/backend/http.md]

## API-first
- Design API-first (MUST): agree and document the public contract before
  implementation begins (MUST), so client teams work in parallel and the
  API is testable without a frontend
- Record any deviation from API-first in a decision record with its
  justification (MUST)

## Protocol selection
[ID: backend-api-protocols]

| Protocol  | Use when                                                                                            |
|-----------|-----------------------------------------------------------------------------------------------------|
| REST      | Default. External APIs, browser/mobile clients, third-party integrations, ops/admin endpoints       |
| gRPC      | Internal service-to-service, performance-critical paths, streaming, polyglot teams sharing a schema |
| GraphQL   | Frontend-facing APIs where clients need flexible querying and over-fetching is a real problem       |
| WebSocket | Real-time push, bidirectional streams where HTTP polling is not viable                              |
| Messaging | Async, fire-and-forget, event-driven                                                                |

- Start with REST; deviate only with a reason in a decision record
- Combine REST for external and ops endpoints with gRPC for internal hot
  paths (MAY)
- Justify any other pair of API styles in one service in a decision
  record; two surfaces double the maintenance
- Never use gRPC as the primary interface for browser clients

## API contract
- Give every API the machine-readable contract of its kind, even when it
  runs over HTTP (MUST):
  - an OpenAPI specification for REST
  - protobuf for gRPC
  - a GraphQL schema
  - a message schema for messaging
- Keep the contract current (MUST); a stale contract is worse than none
- Cover every resource, operation, parameter, response schema, error
  response and authentication requirement in the contract
- Keep a changelog of API changes across versions
- Assert that the enums, operations and error codes in code match the
  contract, so drift fails a test, not a consumer
- Contract-test a running instance against cases generated from the
  contract
- Give the contract a revision of its own, apart from the package version
  and from the API version
- Bump the contract revision for every contract change, additive ones
  included; never bump it for a release that leaves the contract unchanged

## Versioning
- Keep every API version backward compatible (MUST)
- Version the API in the URI path prefix: `/v1/`, `/v2/`
- Start at `v1`; introduce `v2` only when a breaking change is unavoidable
- Use a custom request header (`Api-Version: 2`) where a path prefix does
  not fit
- Never version through the media type (MUST NOT)

## Backward compatibility
- Release a new API version for every breaking change: a removed or
  renamed response field, a changed field type, a switched auth scheme
- Treat as breaking, too, a changed verb or path, wire protocol or
  Content-Type, and business logic that changes observable results
- Never bump the API version for an additive change (MUST NOT): a new
  optional field, endpoint, verb or query parameter keeps `/v1/` and moves
  only the contract revision

## Deprecation strategy
When a breaking change is introduced:

1. Deploy the new version alongside the old one
2. Add the `Deprecation` header to all responses from the old version with
   the Unix timestamp of when deprecation started:
   `Deprecation: @<unix-timestamp>`
3. Optionally add the `Sunset` header with the planned removal date:
   `Sunset: <HTTP-date>`
4. Notify all consumers and agree on a migration timeline
5. Remove the old version only after the sunset date has passed; without
   a `Sunset` header, only after the timeline agreed in step 4 ends

## Statelessness
[ID: backend-api-statelessness]
- Keep APIs stateless (MUST): store no client context on the server
  between requests
- Carry everything a request needs in the request itself (MUST)
- Keep session state in the client or a dedicated session store, never in
  the API service

## Pagination
- Paginate every collection endpoint (MUST); never return an unbounded list
- Use `limit` and `offset` (or cursor-based) pagination
- Include navigation links or cursors (`next`, `prev`) in the response
