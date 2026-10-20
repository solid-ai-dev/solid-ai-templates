---
id: SAIT-SMK-SYS-17-001A
title: Every registered check names a spec document that exists
product: sait
type: smoke
area: SYS
priority: p2
status: ready
environment: [local, ci]
automatable: yes
created: 2026-09-07
author: Branimir Georgiev
product-version: "2.x"
tags: [tests, references, registry, index]
---

## Short description

> **Given** a check registry whose every entry names a procedure
> specification
> **When** each named specification is resolved against the documents on
> disk and against the index a reader consults
> **Then** a name matching no document fails, because the templates gate
> this class of reference for what they ship and the suite had no
> equivalent for its own

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every registered spec names a document under `docs/tests/specs/` and has a row in `docs/tests/index.md` |
| FAILED | A registered spec names no document on disk |
| FAILED | A registered spec has no row in `docs/tests/index.md` |
| FAILED | A registry entry carries no spec field at all |
| FAILED | A document on disk has no row in `docs/tests/index.md` |
| FAILED | A document no registered check cites and no runner in `tests/` names, which does not declare `automatable: manual` |
| FAILED | `docs/tests/index.md` names a spec with no document on disk |
| FAILED | The check read no registry entries, no documents or no index rows |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3

### Setup

— (operates on the committed tree)

### Execution

1. List the `.md` documents under `docs/tests/specs/` by stem
2. Read `docs/tests/index.md`
3. For every entry in the smoke `CHECKS` registry
   (`tests/smoke/registry.py`), resolve its `spec` field against both
4. For every document on disk, look for its row in the index and for a
   citation: a registered check, the text of another runner in `tests/`,
   or `automatable: manual` in its frontmatter
5. For every spec ID the index names, look for its document on disk
6. Report how many checks were registered, how many documents were read
   and how many specs the index names

### Assertions

1. Assert every registered spec resolves to a document on disk
2. Assert every registered spec appears in the index, so a check cannot
   be registered and stay invisible to a reader
3. Assert every document on disk has an index row and a citation, so a
   repointed registry entry cannot leave its old document behind unread
4. Assert every spec the index names has a document on disk
5. Assert every count is non-zero, per ADR-034

### Negative controls

Each control was observed failing, and each mutation was asserted to
have landed before its result was read.

1. **The defect that motivated the check.** Run against the tree as it
   stood, the check named three unresolved references — `SYS-14`,
   `E2E-01` and its own `SYS-17` — while the rest of the suite reported
   no failures at all. Observed 2026-09-07
2. **A renamed document.** Moving `SAIT-SMK-SYS-16-001A.md` aside MUST
   fail. Observed 2026-09-07: the on-disk count moved 58 to 57 and the
   check named `SYS-16`, so the corpus is confirmed to have changed
   rather than the message alone
3. **A document present and unindexed.** Deleting the `SYS-16` row from
   `docs/tests/index.md` MUST fail on the index half while the disk half
   passes, which is what separates the two assertions. Observed
   2026-09-07
4. **An orphan.** A document on disk that nothing cites passed, which the
   2026-10-18 360 review found. A copy of a spec under an unused ID, given
   an index row, MUST fail as cited by nothing
5. **An index row with no document.** A row naming an ID with no file
   MUST fail on that row

## Related

- ADR-034 — why the counts are reported and floored
- `SAIT-SMK-SYS-01-001A` and `SAIT-INT-MNF-01-001A` — the same class of
  reference, gated for what the templates ship rather than for the suite
