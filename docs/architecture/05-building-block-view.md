# 5. Building block view

## 5.1 Repository

```text
templates/          # every template, plus the manifest
  core/             # rules for every project: git, docs, quality, testing, ...
  security/         # application and pipeline security
  infra/            # CI/CD, containers, deployment
  data/             # data modeling, quality, governance, migration
  backend/          # backend layer: HTTP, API, database, observability, ...
  frontend/         # frontend layer: UX, CSS, content, static sites
  fixture/          # one stack and one platform, test input only
  manifest.yaml     # the dependency graph every tool reads
tools/              # resolve_chain.py, sync_docs.py, check_release.py, the audits
tests/              # the three runners; smoke/, conformance/, baselines/
docs/               # this specification, decisions, playbook, audits, test specs
```

A fork adds its own directories, such as `templates/stack/`,
`templates/platform/` and `templates/<org>/`, and never adds a file under
upstream's.

## 5.2 Templates

| Kind | Where | Used how |
|------|-------|----------|
| Base | `core/`, `security/`, `infra/`, `data/` | One concern each; composed into a chain, never used alone |
| Layer | `frontend/`, `backend/` | Concerns shared by one kind of project; extend base templates |
| Stack | A fork's own directory | Technology-specific rules; declares the layers it depends on |
| Platform | A fork's own directory | Maps CI and security tools to one hosting platform, orthogonal to the stack |
| Output format | `core/agents.md` | How the context file is written: structure, inline or hybrid, formatting; an input to generation, not a rule in the chain |
| Interview | A fork, usually `templates/INTERVIEW.md` | The questions an agent asks before generating; upstream ships none |
| Fixture | `fixture/` | `stack-fixture` and `platform-fixture`, marked `fixture: true` so every listing a project reads leaves them out while the checks read them |

The generated context file for one project is its profile: interview
answers, plus the resolved chain, written to the output format.
`templates/core/docs.md`, "Output file by agent", says which file each
agent reads.

## 5.3 Manifest tiers

Every template has one entry in `templates/manifest.yaml`. How an entry
reaches a chain depends on its tier.

| Tier | Members | Reaches a chain |
|------|---------|-----------------|
| Core | `core:`, then a fork's `fork_core:` | Seeded into every chain; never needs declaring |
| Opt-in | CI (`cicd`, `quality-gates`), security, devsecops, containers, deployment, config, data | Only when a stack's `depends_on` names it |
| Orthogonal | Advanced data templates, a fork's platforms and workflow choices | Picked in the interview and resolved as a root of its own |

The core tier, as the manifest states it today:

<!-- generated:spec-core-tier -->
- `templates/core/quality.md`
- `templates/core/git.md`
- `templates/core/docs.md`
- `templates/core/testing.md`
- `templates/core/review.md`
- `templates/core/oop.md`

Measured: 10 `[DEPENDS ON]` tokens across 6 templates name one of these
files, and 6 manifest entries name a core id in `depends_on`. Declaring one
is redundant rather than forbidden — the seeding reaches the file either
way, and the directive documents a dependency a reader would otherwise
infer. Reached by the seeding alone: `base-review`. A chain assembled by
walking the directives does not reach that set and reports nothing about it,
because nothing declares what is absent.
<!-- /generated:spec-core-tier -->

Every top-level list of entries except `core` and `fork_core` is a section
the resolver reads, so a fork keeps its templates under a key of its own
and never edits one upstream owns.

## 5.4 Tools

| Tool | Does |
|------|------|
| `tools/resolve_chain.py` | Resolves a root to its ordered file list, or the concatenated chain |
| `tools/sync_docs.py` | Regenerates the derived sections in this specification and in a fork's README; `--check` fails on drift |
| `tools/check_release.py` | Checks a release's changelog cut and SemVer step |
| `tools/audit_redundancy.py` | Finds duplicate rules across resolved chains |
| `tools/score_templates.py` | Scores each template and holds the score to its baseline |

## 5.5 Checks

| Runner | Reads | Checks |
|--------|-------|--------|
| `tests/smoke/run.py` | The manifest and the templates' structure | References resolve, IDs are unique, chains are valid, governed tiers hold; the checks live in `tests/smoke/`, one module per family |
| `tests/conformance/run.py` | The templates' own fenced checks | Runs each against this repository, or skips it with a stated reason |
| `tests/fork_sync/run.py` | A simulated fork | The change merges into a fork that appends a stack, and smoke passes there |

`docs/tests/index.md` lists every check and `docs/tests/codification.md` the ID
scheme.
