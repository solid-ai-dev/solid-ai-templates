---
id: SAIT-SMK-SYS-26-001A
title: The emitter places each section by its load, the same every run
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-26
author: Branimir Georgiev
product-version: "3.x"
tags: [tooling, composition, delivery, determinism]
---

## Short description

> **Given** a chain whose sections carry load directives
> **When** `resolve_chain.py --emit` builds the root file and the skills
> **Then** every-turn rules stay in the root file, a task's procedure moves
> to its skill, a checked section keeps its command and pass condition
> whole, an overridden section gives way to its override, a declined
> section is left out, a rerun keeps the project's facts and removes what
> it no longer emits, and two runs give byte-identical files, because the
> same templates must give every project the same files

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Both planted placements and the planted rerun are right, and two runs of the core chain under different hash seeds write the same bytes |
| FAILED | A planted placement is wrong, in either mode, or the planted rerun loses a fact, keeps a declined skill or its mirror, or overwrites a hand-written root file |
| FAILED | The two runs differ, or the emitter exits non-zero |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

— (operates on a planted template and on `base-quality`'s chain, written
to a temporary directory that is removed afterwards)

### Execution

1. Build the planted template and the planted stack that overrides one of
   its sections, with skills, then with skills inlined
2. Emit them into a directory, fill in a fact, decline the skill's
   section, and emit again; emit once more over a hand-written root file
3. Run `resolve_chain.py --emit` on `base-quality` twice, with
   `PYTHONHASHSEED` 1 and 2, mirroring the skills into `.claude/skills`
4. Compare the two output trees byte for byte

### Assertions

1. Assert the every-turn rule is in the root file in both modes
2. Assert the checked section keeps its command and its bullet-form pass
   condition with its wrapped line, and drops its rule with its wrapped
   line
3. Assert the overridden rule is absent and its override present, and the
   declined section is absent
4. Assert, with skills, the procedure is in its skill and the trigger
   table, and not in the root file
5. Assert, inlined, the procedure is in the root file and no skill file is
   written
6. Assert the rerun keeps the filled-in fact, removes the declined skill
   and its mirror, and refuses the hand-written root file
7. Assert the two runs write the same files with the same bytes

### Negative controls

1. **Procedures kept in the root file.** With the emitter's task branch
   sending rows to the root file, the planted placement with skills fails
2. **Overrides ignored.** With the overridden section kept, both planted
   placements fail on the overridden rule
3. **Facts not kept.** With the previous root file's facts not carried
   over, the rerun fails on the filled-in fact and on the hand-written
   file
4. **A non-deterministic run.** With the root file opening on a string's
   hash, which changes with the seed, the two runs differ in `AGENTS.md`

## Related

- ADR-058: templates place each rule, and task procedures load on demand
- The spec, chapter 8.1: the load directive
