# Stack — Go Service
[DEPENDS ON: templates/stack/go-lib.md, templates/core/config.md, templates/backend/http.md, templates/backend/database.md, templates/backend/observability.md, templates/backend/errors.md, templates/backend/quality.md, templates/backend/concurrency.md, templates/backend/features.md, templates/backend/messaging.md, templates/infra/cicd.md, templates/security/devsecops.md]

Extends the Go library stack with service-specific rules. Covers project
structure, HTTP handlers, configuration, concurrency, graceful shutdown,
and deployment.

---

## Stack
[ID: go-service-stack]
[OVERRIDE: go-lib-stack]

- Language: Go 1.22+
- HTTP router: [net/http (stdlib) / chi / gin / echo]
- Database: [database/sql + pgx / sqlc / GORM]
- Config: [github.com/caarlos0/env / viper / godotenv]
- Test runner: go test (stdlib)
- Containerisation: Docker
- Distribution: [binary / Docker image / GitHub Releases]

---

## Project structure
[ID: go-service-structure]

```
cmd/
  [service]/
    main.go              # entry point — wires dependencies, starts server
internal/
  [feature]/
    handler.go           # HTTP handlers (thin)
    service.go           # business logic
    repository.go        # data access
    model.go             # domain types
  config/
    config.go
  server/
    server.go            # HTTP server setup, middleware, routing
pkg/                     # code safe to import by external packages (if any)
migrations/              # SQL migration files
Dockerfile
Makefile
go.mod
go.sum
README.md
CLAUDE.md
```

- `internal/` enforces encapsulation — external packages cannot import it
- `cmd/` is thin — no business logic, only wiring

---

## HTTP handlers
[ID: go-service-http]
[EXTEND: backend-http]

- Decode request body explicitly — never trust unvalidated input
- Use `http.Error()` or a JSON encoder for all error responses
- Handlers are thin — delegate all logic to service functions

---

## Configuration
[EXTEND: base-config]

- One `Config` struct in `internal/config/config.go` — loaded from env
  vars at startup; passed explicitly through the dependency graph
- Never read `os.Getenv` directly in application code outside of
  the config loader

---

## Concurrency
[EXTEND: backend-concurrency]

- Protect shared state with `sync.Mutex` or `sync.RWMutex` — document
  which fields are guarded and by which lock
- Always use `context.Context` as the first argument in functions that may block
- Use `errgroup` for structured concurrency — all goroutines started in
  `main.go` under one group, stopped cleanly on context cancellation
- Never start a goroutine without a clear owner and a clear way to stop it
- Graceful shutdown: listen for `SIGTERM`, call server shutdown, drain
  in-flight requests, then cancel the root context

---

## Testing
[ID: go-service-testing]
[EXTEND: go-lib-testing]

- Integration tests in `internal/[feature]/*_integration_test.go`
  behind a build tag: `//go:build integration`
- Performance tests with k6 — colocated in `tests/performance/`

---

## Feature flags (if applicable)
[EXTEND: backend-features]

- Use the OpenFeature Go SDK or a provider SDK (LaunchDarkly, Unleash) —
  wrap behind an interface so the provider can be swapped in tests
- Pass the flag client through the dependency graph — constructor argument,
  not a package-level singleton
- In tests, use the in-memory OpenFeature provider

---

## Messaging (if applicable)
[EXTEND: backend-messaging]

- Use `confluent-kafka-go` for Kafka, `amqp091-go` for RabbitMQ, or the
  AWS SDK v2 `sqs` package for SQS
- Run consumers as goroutines under an `errgroup` — stop cleanly on
  context cancellation
- Define a `Message` struct per topic/queue — decode at the entry point,
  never pass raw `[]byte` to business logic

---

---

## Commands
```
go run ./cmd/[service]    # develop
go build ./cmd/[service]  # build binary
go test ./...             # run all tests
go test -tags integration ./...  # run integration tests
go vet ./...              # static analysis
goimports -w .            # format imports
make migrate-up           # apply DB migrations
docker build -t [name] .  # build container image
```