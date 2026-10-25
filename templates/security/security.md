# Base — Application Security

[ID: base-security]

Apply these cross-cutting security rules to application code in every
project, regardless of language or framework.

The sections below cover the OWASP Top 10 categories: injection, broken
access control, cryptographic failures, insecure design, security
misconfiguration, vulnerable components, identification and authentication
failures, software and data integrity failures, logging and monitoring
failures, and server-side request forgery.

## Input validation

[ID: security-input]

- Validate all external input at the system boundary — the first point
  where untrusted data enters the application
- Validate complex input with a schema validation library; never
  hand-write it
- Use an allowlist, not a blocklist — define what is valid, reject
  everything else
- Reject invalid input with a clear error; do not silently coerce or strip
  fields
- Do not repeat the boundary's schema validation in inner layers; a
  function still asserts the preconditions it relies on

## Output encoding (XSS)

[ID: security-output]

- Encode dynamic data for its rendering context at the point of output:
  HTML, URL, JavaScript, SQL, shell
- Encode on output, not on input — store the raw value, encode when
  rendering
- Use the encoding the framework or template engine provides
- Never insert user-supplied data through a raw-HTML path that bypasses
  auto-escaping
- Apply the encoding that matches each context; HTML encoding does not
  prevent URL injection

## Injection prevention

[ID: security-injection]

- Use parameterized queries for all database access; never concatenate user
  input into SQL strings
- Escape shell arguments when invoking external commands, or use API
  alternatives that do not invoke a shell
- Never pass user input to dynamic code execution, such as an `eval`

## Authentication

[ID: security-authn]

- Hash passwords with a modern algorithm: bcrypt, scrypt, or Argon2 — never
  MD5, SHA-1, or plain SHA-256
- Require a minimum password length and reject known-breached passwords;
  never impose composition rules (NIST SP 800-63B)
- Use constant-time comparison for secrets and tokens; timing attacks leak
  information through response time
- Lock accounts or throttle after repeated failed attempts

## Session management

[ID: security-sessions]

- Generate session IDs with a cryptographic random generator
- Regenerate the session ID after login; this prevents session fixation
- Set cookie flags: `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict` for
  sensitive applications)
- Expire sessions after an idle period: 30 minutes for sensitive
  applications, configurable otherwise
- Invalidate sessions on logout; do not rely on cookie expiry alone

## Cross-site request forgery (CSRF)

[ID: security-csrf]

- Give every state-changing request a CSRF defence (MUST) when the session
  is authenticated by an ambient credential
- Treat as ambient any credential the browser attaches on its own: a
  cookie, HTTP Basic, or a client certificate
- Use the framework's built-in CSRF middleware; never hand-roll token
  generation or comparison
- Treat `SameSite=Lax` on the session cookie as defence in depth, not the
  defence; it does not cover top-level `POST` navigation on older browsers,
  and a subdomain takeover defeats it
- Prefer the synchroniser token pattern
- Use the signed double-submit cookie where the server holds no session
  state, with the token bound to the session identifier
- Validate the token on every `POST`, `PUT`, `PATCH` and `DELETE`, never on
  `GET`
- Never change state on a `GET` request (MUST NOT)
- Treat an API authenticated only by a bearer token the client attaches
  explicitly as needing no CSRF token; the browser never adds that header
  on its own
- Require a CSRF token on a bearer-token API that also accepts cookie
  authentication

## Secrets in code

[ID: security-secrets]

- Never hardcode secrets, API keys, tokens, or credentials in source files
- Keep local secret files out of version control
- Rotate a secret immediately if it is accidentally committed; removing it
  from git history is not sufficient, since the secret is compromised

## Transport security

[ID: security-transport]

- Use HTTPS everywhere, with no exceptions for production traffic
- Enable HSTS on all production sites (MUST), with `includeSubDomains` and
  a minimum `max-age` of one year
- Require TLS 1.2 as the minimum version; disable TLS 1.0 and 1.1
- Use strong cipher suites; disable known-weak ciphers

## Security headers

[ID: security-headers]

- Set security headers on every HTTP response at the reverse proxy or
  middleware level, not per route
- Set these required headers:
  - `Content-Security-Policy` — start strict, relax only what a page needs
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY` (or CSP `frame-ancestors`)
  - `Strict-Transport-Security` (see Transport security)
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy` — disable unused browser APIs
- Map each static asset type to its `Content-Type` in code when enabling
  `nosniff`; the browser then never corrects a wrong one
- Never let MIME resolution depend on the host when `nosniff` is enabled
  (MUST NOT)
- When enabling `nosniff`, verify script and style execution in a real
  browser, not just status codes
- Never use `unsafe-inline` or `unsafe-eval` in CSP without a written
  justification
- Do not expose server version or technology stack in headers; remove
  `X-Powered-By`, `Server` version strings

## Error handling

[ID: security-errors]

- Never expose stack traces, internal paths, or database errors to end
  users; return generic error messages externally
- Log full error details server-side for debugging
- Use consistent error response formats; do not leak internal structure
  through varying error shapes
- Return each error through the protocol's own error signal, never as a
  success
- Do not reveal whether a resource exists via error messages: login errors
  should say "invalid credentials", not "user not found" vs "wrong password"

## Logging

[ID: security-logging]

- Never log secrets, tokens or passwords
- Never log personally identifiable information (PII), except the client
  IP in the security log below
- Sanitize log output; user-supplied data in logs can enable log injection
  attacks
- Log security-relevant events: authentication attempts, access denials,
  privilege changes, configuration changes
- Include enough context for investigation: timestamp, an opaque user ID,
  action, result; never a name, email or submitted username
- Record the client IP only in the security log, access-restricted and
  purged at the end of its retention period
- Retain security logs for a defined period; compliance may require 90
  days to 7 years

## CORS

[ID: security-cors]

- Restrict `Access-Control-Allow-Origin` to specific known origins; never
  use `*` for authenticated endpoints
- Do not reflect the `Origin` header back as `Access-Control-Allow-Origin`
  without validation
- Restrict allowed methods and headers to what the API actually needs

## Deserialization and data integrity

[ID: security-integrity]

- Never deserialize untrusted data with a format that can instantiate
  arbitrary types; use a data-only format such as JSON
- Validate the structure and types of deserialized data before use; treat
  it as untrusted input
- Verify integrity of downloaded artifacts, updates, and dependencies; use
  checksums or digital signatures
- Pin dependency versions and verify checksums in lockfiles; do not trust
  upstream registries blindly
- Use pinned, verified steps and images in CI/CD pipelines (MUST)
- Never pull `latest` tags in production CI/CD pipelines

## Server-Side Request Forgery (SSRF)

[ID: security-ssrf]

- Never pass user-supplied URLs directly to server-side HTTP clients;
  validate and sanitize first
- Allowlist permitted destination hosts and schemes; reject anything not
  on the list
- Block a request whose resolved address is not public, in IPv4 and IPv6
  alike: loopback, private, link-local, unique-local, shared, unspecified,
  multicast and reserved ranges
- Unwrap an IPv4-mapped IPv6 address (`::ffff:127.0.0.1`) to its IPv4
  form before classifying it
- Classify with an address library, never a hand-kept CIDR list
- Use the standard library's address module where the runtime has one,
  and a maintained external library where it has none
- Test each excluded category by its own predicate; a library's single
  "is public" test can still admit multicast
- Resolve the hostname once, validate the IP, and connect only to that
  address; a client that resolves the name again can be rebound by DNS
- Keep TLS verifying the certificate against the original hostname when
  the connection is pinned to the validated address
- Disable HTTP redirects in server-side HTTP clients, or resolve and
  validate each redirect's destination the same way
- Limit response size and timeout for outbound requests to prevent
  resource exhaustion

## File uploads

[ID: security-uploads]

- Validate file type by content (magic bytes), not by extension or MIME
  type; both are trivially spoofed
- Enforce maximum file size at the boundary
- Store uploads outside the web root; never serve user uploads from the
  same domain without sanitization
- Generate random filenames; do not use the original filename (path
  traversal risk)
- Scan uploaded files for malware if the application serves them to other
  users

## Agent secrets handling

[ID: security-agent-secrets]

- Never read, print, or cat files that may contain secrets (MUST NOT):
  `.env`, `credentials.json`, `*-key*`, `*.pem`, `*.key`,
  `serviceaccount.json`, `secrets.yaml`
- Never echo, log, or display environment variable values (MUST NOT)
- Check a variable's presence by its exact name without printing its value,
  and treat a set but empty variable as absent
- Never include secret values in commit messages, PR descriptions, or
  conversation output (MUST NOT)
- Warn the user (MUST) before committing files that commonly contain
  secrets (`.env`, `credentials.json`, private keys)
- Verify a secret's presence by a match count or an existence check,
  never by printing it
- Flag a secret exposed in a session to the user immediately: name the
  exposed secret, recommend immediate rotation, and note that session
  history may be cached or logged
