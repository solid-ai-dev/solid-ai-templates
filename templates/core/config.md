# Base — Configuration

[ID: base-config]

Store configuration in the environment, not in code, after the
[12-factor app](https://12factor.net/config).

## Sources

- Supply every value that varies by deployment through a source the
  precedence below lists; keep defaults in code only for optional settings
- Read every secret from the environment or a secrets manager, never from a
  committed file or a command-line flag (MUST)
- Commit an example configuration file with placeholder values; never
  commit the file that holds the real values
- Keep separate configuration for each environment the project runs, such
  as development, testing, staging and production
- Pass configuration to components explicitly; never read a global config
  object from arbitrary places

## Naming

- Name environment variables in `SCREAMING_SNAKE_CASE`
- Prefix each with the app or service name, such as `MYAPP_DATABASE_URL`

## Precedence

Sources override in this order, highest last:

1. Defaults in code
2. A config file, such as `config.yaml` or `appsettings.json`
3. Environment variables
4. CLI flags and arguments

- Document the precedence model the project uses
- Never let a lower-priority source silently override a higher one
- Treat a source that is present but empty as an error naming the accepted
  input, never as absent (MUST): an empty flag, environment variable or
  config key never falls back to a lower-priority value

## Validation

- Validate every value's type, range and format at load time, optional
  ones included, never at first use
- Fail fast on a missing required value or an invalid one
- Read configuration through a typed object or schema; never scatter raw
  environment reads across the code
- Never give a secret a default (MUST NOT)
- Require a secret whenever the capability that uses it is enabled, and
  only then: disabled mail delivery needs no provider key
- Fail at startup when an enabled capability lacks its secret, naming both;
  never fall back silently to running without the capability

## Build time and run time

- Put into the artifact only values the same in every environment, such
  as public keys
- Read the rest at start or per request: API base URLs, feature flags,
  secrets, database URLs, log levels
- Never put a secret in build-time config (MUST NOT); it ships inside the
  artifact
- Document which variables are build-time and which are runtime

## Secrets

- Source production secrets from a secrets manager or the CI secret store,
  never from a plain file on the host
- Give automated tests stub secrets, never real ones
- Load secrets so they can rotate without a redeployment
- Never log a secret; redact or omit it from logs and diagnostics
- Reference a secret by name or path; never embed it in a config file

## Dependencies

[LOAD: add-dependency]

- Declare every dependency in a manifest, such as `package.json`,
  `pyproject.toml`, `go.mod` or `Cargo.toml`
- Run with only the declared dependencies installed; never rely on
  system-wide packages (MUST)

## Example

```text
# Required
MYAPP_API_BASE_URL=http://localhost:8000
MYAPP_SECRET_KEY=change-me

# Optional, defaults shown
MYAPP_LOG_LEVEL=info
MYAPP_ENABLE_DEBUG=false

# Required only while MYAPP_ENABLE_MAIL is true
MYAPP_ENABLE_MAIL=false
# MYAPP_MAIL_API_KEY=change-me
```
