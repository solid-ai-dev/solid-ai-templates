# Rationale: frontend quality

Why the rules in `templates/frontend/quality.md` say what they say. The template
states each rule as one instruction; the reasoning and the worked examples
are here, one heading per section, named by ID where the section has one.

## testing-in-process-server

A framework test client bypasses the real server, its headers and its
static-file content types; a container is slow and needs a runtime. Port 0
never collides across parallel tests. Python `make_server(..., 0, ...)`,
Node `server.listen(0)` and Go `httptest.Server` all expose the primitive.
