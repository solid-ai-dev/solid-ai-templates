---
id: "048"
status: Accepted
date: 2026-09-27
category: templates
supersedes: []
superseded_by: []
---

# ADR-048: A lessons log replaces the development journal

## Context

`templates/base/core/docs.md` resolves into every chain and makes
`docs/dev-journal.md` a MUST for agent-assisted projects. The wrap-up
checklist writes one entry per session, recording its changes, pull
requests, issues, gaps and lessons, and `docs.md` checks the entry form.

Measured in this repository on 2026-09-27, the journal held 139 entries in
8,762 lines. At 470 KB it is too large for an agent to read whole, so it
cannot carry context to the next session. In September, 48 of 333 commits
touched it and added 3,456 lines, about 40 % of the file in one month.

Most of an entry restates what the tracker already holds. Gaps are
unfinished work with a state, open or done, that a frozen entry cannot
follow, and the wrap-up already turns them into issues. The lessons are the
one part no other record holds. A lesson also feeds upstream: a consuming
project can recognise a recurring need only if it recorded the first
occurrence.

## Decision

1. **The development journal is no longer a standard document** —
   `docs/dev-journal.md` leaves the standard documents table, and no
   template requires a per-session entry.
2. **A lessons log takes its place** — a project built from the templates
   SHOULD keep `docs/lessons.md`. It holds one entry per lesson, not per
   session.
3. **An entry states three things** — what was learned, where it occurred,
   and its upstream disposition: an issue filed against the templates, kept
   local, or already covered by a rule. A lesson with no disposition is not
   finished.
4. **The wrap-up records a lesson only when the session produced one** —
   a session with nothing learned writes nothing, and gaps stay issues.
5. **The rule takes effect in the v3.0 release** — together with the guide
   docs' rename, which edits the same table, so a consuming project
   migrates once. This repository keeps `docs/dev-journal.md` as frozen
   history and seeds the lessons log from its lessons that still hold.

## Alternatives considered

- **Keep the journal and shorten its entries** — rejected; a shorter entry
  is still one pull request per session, and still restates the tracker.
- **Drop the journal and keep nothing** — rejected; the lessons would be
  lost, and a consuming project could no longer tell a recurring need from
  a one-off.
- **Keep lessons only in the agent's memory** — rejected; memory is private
  to one agent and one machine. The upstream report needs a record in the
  repository.
- **Make the lessons log a MUST** — rejected; a project that never meets a
  recurring need gains nothing from the file, and an empty MUST document is
  bookkeeping.

## Consequences

- At v3.0, `templates/base/core/docs.md` replaces the journal row with the
  lessons log, states the entry form, and replaces the journal-form check
  with a lesson-form check
- The wrap-up checklist in `templates/base/workflow/scope.md` replaces its
  journal item with "record a lesson if the session produced one"
- This repository's `CLAUDE.md` wrap-up list and `docs/PLAYBOOK.md` follow
- The v3.0 migration guide tells a consuming project to keep its journal as
  history and start `docs/lessons.md`
- The CHANGELOG entry for v3.0 names the removal as a breaking change
