# 4. Solution strategy

| Goal | Approach | Decision |
|------|----------|----------|
| One concern per file, composed without edits | Templates in the spirit of SOLID: single responsibility, open for extension through `[EXTEND]` and `[OVERRIDE]`, never modified by a consumer | ADR-001, ADR-004 |
| One source of truth for the graph | `templates/manifest.yaml` holds every template, its ID and its dependencies; headers mirror it and smoke checks the mirror | ADR-004 |
| No transitive surprises | A stack composes only the modules it declares; the core tier is seeded into every chain, everything else is opt-in | ADR-004 |
| Rules an agent actually applies | A generated file delivers rules inline or hybrid, never by reference alone | ADR-052 |
| Shared policy, local content | Upstream keeps the engine and shared policy; forks carry stacks and process and merge upstream | ADR-049, ADR-050 |
| A contract consumers can pin | 3.x freezes the surface chapter 8.7 lists; removal waits for the next major | ADR-051 |
| Rules that check themselves | A mechanically checkable rule names its command and pass condition; the conformance runner runs those checks against this repository | ADR-030, ADR-031 |

## 4.1 Delivery model

![How one rule is placed: if breaking it is silent and no test, linter or CI step enforces it, it is inlined; if it fails visibly or a tool enforces it, it may be referenced. Inline and hybrid remain; pure reference is deprecated](../diagrams/delivery-model.png)

A rule whose breach is silent, with no test, linter or CI step to catch it,
is copied into the context file. A rule that fails visibly, or that a tool
enforces, may be named as a file to read. Chapter 6 shows how a chain is
resolved and handed to the agent.

## 4.2 Compatibility

![Releases on a line: 2.90.0 receives nothing more and is the pin until a project migrates; 3.0.0 freezes the contract; a 3.x minor adds and may deprecate; 4.0.0 removes what 3.x deprecated; a security fix may break early](../diagrams/compatibility.png)

`docs/migrating-to-v3.md` moves a 2.x project or fork to 3.0.
