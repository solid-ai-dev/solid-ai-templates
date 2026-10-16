---
id: "049"
status: Accepted
date: 2026-10-16
category: composition
supersedes: ["009"]
superseded_by: []
---

# ADR-049: Forks carry the stacks and the process layer

## Context

This repository holds two kinds of content. One is the composition engine
and the engineering policy every project shares: the manifest schema, the
ID system, the resolver, the checks, and the quality, testing, security and
data rules. The other is one organisation's choices: seventeen stacks,
three platforms, a release and session process, the interview, examples and
generated chains.

The previous scope decision kept a curated stack set here and sent other
organisations to their own repositories. That left the second kind of
content in the shared core. A review of the core found half of it was an
operating manual rather than engineering policy. A team running a
different process inherits rules that contradict its practice, and a
contradiction between the context file and the practice is a failure the
efficacy benchmark tests for.

Every stack also ships in every release. The generated chains have grown
until the e2e canary hits the generator's output ceiling, and a change to
one organisation's process is a release for everyone.

## Decision

1. **Upstream holds the engine and the invariant policy** — this
   repository keeps the manifest schema, IDs, EXTEND and OVERRIDE, the
   resolver, the checks and the engineering policy that holds for any
   team. Which files fall on which side is a separate boundary decision.
2. **Forks hold the rest** — stacks, platforms, the process layer, the
   interview, examples and generated chains live in forks. Imbra's fork,
   `imbra-ai-templates`, is the first; any organisation MAY fork the same
   way.
3. **A fork is a git fork that merges upstream** — a fork syncs with
   `git merge upstream/main`, never by copying files.
4. **A fork appends and never edits upstream keys** — a fork MUST NOT edit
   the manifest keys upstream owns (`core:`, `base:`, `backend:`,
   `frontend:`). It appends under `stacks:`, `platform:` and keys of its
   own.
5. **Forks own their ID namespaces** — the prefixes `stack-*`,
   `platform-*` and `<org>-*` are reserved for forks, and upstream adds no
   ID under them.
6. **Upstream commits no derived content** — no `generated/`, no
   `examples/` and no stack table. A fork regenerates its own.
7. **Some files are expected to conflict** — `README.md`, `CLAUDE.md` and
   `CHANGELOG.md` are fork-owned, and a fork resolves them in its own
   favour on every merge.
8. **The split is merged with the `ours` strategy** — a fork that exists
   before the split merges the split commit with `git merge -s ours`. An
   ordinary merge deletes every file the fork left unchanged and upstream
   removed.
9. **Generation stays agent-driven** — the split adds no compiler. A
   project still hands its agent the interview and a resolved chain.
10. **The split takes effect in the v3.0 release** — until then this
    repository carries both kinds of content as it does today.

## Alternatives considered

- **Keep the curated set here** — rejected; it keeps one organisation's
  process in the shared core, and every stack ships in every release.
- **Stacks as a package or submodule** — rejected; it adds an install step
  for a user who only attaches a file to an agent, and a submodule pins
  rather than merges.
- **A separate stacks repository that copies the core** — rejected; a copy
  drifts, and nothing carries an upstream fix into it.
- **A compiler that assembles context files** — rejected; the composition
  stays readable Markdown an agent resolves, and a build step is a new
  dependency for every consumer.

## Consequences

- A boundary record assigns each template to upstream or to forks
- A compatibility record states what upstream freezes from `3.0.0`, so a
  fork can rely on the IDs it extends
- Smoke gains a check that fails when a fork edits an upstream manifest key
- Upstream CI gains a job that simulates a fork, lands an upstream change
  and asserts the merge is clean
- A fixture stack and platform give the per-stack checks an input once the
  stacks leave
- The README is rewritten for the fork model, and the issue on capping
  stack scope and defining the extension model closes on this record
- The migration guide documents the `ours` merge and the ownership rule
