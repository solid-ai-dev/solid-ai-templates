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
> **When** `resolve_chain.py --emit` builds them, with skills and inlined
> **Then** no line of an emitted file names a template file, because an
> emitted project carries the rules and not the templates, so a named
> template is a file the agent cannot open and the rules it stands for
> never reach it

## Results

| Result | Condition |
|--------|-----------|
| PASSED | The planted template's two named paths are both found, and no file emitted from any root, in either mode, names a template file |
| FAILED | An emitted line names a template file, with or without its `templates/` prefix, or the planted scan misses a form |
| FAILED | The emitter exits non-zero |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

— (operates on a planted template and on every root, written to a
temporary directory that is removed afterwards)

### Execution

1. Build a planted template that names its own path once with the
   `templates/` prefix, in a skill, and once without, in the root file
2. Run `resolve_chain.py --emit` on every root `--roots` lists, then again
   with `--inline-skills`
3. Scan every emitted line for the path of every template file

### Assertions

1. Assert the scan finds both of the planted template's named paths
2. Assert no line emitted in either mode names a template file

### Negative controls

1. **The prefix-less form unread.** With the scan matching only paths that
   start `templates/`, the planted case finds one of its two paths and
   fails
2. **A pointer left in a template.** With the templates before this check
   landed, the scan fails on the seven lines that named another template

## Related

- ADR-058: templates place each rule, and task procedures load on demand
- SYS-26: the emitter places each section by its load
