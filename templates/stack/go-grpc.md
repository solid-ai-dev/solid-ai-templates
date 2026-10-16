# Stack — gRPC Service (Go)
[DEPENDS ON: templates/stack/go-lib.md, templates/core/config.md, templates/backend/grpc.md, templates/backend/concurrency.md, templates/infra/cicd.md, templates/security/devsecops.md]

Extends the Go library stack and the gRPC backend layer with Go-specific
conventions for implementing gRPC servers and clients.

---

## Stack
[ID: grpc-go-stack]

- Language: Go 1.22+
- gRPC library: `google.golang.org/grpc`
- Proto compiler: `protoc` + `protoc-gen-go` + `protoc-gen-go-grpc`
- Proto tooling: `buf`
- Config: per `templates/stack/go-service.md`
- Test runner: go test (stdlib) + `google.golang.org/grpc/test/bufconn`
- Distribution: Docker image

---

## Project structure
[ID: grpc-go-structure]

```
cmd/
  [service]/
    main.go              # wires dependencies, starts gRPC server
internal/
  [feature]/
    server.go            # implements generated gRPC server interface
    service.go           # business logic — no gRPC imports
    repository.go        # data access
    model.go             # domain types
  interceptor/
    auth.go
    logging.go
    recovery.go
  config/
    config.go
proto/
  [org]/[service]/v1/
    [service].proto
generated/
  [org]/[service]/v1/    # generated stubs — never edit by hand
Makefile
Dockerfile
go.mod
go.sum
buf.yaml
buf.gen.yaml
README.md
CLAUDE.md
```

---

## Service implementation
[EXTEND: grpc-implementation]

- Implement the generated `[Service]Server` interface in `server.go`
- Register the server: `pb.Register[Service]Server(grpcServer, &Server{})`
- Inject dependencies via constructor — `Server` struct holds service and
  config references, never accesses globals
- Use `context.Context` as the first argument to all downstream calls —
  cancel propagates from the gRPC framework automatically

---

## Server setup and shutdown
[EXTEND: backend-concurrency]

- Start the gRPC server in `main.go` under an `errgroup` alongside any
  other servers (HTTP metrics, health)
- Graceful shutdown on `SIGTERM`: call `grpcServer.GracefulStop()` then
  cancel the root context — in-flight RPCs drain before the process exits
- Set explicit timeouts: `grpc.ConnectionTimeout`, `grpc.KeepaliveParams`

---

## Interceptors
[EXTEND: grpc-interceptors]

- Chain interceptors with `grpc.ChainUnaryInterceptor()` and
  `grpc.ChainStreamInterceptor()` at server creation
- Auth interceptor extracts metadata with `metadata.FromIncomingContext(ctx)`

---

## Testing
[EXTEND: grpc-testing]

- Use `bufconn.Listen()` for an in-memory connection — no port allocation,
  no network required
- Table-driven tests with `t.Run()` — one sub-test per scenario
- Inject a mock or fake service into the server under test using interfaces
- Integration tests behind `//go:build integration` build tag
- Go test functions MUST start with `Test` prefix:
  `TestGetUser_UserNotFound_ReturnsNotFoundStatus`
- Run before every commit: `go test ./... && go vet ./...`

---

## Commands
```
buf lint                          # lint proto files
buf generate                      # generate Go stubs
buf breaking --against .git#tag=v<prev>  # check for breaking changes
go run ./cmd/[service]            # develop
go test ./...                     # run unit tests
go test -tags integration ./...   # run integration tests
go vet ./...                      # static analysis
make docker-build                 # build container image
```