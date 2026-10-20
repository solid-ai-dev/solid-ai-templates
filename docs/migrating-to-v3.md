# Migrating to v3.0

v3.0 splits this repository in two. Upstream keeps the composition engine
and the policy every team shares; forks carry the stacks, platforms,
process templates, interview, examples and generated chains (ADR-049,
ADR-050). This guide covers the move for the two kinds of reader:

| You maintain | Read |
| ------------ | ---- |
| A project whose context file was generated from 2.x | [Projects](#projects) |
| A fork made before v3.0 | [Forks made before v3.0](#forks-made-before-v30) |
| A new fork | [Starting a fork](#starting-a-fork) |

`CHANGELOG.md` lists every change v3.0 makes. After `v2.90.0`, 2.x
receives nothing (ADR-051).

---

## What moved

| Content | 2.x | 3.0 |
| ------- | --- | --- |
| Engine — resolver, sync, the checks | upstream | upstream |
| Core, security, infra, data, backend and frontend templates | upstream | upstream |
| Stacks, platforms | upstream | a fork |
| Workflow and process templates, the interview | upstream | a fork |
| `examples/`, `generated/`, the e2e suite | upstream | a fork |
| Rules for decision records, changelogs and journals | upstream | a fork |
| Long check scripts in the core templates | fenced in the template | pre-commit hooks the template names |
| Rules for writing a check into Markdown | `base-quality-gates` | `base-embedded-checks`, by `Extras` |
| Rules for numerical routines, calibration and source silence | `base-quality` | `base-measurement`, by `Extras` |
| Rules for writing this repository's checks: control runs, prose detectors, refused preconditions, remedy references | `base-testing` | this repository's playbook |
| Python and pytest test mechanics: tier import modes, `__all__`, worked fixtures | `base-testing` | a fork's stack |
| The cohort check after a bulk migration, `base-testing-data-validation` | `base-testing` | `base-data-migration` |
| Pipeline diagnostics, `testing-diagnostic-production-path` and `testing-identical-metrics` | `base-testing` | removed |
| The Markdown line-width and documentation-figure scripts | `base-docs` | the Markdown linter's line-length rule; the figure check is this repository's own tool |
| Rules for retiring a document and for changing one other repositories carry | `base-docs` | this repository's playbook |
| Mermaid parser quirks, bulk-emit and round-trip generator rules | `base-docs` | removed |
| Verifying a filed issue in full, its shapes and checks; counting a text's self-claims | `base-review` | this repository's playbook; a short form stays |
| Review of shared browser and framework state | `base-review` | `frontend-quality` |
| Numerical-gate and score-component review items | `base-review` | removed |

The core tier requires three documents only: `README.md`, `AGENTS.md` and
`CLAUDE.md`, both agent files on every project. Their layout is the
project's own; `templates/core/agents.md` offers a default.

---

## Projects

A project pins the templates it was generated from, usually as a
submodule. Upstream at v3.0 ships no stack, so a project re-pins to a
fork.

1. Choose the fork: Imbra's, on request, or your own
   (see [Starting a fork](#starting-a-fork))
2. Point the submodule at the fork and pin a released tag of the fork,
   never a branch. The fork's own v2.x tags are upstream's, so pin one the
   fork cut after the split, such as the Imbra fork's `v1.0.0`:
   ```bash
   git submodule set-url <path> https://github.com/<owner>/<fork>.git
   git -C <path> fetch --tags
   git -C <path> checkout <tag>
   git add <path> .gitmodules
   ```
3. Regenerate the context file from the fork's interview and the resolved
   chain for your stack, per the fork's README. Do not hand-edit the
   2.x file into shape: the fork's output contract may differ from the one
   the file was generated against
4. Review the diff. Adopt a new rule for a named need or a material risk;
   existing adopted rules stay effective, and declining one needs no ADR
   (`docs/playbook.md`, "Adopt a template policy update")
5. Replace any check script copied from a 2.x template with the hook the
   template now names, pinned in `.pre-commit-config.yaml` to the same tag
   as the templates. Where the project's own docs carry check scripts, add
   `base-embedded-checks` to `Extras`; where it computes, calibrates or
   extracts values, add `base-measurement`

No guide document a project carries is renamed — see
[Guide documents](#guide-documents).

---

## Forks made before v3.0

The split is one upstream commit carrying the trailer `Fork-merge: ours`.
An ordinary merge of it deletes every file the fork kept and upstream
removed, so the fork takes it in steps. `docs/playbook.md`, "Sync with
upstream as a fork", gives each command; in outline:

1. Merge the split's parent normally
2. Merge the split with `git merge -s ours`
3. Move the fork's entries out of `base:`, `backend:` and `frontend:` into a
   manifest key of its own, and the core IDs upstream dropped into
   `fork_core:`
4. Restore each template the split modified rather than deleted. `-s ours`
   kept the fork's pre-split text of every file the commit touched; move
   the fork's own lines into fork-owned files and take upstream's text
5. Merge the rest of upstream normally, then confirm no upstream template
   differs from upstream's

Step 4 applies to documents as much as to templates. A fork's
`docs/PLAYBOOK.md`, `docs/SPEC.md` and `docs/ONBOARDING.md` keep their
pre-split text after `-s ours`; the Imbra fork moved its own procedures to
`docs/imbra-*.md` and took upstream's text for the three. v3.0 then renames
`docs/PLAYBOOK.md` to `docs/playbook.md`, merges `docs/ONBOARDING.md`
into `CONTRIBUTING.md`, and replaces `docs/SPEC.md` with `docs/spec.md` and
`docs/architecture/`; a fork takes all three with the merge.

### Traps

| Trap | What happens | Fix |
| ---- | ------------ | --- |
| Fork key appended at the manifest's end | A downstream fork's appends conflict with it | Place the key above `stacks:` |
| Rewriting the manifest | Its trailing blank line goes, and SYS-20 reads an edit | Keep the file's end byte-identical |
| A sync PR merged by squash | The upstream link is lost, and the next sync re-merges the range | Merge every sync PR with a merge commit |
| Upstream's history in the fork's log | The merged-work sweep reads upstream's `(#N)` as the fork's issue `#N` | Set `UPSTREAM_REPO` (below), so CI excludes upstream's commits |
| The changelog-deletion check on a merge | It reads upstream's bullet as one the fork deleted | Run it on `--first-parent` |
| A tag-triggered workflow never registered | `gh run list --workflow release-gates.yml` returns 404 | Register it (below) |

---

## Starting a fork

Fork the repository on GitHub, then set it up once:

| Setting | Why |
| ------- | --- |
| Repository variable `UPSTREAM_REPO` = `solid-ai-dev/solid-ai-templates` | CI fetches upstream, so SYS-20 compares the manifest with what the fork last merged and the merged-work sweep skips upstream's commits |
| Push upstream's tags to the fork | The release and changelog checks need a tag to bound their range |
| Turn on delete-branch-on-merge | The merged-head-branch check requires it |
| Register `release-gates.yml` | GitHub lists a workflow only once an event touches it, and this one fires on tags and dispatch alone. Touch it in one pull request and revert the line in the next |
| `gh repo set-default <owner>/<fork>` in each clone | A clone with an `upstream` remote can default to upstream, and every check reading issues then reads the wrong tracker |

Then add the fork's own content:

- Templates under a manifest key of the fork's own, with core-tier
  additions under `fork_core:` (spec, chapter 8.6)
- Rules that refine an upstream file in a fork-owned file beside it, never
  as edits to the upstream file
- Smoke checks in `tests/fork_checks.py`, dispositions in
  `tests/fork_dispositions.py`, and chain examples in
  `tools/fork_examples.py`, whose `CHAIN_EXAMPLES_DOC` names the fork-owned
  document they go to
- Procedures in fork-owned documents beside upstream's, so upstream's
  `docs/` merge cleanly

---

## Guide documents

v3.0 renames, merges or retires no guide document a project carries. The core
tier requires `README.md`, `AGENTS.md` and `CLAUDE.md` and prescribes no
layout for them, so a project's `docs/` keeps the files it has.

ADR-047, which renamed the guide documents to kebab-case, and ADR-048,
which replaced the development journal with a lessons log, are both
withdrawn: each changed a document upstream no longer prescribes. A fork
that prescribes guide documents, as the Imbra fork does in
`templates/imbra/docs.md`, decides their names and contents itself, and its
own migration notes say what its projects change.
