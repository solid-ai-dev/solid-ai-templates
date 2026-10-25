# Backend — Authentication and Authorization
[ID: backend-auth]
[DEPENDS ON: templates/security/security.md, templates/backend/http.md]

Rules for identity verification (authn) and access control (authz).
Applies to any backend service that has protected resources.
Extends `security/security.md`, "Authentication" (`security-authn`) and
"Session management" (`security-sessions`), with backend-specific depth.

## General principles

- Keep authentication (who are you?) and authorization (what can you do?)
  in separate layers; they are separate concerns
- Never implement your own cryptographic primitives — use well-audited libraries
- Fail closed: deny access by default; grant explicitly
- Centralise auth logic; never scatter permission checks across route handlers

## Authentication
[EXTEND: security-authn]

- Prefer delegating authentication to an identity provider (IdP) over
  rolling your own
- Expire an access token within 15 minutes when the service issues tokens
  itself
- Issue refresh tokens only to user sessions, such as a browser or mobile
  client; rotate each on use and expire it within 7 days
- Never issue a refresh token to a service
- Authenticate a service by credentials of its own, such as OAuth 2.0
  client credentials, mutual TLS or a scoped API key (below)
- Validate every signed token's signature, expiry, issuer and audience
- Reject a token that lacks any required claim
- Store refresh tokens server-side, in a database or a dedicated session
  store, so they can be revoked; stateless refresh tokens cannot be
  invalidated before expiry

## Token transport
[ID: backend-auth-token-transport]

- Send access tokens in the `Authorization: Bearer <token>` header (MUST)
- Do NOT accept tokens in query parameters — they appear in server logs and
  browser history
- Store a browser client's refresh tokens in `httpOnly`, `Secure`,
  `SameSite=Strict` cookies (MUST)
- Never store refresh tokens in `localStorage` or JavaScript-accessible memory

## Authorization

- Use role-based access control (RBAC) as the baseline (SHOULD):
  assign permissions to roles, assign roles to users
- Add attribute-based access control (ABAC) as a layer on top of RBAC for
  fine-grained needs
- Replace RBAC with ABAC only with a reason in a decision record
- Enforce authorization at the service layer, not only at the route layer;
  a route that passes auth may call a service that operates on another
  user's data
- Never trust client-supplied IDs for ownership checks — always verify that
  the authenticated user owns or has access to the requested resource

## API keys (service-to-service)

- Issue API keys with the minimum required scope
- Hash API keys before storing — treat them like passwords
- Rotate API keys on a schedule and immediately on suspected compromise
- Log every API key usage with the key ID (not the key value) and the
  calling service identity

## Observability

- Log authentication failures at WARN to the security log, with IP and
  user agent
- Name the account by its opaque user ID when it exists; never log the
  submitted username or password
- Log authorization failures at WARN with user ID, resource, and action
- Alert on a spike in auth failures; it may indicate a credential stuffing
  attack

## Testing

- Cover permission logic with unit tests for all role combinations,
  including edge cases (no role, multiple roles, deprecated role)
- Assert in an integration test that a protected endpoint rejects an
  unauthenticated request with an unauthenticated status, such as HTTP 401
- Assert in an integration test that it rejects an authenticated request
  lacking permission with a permission-denied status, such as HTTP 403
- Test token expiry: assert that an expired token is rejected
- Test token revocation where refresh tokens exist: assert that a revoked
  refresh token cannot obtain a new access token
