---
id: SAIT-INT-MNF-06-001A
title: A fork that only appends merges an upstream change cleanly
product: sait
type: integration
area: MNF
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-17
author: Branimir Georgiev
product-version: "2.x"
tags: [manifest, fork, composition, merge]
---

## Short description

> **Given** a simulated fork made from the revision an upstream change
> starts at, which appends a stack and edits its own documents
> **When** the upstream change is merged into it with `git merge`
> **Then** the merge conflicts in no file but the fork's own documents,
> and the merged tree passes smoke with SYS-20 against the upstream side

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Both planted merges yield exactly their owed conflicts, and the upstream change merges and passes smoke |
| FAILED | A planted merge yields conflicts other than those it owes |
| FAILED | The upstream change conflicts outside `README.md`, `AGENTS.md`, `CLAUDE.md` and `CHANGELOG.md` |
| FAILED | The merged tree loses the fork's stack, or its smoke run fails or prints no verdict |
| FAILED | The base ref does not resolve, or shares no history with HEAD |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | A simulated commit changes files other than those it claims, or a merge fails without conflicts |

## Steps

### Prerequisites

- Repository cloned with full history, and git
- Python 3 and PyYAML
- The base ref, `origin/main` by default, fetched

### Setup

1. Take the base: the merge base of HEAD and the base ref. In CI's pull
   request checkout HEAD is the merge commit, so the upstream change is
   the pull request's diff; on a push to main it is empty
2. Make a shared clone in a temporary directory, so a detached HEAD no
   branch names still resolves
3. Commit the fork on the base: a copy of the fixture stack under
   `templates/stack/`, its entry appended to the manifest, and a line under
   the title of each fork-owned document

### Execution

1. FS-01: merge a planted upstream commit that appends its own stack entry
   at the manifest's end
2. FS-02: merge a planted upstream commit that edits the README under its
   title
3. FS-03: merge HEAD, or a planted `base:` description edit when HEAD
   changes nothing against the base; keep the fork's side of any conflict
   in a fork-owned document, point the fork's own files at each path
   upstream renamed, as a fork migrating would, then run the merged
   tree's `run_smoke.py` with `SAIT_UPSTREAM_REF` at the upstream side
4. FS-03, when a commit in the range carries the trailer
   `Fork-merge: ours` and no merge in the range already took it with
   `-s ours` (a merge whose tree is its first parent's): merge with
   `git merge -s ours`, as a fork takes a change that removes what forks
   carry; move each entry upstream dropped from `base:`, `backend:` and
   `frontend:` to the fork's own `fork:` key and each dropped core ID to
   `fork_core`; then run smoke as in step 3

### Assertions

1. Assert each simulated commit changes exactly the files it claims —
   the landing assertion for every scenario
2. Assert FS-01 conflicts in `templates/manifest.yaml` only, and is caught
3. Assert FS-02 conflicts in `README.md` only, and completes as the fork's
4. Assert FS-03 conflicts in no file outside the fork-owned documents,
   keeps the fork's stack, and its smoke run passes. A rename is migrated
   and reported; a deleted file or a removed ID is not, and fails smoke.
   Under the trailer, the fork's tree passes smoke once its templates leave
   upstream's keys; skipping that move fails SYS-20
5. Assert all three scenarios ran

### Negative controls

1. **The defect that motivated the check.** An upstream change that a fork
   cannot take: commit one that gives a core template the section ID
   `fork-sync-stack`. Upstream's own smoke passes it; this runner fails
   FS-03 through SYS-02 in the merged tree
2. **A detector that finds no conflict.** FS-01 runs on every run and owes
   a manifest conflict, so a merge step that reports none fails it

## Related

- ADR-049 — a fork syncs by `git merge upstream/main`, appends and never
  edits upstream keys, and owns its README, AGENTS.md, CLAUDE.md and CHANGELOG
- SAIT-SMK-SYS-20-001A — the manifest ownership check this run nests
