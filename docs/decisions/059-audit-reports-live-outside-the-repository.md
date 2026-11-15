---
id: "059"
status: Accepted
date: 2026-11-15
category: process
supersedes: ["018"]
superseded_by: []
---

# ADR-059: Audit and benchmark reports live outside the repository

## Context

`docs/audits/` held two kinds of generated report, and neither is made by
the templates.

| Kind | Made by |
|---|---|
| Efficacy rounds, records, appendices and radars | The benchmark, in `solid-ai-dev/solid-ai-benchmark` |
| 360 audits, template-quality reports and other reviews | An audit or review session |

- The folder grew with every round, and the benchmark had to write into a
  checkout of the templates to publish a result
- A smoke check guarded where the folder's 360 audits were filed, which is
  housekeeping a consuming project never sees
- The v3.0.0 tag is the cheapest point to move the reports, before a fork
  syncs a tree that holds them

## Decision

The efficacy reports live in `solid-ai-dev/solid-ai-benchmark` under
`docs/reports/`, every other review lives in `solid-ai-dev/solid-ai-audits`
under `reports/`, and this repository keeps none.

## Rationale

- Each report lives with the tool or process that makes it, so publishing
  one needs no write to the templates
- Both repositories are public, so the architecture chapters can still
  cite a report by link
- With no report here, the smoke check that filed them has nothing to
  guard and is retired

## Design

1. **No report here** — `docs/audits/` is deleted and gitignored; a report
   is never committed to this repository
2. **Citations link out** — a chapter cites a report by its link in the
   repository that holds it
3. **History stays** — the reports remain in this repository's history up
   to the commit that removed them; no history is rewritten

## Alternatives considered

| Alternative | Why not |
|---|---|
| Keep `docs/audits/` | The benchmark keeps writing into the templates, and the folder keeps growing |
| One repository for every report | Efficacy reports belong with the harness that checks their stamp; reviews do not |
| A wiki or release assets | Neither is reviewed by pull request or versioned like a repository |

## Consequences

| Change | Where |
|---|---|
| SYS-07, its spec and its registry entry are removed | `tests/smoke/`, `docs/tests/` |
| The figures gate no longer exempts `docs/audits/` | `tools/check_doc_figures.py` |
| Citations point at the new homes | `docs/spec.md`, chapters 3, 10 and 11 |
| The 360 procedure stores a report in `solid-ai-audits` | `docs/playbook.md` |
| The benchmark writes its reports to its own `docs/reports/` | `solid-ai-dev/solid-ai-benchmark` |

## Compatibility

None for a consuming project. A 360 template a fork carries still tells
that fork's projects where to store their own audits.

## Security

None.
