---
id: SAIT-SMK-SYS-23-001A
title: A hook a template names is shipped and catches its plant
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-20
author: Branimir Georgiev
product-version: "3.x"
tags: [tooling, hooks, checks, compatibility]
---

## Short description

> **Given** the hooks in `.pre-commit-hooks.yaml` and the hook commands the
> templates name
> **When** smoke reads them and runs each hook against planted repositories
> **Then** every named hook is shipped, every shipped hook dispatches, and
> each one fails its planted violation and passes its clean subject, because
> a template naming a missing hook points a rule at nothing, and a hook that
> cannot fail is decoration

## Results

| Result | Condition |
|--------|-----------|
| PASSED | The manifest and the dispatch table hold the same hooks, each entry is `solid-ai-checks <id> --pre-commit`, every named hook is shipped, and every planted case yields the exit and finding count it owes |
| FAILED | A hook is in one of the manifest and the dispatch table, not both |
| FAILED | A manifest entry runs anything but its own hook in pre-commit mode |
| FAILED | A template names a hook no manifest entry ships |
| FAILED | A planted case yields another exit status or finding count |
| FAILED | No hook, no hook command or no planted case was found |
| SKIPPED | — |
| BLOCKED | PyYAML is not installed |
| ERROR | git is not on `PATH` |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3, PyYAML and git

### Setup

— (each planted case gets a throwaway git repository, removed afterwards)

### Execution

1. Read `.pre-commit-hooks.yaml` and `solid_ai_checks.__main__.HOOKS`
2. Collect every `pre-commit run <id>` line in the templates
3. For each case in `CASES`, commit its files to a fresh repository and run
   the hook there directly
4. Run `report-test-edits` against a base: at the base, at the base in
   pre-commit mode, after a commit editing a test, and against a base that
   does not resolve
5. Run `report-off-limits-paths` on a branch touching a declared path, on
   one touching none, and against a base that does not resolve

### Assertions

1. Assert the manifest and the dispatch table name the same hooks, and the
   package's top-level modules are exactly the dispatched hooks; shared
   code lives in `support/`
2. Assert each entry is `solid-ai-checks <id> --pre-commit`
3. Assert each hook a template names is in the manifest
4. Assert each planted violation fails, or is listed for a reading hook
5. Assert each clean subject passes
6. Assert a subject with nothing to check exits 3 run directly, and prints
   `not applicable:` and exits 0 in pre-commit mode
7. Assert a root written as `./docs` or `.` reaches the paths git prints
8. Assert `report-test-edits` fails on a base that does not resolve, in
   both modes, since a missing baseline compares nothing
9. Assert the hook, hook-command and planted-case counts are non-zero

### Negative controls

1. **A misnamed hook.** A template naming `pre-commit run find-unfenced`
   fails with "names hook find-unfenced, which no manifest entry ships"
2. **A blind hook.** `find-bare-suppressions` with its pattern table
   emptied fails the "a suppression naming no rule" case

## Related

- ADR-055: long checks become pre-commit hooks
- `templates/core/quality-gates.md`, "Shipped checks"
