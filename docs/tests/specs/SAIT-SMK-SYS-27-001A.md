---
id: SAIT-SMK-SYS-27-001A
title: An emitted file names no template file
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-30
author: Branimir Georgiev
product-version: "3.x"
tags: [tooling, composition, delivery]
---

## Short description

> **Given** every root a project can pick
> **When** the emitter builds each root on its own, with skills and inlined
> **Then** no line of an emitted file names a template file, because an
> emitted project carries the rules and not the templates, so a named
> template is a file the agent cannot open and the rules it stands for
> never reach it

Each root gets its own build because a project may pick it alone. Built
together, an override one root carries can drop the section another root
names a template in, and the path goes unseen.

## Results

| Result | Condition |
|--------|-----------|
| PASSED | The planted template's two named paths are both found in each mode, the planted override hides one only when the roots are built together, and no file emitted from any root alone, in either mode, names a template file |
| FAILED | An emitted line names a template file, with or without its `templates/` prefix, or the planted scan misses a form |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

— (operates on planted templates and on every root, built in memory; no
file is written)

### Execution

1. Build a planted template that names its own path once with the
   `templates/` prefix, in a skill, and once without, in a section a
   second planted root overrides
2. Build the planted roots together, then each on its own
3. Build every root `--roots` lists on its own, with skills and then with
   skills inlined
4. Scan every emitted line for the path of every template file

### Assertions

1. Assert the scan finds both of the planted template's named paths, in
   each mode
2. Assert the planted roots built together show one of the two paths, and
   built each on its own show both
3. Assert no line emitted from any root, in either mode, names a template
   file

### Negative controls

1. **The prefix-less form unread.** With the scan matching only paths that
   start `templates/`, the planted case finds one of its two paths and
   fails
2. **A pointer left in a template.** With the templates before this check
   landed, the scan fails on the seven lines that named another template,
   in every root that carries them
3. **Every root built together.** With the planted roots built as one
   chain, the override hides the second path and the planted case fails

## Related

- ADR-058: templates place each rule, and task procedures load on demand
- SYS-26: the emitter places each section by its load
