# Stack — Fixture
[DEPENDS ON: templates/security/security.md, templates/core/quality-gates.md]

Test input for the checks that read every stack, not a stack to pick. It
resolves the security and quality-gate tiers and carries each section a
stack MUST carry, so those checks keep an input in a tree that ships no
stack of its own.

## Stack
[ID: fixture-stack]

- Language: [any]
- Service: one HTTP endpoint that returns its request body unchanged
- Build tool: `make`

## Commands
[ID: fixture-commands]

```
make install   # install dependencies
make test      # run the test suite
make lint      # lint and format check
```

## Project structure
[ID: fixture-structure]

- `src/` — the service, one module per endpoint
- `tests/` — one test file per module under `src/`, named after it

## General testing rules
[EXTEND: base-testing-general]

- Every endpoint test sends an empty body as well as a non-empty one

## Rendered output
[OVERRIDE: testing-verify-the-render]

- The service renders no page, so no test reads pixels or a DOM
