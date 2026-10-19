---
id: "053"
status: Accepted
date: 2026-10-19
category: composition
supersedes: []
superseded_by: []
---

# ADR-053: The declaration block is a target, not part of the frozen surface

## Context

The compatibility contract for 3.x freezes what forks and projects refer
to until 4.0.0. Its list includes a declaration block: the `Stack`,
`Extras` and `Platform` lines a generated context file would carry so an
agent resolves its chain at startup. The review before 3.0.0 found that
nothing stands behind that entry.

| Force | What it shows |
| ----- | ------------- |
| No producer | No interview writes the block; a generated file lists its chain or inlines it |
| No reader | `tools/resolve.py` takes one root and cannot compose a stack with its extras and platform |
| Described as a target | SPEC states the block under "Consumption model (target)" |
| A freeze binds the shape | Once frozen, a field the first reader turns out to need, or a change of shape, is breaking until 4.0.0, though nothing ever read the old form |

## Decision

The declaration block leaves the 3.x frozen surface and stays a target until
a release ships both a tool that writes it and one that reads it.

## Rationale

- A contract protects consumers from changes to what they use. No consumer
  uses the block, so freezing it protects no one.
- Freezing an unexercised format fixes its shape before the first reader
  tests it, and the cost of a wrong guess is a major release.
- Adding the block to the frozen surface later is itself compatible: a 3.x
  minor may freeze more, and freezing breaks nothing.

## Design

1. **The frozen surface** — template paths, template and section IDs, the
   manifest schema, core-tier membership, and check exit codes (0 passes,
   1 fails, 3 does not apply). The declaration block is not among them
2. **Target, not contract** — SPEC keeps the block under its consumption
   model target and states that it is not frozen
3. **Freezing it later** — the minor that ships a producer and a reader of
   the block adds it to the frozen surface and says so in `CHANGELOG.md`

## Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| Implement the block before 3.0.0 | A resolver composing a stack with extras and a platform, an interview writing the block and its tests, all for a need no consumer has raised, delay the release the rest of the contract is ready for |
| Keep it frozen, unimplemented | Commits 3.x to a format no tool has exercised; the first reader then either takes the frozen shape as it is or waits for 4.0.0 |

## Consequences

- 3.x may change the declaration block's fields or shape in a minor until
  the block is frozen.
- A project that writes the block by hand loses nothing: no tool reads it.
- The rest of the frozen surface is unchanged.

## Compatibility

No template, ID, path, manifest field or exit code changes. The block's
description in SPEC stays, marked as a target.

## Security

No credentials, secrets or attack surface are involved.

## Related

- ADR-051 - the compatibility contract whose frozen surface this narrows.
