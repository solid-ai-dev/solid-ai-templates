---
id: "060"
status: Accepted
date: 2026-11-15
category: composition
supersedes: []
superseded_by: []
---

# ADR-060: The emitter can build section files that load on demand

## Context

The emitter's root file holds every rule without a load directive, so an
agent reads most of its chain on every turn, whatever the task touches.
The benchmark measures other deliveries against it, each built by script
from the same chain (solid-ai-dev/solid-ai-benchmark#169).

- Whole templates read on demand from a map, the benchmark's `lazyref`
  arm, read 11 of 13 templates, about 46k tokens, by turn 3 in its round
  5e (15 runs), so an agent that needs one topic reads the whole file
  (#2466)
- A template holds several topics; the benchmark chain's run from about
  450 to 1,700 words each, and nothing hands an agent one topic of one
- A topic's rules can depend on rules elsewhere: the rules under the
  template's title, a section it extends, a section its prose names by
  ID or by heading, and an extension a later template adds on top of it
- Template paths and section IDs are frozen for 3.x, so a delivery that
  splits templates or anchors each heading changes the frozen surface

## Decision

The emitter gains an opt-in mode, `--sections`, that builds one file per
topic, each a heading of a template with every rule it depends on, and a
root file that maps each topic to its file, to be read when the work
first touches it.

## Rationale

- One topic, one read: an agent reads the rules of the topic at hand, not
  the whole template that holds it
- Same rules, same precedence: the mode applies the overrides, the
  declined list and the checked cut the other modes apply, so only
  packaging and loading differ, which is what the benchmark compares
- Nothing frozen changes: the files are built from the templates as they
  are, with no new anchor, path or ID
- Measured before it is endorsed: the mode stays opt-in and outside the
  frozen surface until a benchmark round compares it with the root file
  and with whole templates on demand

## Design

1. **Topic** — each heading one level under a template's title, with its
   subheadings, is a topic with a file of its own. The rules under a
   title alone get a file only where no topic's file carries them
2. **Carried rules** — a topic's file carries, in chain order, the rules
   under its template's title, each section it extends, each section its
   prose names by ID in backticks or by heading, each extension of its own
   sections, and what each of those carries in turn. A heading is named
   by its exact text in double quotes, after "see", or as a link to its
   anchor, read across a wrapped line, and resolves in the naming
   template first, then anywhere in the chain. Each relationship is read
   from the template as written and resolved through the overrides to the
   rules that survive. Rules carried only because they sit under a title
   do not bring that title's extensions (MUST)
3. **Same rule set** — the files together hold exactly the rules the
   inlined root file holds, and every copy of a rule matches its source
   (MUST)
4. **The map** — the root file keeps the facts, states
   `Model: root and sections`, and lists each template by its title and
   manifest description, with one row per topic naming its file. It holds
   no rule, and tells the agent not to read the files before the work
   starts (MUST)
5. **Paths** — a file is written to
   `.agents/sections/<template ID>/<heading>.md`, so no emitted path or
   line names a template file (MUST)
6. **Deterministic** — the same chain and declined list give
   byte-identical files (MUST)
7. **Not frozen** — the flag and the layout may change or go in a minor
   until a benchmark round decides whether the mode is a delivery

## Alternatives considered

| Alternative | Why not |
|---|---|
| Stable anchors per section, the map naming `file#anchor` | Freezes one more name per heading, and an agent's file reader takes no anchor, so it reads the whole file anyway |
| Split a template over a size limit into topic files | Changes template paths, which 3.x freezes, and leaves a topic's dependencies in other files |
| Whole templates read on demand from a map | Already measured: the agent read most of the chain within three turns |
| Leave the root file as it is | Every turn carries most of the chain, which no delivery has yet been measured against topic by topic |

## Consequences

| Consequence | Effect |
|---|---|
| Tool | `resolve_chain.py --emit <dir> --sections <root>...` writes the map and the section files; `--inline-skills` with it is refused |
| Checks | SYS-28 compares the files with the inlined root file's rules, every root built alone, and runs the tool twice under different hash seeds; SYS-27 scans the section files for template paths |
| Requirements | FR-06-08 and FR-06-09 state the mode |
| Frozen surface | The mode is listed as not frozen (chapter 8.7) |
| Benchmark | Builds arm `lazysections` from the mode, beside the arm that reads every template up front and the one that reads whole templates on demand |

## Compatibility

None for an existing project: the root file and skills, inlined or not,
are byte-identical to what the emitter built before. A project that moves
to `--sections` keeps its filled-in facts, and the emitter removes the
skills it wrote before, as it removes any file it no longer emits.

## Security

- Exposes: every rule leaves the root file, a section that guards data,
  credentials or authentication included, so it is read only when the
  work touches its topic. The root and skills keep such a section in
  context on every turn, which is why this mode is opt-in and measured
  first, on the benchmark's security and data-protection rows as well as
  every other
- Protects: a file carries every section its rules extend or name, so no
  rule in it is left to a reference the agent may not follow
- Trust boundary: the section files are built by the tool into the
  project's tree, under the same review as the root file

## Related

- solid-ai-dev/solid-ai-benchmark#169, the arms that compare deliveries
