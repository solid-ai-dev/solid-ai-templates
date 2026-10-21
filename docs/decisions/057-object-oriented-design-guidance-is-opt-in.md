---
id: "057"
status: Accepted
date: 2026-10-21
category: composition
supersedes: ["046"]
superseded_by: []
---

# ADR-057: Object-oriented design guidance is opt-in

## Context

`base-oop` sits in the core tier, so every chain loads it, including chains
whose code has no classes to design.

| Force | What it shows |
| ----- | ------------- |
| Reach | Measured on `main` on 2026-10-21: `templates/core/oop.md` resolved into all 41 roots, documentation-only and static-site roots among them |
| Fit | SOLID, class hierarchies and design patterns govern object-oriented code; a documentation repository or a static site applies none of it |
| Content | The file held a GoF catalogue and a categorical ban on AOP frameworks, preferences rather than rules every project needs |
| The freeze | From 3.0.0 core-tier membership is frozen until 4.0.0, so leaving the core is possible only before the tag |
| The earlier gap | The file once reached only service chains, by accident of the graph; library and service projects still need a way to load it |

## Decision

`base-oop` leaves the core tier and becomes an opt-in template that a
project declares through `Extras` or a stack names in `depends_on`.

## Rationale

- A chain whose code has no classes stops carrying rules it cannot apply,
  which answers the reach and fit forces.
- A library or service project still loads the file by declaring one
  template, so the earlier gap does not return by accident: reach becomes a
  stated choice instead of a graph side effect.
- Doing it before 3.0.0 is the only window the freeze leaves.

## Design

1. **Membership**: the manifest's `core:` entry drops `base-oop`; its entry
   stays under `base:` at `templates/core/oop.md`
2. **Reach**: a project declares `base-oop` in `Extras`; a stack for an
   object-oriented language MAY name it in `depends_on`
3. **IDs**: `base-oop`, `base-oop-restraint` and `base-oop-aop` keep their
   names; the AOP section is retitled "Cross-cutting concerns"
4. **Content**: the GoF catalogue gives way to one rule, use a named
   pattern where it fits and name it in code; the AOP-framework ban becomes
   a rule to keep cross-cutting behaviour visible at its call site

## Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| Keep it in core, trimmed | Every non-object-oriented chain still carries it, and the freeze then fixes that until 4.0.0 |
| Name it in each object-oriented stack's `depends_on` only | Upstream ships no stacks; a project without a fork stack would have no way in but `Extras`, which this design already gives |
| Drop the file | Library and service projects lose the only interface and abstraction rules the templates hold |

## Consequences

| Area | Change |
| ---- | ------ |
| Chains | Every chain that does not declare `base-oop` loses the file |
| Manifest | `core:` drops `base-oop` |
| Generated docs | The core-tier listing in the building-block view regenerates |
| Projects | A project that applies object-oriented design adds `base-oop` to `Extras` |
| Forks | A fork's object-oriented stacks add `base-oop` to `depends_on` |
| Migration guide | Lists the move |

## Compatibility

No section ID is renamed or removed. A chain that relied on the core tier
for these rules adds `base-oop` to `Extras`; a template extending or
overriding one of its sections adds it to `depends_on`. The change ships in
3.0.0, before the freeze, and the CHANGELOG lists it under `Breaking
changes`.

## Security

None.

## Related

- `templates/core/oop.md`, the file this record moves out of the core tier.
