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
| Pipeline diagnostics, `testing-diagnostic-production-path` and `testing-identical-metrics` | `base-testing` | removed; one diagnostic-view rule remains |
| The Markdown line-width and documentation-figure scripts | `base-docs` | the Markdown linter's line-length rule; the figure check is this repository's own tool |
| Rules for retiring a document and for changing one other repositories carry | `base-docs` | this repository's playbook |
| The Mermaid-note rule and the generator rules: banner, `--check`, re-rendering, formatter exclusion, regeneration, round-trip refresh, stale-entry counts, schema-derived fields | `base-docs` | condensed in `base-docs`; a bulk-emit script's `--check` is now the SHOULD every generator carries; the Mermaid-note rule, stale-entry counts and schema-derived fields are removed |
| Verifying a filed issue in full, its shapes and checks | `base-review` | this repository's playbook; a short form stays |
| Review of shared browser and framework state | `base-review` | `frontend-quality` |
| Numerical-gate and score-component review items | `base-review` | removed |
| Port binding | `base-config` | `backend-http` |
| The in-process config model and the interlocked-dependency updater rule | `base-config` | removed |
| Reading and bumping a vendored pin, and the chain-list rule | `base-agents` | this repository's playbook, "Vendor the templates in a project" |
| GitHub-specific SBOM upload and Actions pinning, Python SBOM tools, per-platform tool choice | `base-devsecops` | removed; neutral rules remain |
| Where a licence notice sits inside an image | `base-devsecops` | `base-containers` |
| Penetration testing, a periodic engagement rather than a pipeline step | `base-devsecops` | removed; a fork's process template can carry it |
| The list of IaC misconfigurations to detect, and the "widely adopted" dependency preference | `base-devsecops` | removed; the scanner's configured policy covers the first |
| The CycloneDX component check and the one-component library rule; the base-image dependency bot; the version comment on a pinned CI step; `pip-audit`, `npm audit` and `govulncheck` | `base-devsecops` | removed; image findings, deploy-time SCA and the vault rule are restated tool-neutrally |
| GitHub Actions specifics of the release record and the deploy skip; the hand-built side image | `base-cicd` | neutral rules remain |
| Python editable installs under Compose, `run --rm` write loss, the linter target-version exception | `base-containers` | removed |
| Figure cropping, the research scrape cache, the lens-catalogue examples | `base-data-quality` | removed; neutral rules remain |
| MySQL online-DDL tool names; the host MIME-registry example | `base-data-migration`, `base-security` | neutral rules remain |
| Multi-factor authentication, internal mTLS, the CORS preflight cache, `.env` files; vendor, library and shell-command examples | `base-security` | removed; neutral rules remain and every ID stays |
| React hooks and render props, the CSS line-width note, the no-consent-banner choice | `frontend-quality` | removed |
| Cloudflare crawl control, SEO audit thresholds, AEO measurement, the FAQPage fact; answer-engine crawlers now MAY | `frontend-static-site`, `frontend-quality` | removed or relaxed |
| `public/` paths, ESLint and Prettier file names, the homepage-sections note | `frontend-static-site` | removed; `frontend-content` keeps a neutral asset-path rule |
| Sortable boolean columns, fixed breakpoints, `frontend-ux-bakeoff` | `frontend-ux` | removed; breakpoints come from the design system |
| Pipeline diagnosability, the Serilog log shape, the OpenAPI drift-test detail | `backend-observability`, `backend-api` | removed or neutral |
| The unfenced-check script and the extraction rules | `base-quality-gates` | `base-embedded-checks`; the script ships as a hook |
| `quality-gates-length-bound-exemptions`, synthetic-subject and fixing-branch controls, the backslash table | `base-quality-gates` | this repository's playbook |
| The ruff rule-family sizing block | `base-quality-gates` | removed; the rule stays |
| `quality-exemption-doc-duty`, the exit-3 and readings rules, the immutable-corpus sweep | `base-quality` | this repository's playbook |
| Language porting rules; `inspect.getattr_static`; Python `__init__` and extras wording | `base-quality` | removed or neutral; one cross-language port rule remains |
| The eight-stage pipeline order, its push and tag triggers, the three-environment minimum, the post-publish deploy hook | `base-cicd` | removed; the gates, packaging once, DAST before production and artifact promotion remain |
| Kubernetes: namespaces, two replicas per service, probes, PodDisruptionBudget, ConfigMap secrets | `base-containers` | removed; resources as code and the readiness gate remain, orchestrator-neutral |
| Exact names: plural snake_case tables, `is_` booleans, `<table>_id` keys, alphabetical junctions, `ix_` and `ux_` indexes | `base-data-modeling` | one convention per store, recorded in the context file; relational rules say so |
| Per-target product choices: managed CAs, `step-ca`, F5 and MetalLB, Route 53 and Consul, Harbor and Athens, Vault topologies | `base-deployment` | removed; each section keeps its ID and the rules that hold on any target |
| `backend-quality`: the handler, service and repository layering and its pattern catalogue | `backend-quality` | removed with the template; declare a stack's own architecture in a fork |
| `backend-quality`: process lifecycle, admin processes, outbound timeouts, auth before logic, rate limits | `backend-quality` | `backend-http` |
| `backend-quality`: N+1, async I/O, API deprecation, circuit breaker, outbox | `backend-quality` | already in `backend-database`, `backend-concurrency`, `backend-api`, `backend-errors`, `backend-messaging` |
| `frontend-static-site`: one stylesheet, BEM naming, system fonts, the `localStorage` theme snippet, the page table, lint and format files | `frontend-static-site` | removed with the template; a fork's static-site stack carries its choices |
| `static-site-theme`, `static-site-trailing-slash`, the custom 404 page, build-time rendering by default | `frontend-static-site` | `frontend-quality` and `frontend-content`, IDs kept |
| `base-oop`: SOLID, object design, patterns, cross-cutting concerns | the core tier | opt-in by `Extras`; the GoF catalogue and the AOP-framework ban are cut |
| The numbered-document check after concurrent merges, the first-CI-run rule for a check on its own change | `base-git` | the numbered-document check is removed, and the `check-heading-numbers` hook still ships; the first-CI-run rule stays in `base-git`; the playbook keeps this repository's own form |
| The in-process server, `testing-in-process-server` | `base-testing` | `frontend-quality`, ID kept |
| The refactor fingerprint, AST equivalence and public-API contract tests: `testing-characterization-fingerprint`, `testing-ast-equivalence`, `testing-ast-contract` | `base-testing` | the fingerprint moves to `base-quality-gates`, ID kept; the other two are removed, IDs included |
| The module-split procedure | `base-quality` | removed; the stable import paths and the untouched suite join Refactors in `base-quality-gates`, and the general module rules stay |
| Hierarchies: variadic overrides, the override checker and its contract test | `base-quality` | `base-oop` |
| Citing the software | `base-docs` | removed |
| The submodule update after a pin bump, the base64 bundle mask, the `.vscode` allowlist | `base-git` | all removed, the neutral editor-settings rule that replaced the allowlist included |
| Factory classmethods; `*-overlay.png` naming | `base-oop`, `base-quality` | neutral rules remain |
| Revisit triggers, `quality-revisit-trigger`; spike bars; the data directory; flag-selected rule sets; the package error hierarchy and its raise-walking test; return-type shims; extraction-ready modules; exact ports; auto-detect variants; `.editorconfig` and the old-checkout refresh; the citation test and audit; comment layout; probe naming; `scripts/` | `base-quality` | removed, ID included; the `check-comment-layout` and `find-unreferenced-scripts` hooks still ship |
| Self-match and the verdict rules from "Check trust" | `base-quality` | `base-quality-gates`, under "Running a check" |
| The markdownlint line-width check and its line-of-its-own setting; the Mermaid note characters; uniform node shapes; the bulk-emit stale count; per-field generators reading the schema | `base-docs` | removed; the width rules stay tool-neutral, with Mermaid only as an example |
| The work-email rule; the `gh` check-watch loop; bidirectional artifacts; the vendored-pointer default | `base-git` | removed; tool-neutral rules on registered checks and branch updates remain |
| Container e2e and test tiers, `testing-container-e2e` and `testing-tier-by-directory`; system, end-to-end and acceptance obligations; the regression cadence and budgets; integration-test naming | `base-testing` | removed, IDs included; a fork's stack can carry them. Doubles cover boundary-crossing dependencies only, and the deadline-wait rule joins Isolation |
| The structure audit's shared-module rule; the URL-parameter and principal and credential probe items | `base-review` | the shared-module rule removed, as `base-quality`'s DRY rule states it; neutral rules on external input and probe conditions remain |
| The secondary-toolchain rule, the auto-merge rule, the hierarchy control in a freeze retirement and ASCII-only output | `base-quality-gates` | removed; byte-exact test inputs, the aggregate CI job and the formatter ignore list are restated tool-neutrally |
| The browser-bundle runtime config file; the per-environment secrets table; the boolean `ENABLE_`/`DISABLE_` and group-prefix naming rules; the development-dependency split | `base-config` | removed; the table's test-stub row stays as a neutral rule |
| The agent-to-file mapping copy rule, the deprecated reference-model upgrade, the decision-record length rule, the monorepo package files, the brand-voice skeleton section | `base-agents` | removed; a file delivered by reference alone stays forbidden |
| The memory budget and checkpoints; the convergence escalation ladder; the spike deliverable; citing the software | `base-measurement` | removed; the convergence check, approximations, calibration and source silence remain, IDs kept |
| URI design; HATEOAS; query-parameter naming and reserved names; header-name spelling; the methods table; JSON by default; RFC 9457 errors; JWT by name; a port the process opens itself | `backend-http` | removed; malformed query values, header case, safe and idempotent methods and the JSON number rules remain, tool-neutral |
| The hand-authored spec served verbatim, the Schemathesis example, the SOAP rule, the duplicate deprecation-header block | `backend-api` | removed; the contract rules now cover every contract kind, and any second API style in one service needs a decision record, except REST for external and ops endpoints combined with gRPC for internal hot paths |
| The log-level table; HTTP status codes, `/health` paths and the `Trace-Id` header; OpenTelemetry and its collector as the required tool | `backend-observability` | removed; protocol- and vendor-neutral rules remain |

The core tier requires three documents only: `README.md`, `AGENTS.md` and
`CLAUDE.md`, both agent files on every project. Their layout is the
project's own; `templates/core/agents.md` offers a default.

## Removed templates

A 2.90.0 template ID listed here no longer resolves upstream. The Imbra fork
keeps every template the split moved to forks, under the same ID.

| ID | 2.90.0 file | Where its rules went |
| -- | ----------- | -------------------- |
| `stack-astro`, `stack-c-embedded`, `stack-django`, `stack-express`, `stack-fastapi`, `stack-flask`, `stack-go-echo`, `stack-go-lib`, `stack-go-service`, `stack-grpc-go`, `stack-grpc-python`, `stack-htmx`, `stack-nestjs`, `stack-nodejs-lib`, `stack-python-lib`, `stack-python-service`, `stack-tutorial` | `templates/stack/*.md` | a fork |
| `platform-github`, `platform-gitlab`, `platform-linear` | `templates/platform/*.md` | a fork |
| `base-360`, `base-ai-workflow`, `base-communication`, `base-compression`, `base-issues`, `base-release`, `base-scope`, `base-two-pass-review` | `templates/base/workflow/*.md`, except `quality-gates.md` | a fork |
| `base-c`, `base-go`, `base-python`, `base-typescript` | `templates/base/language/*.md` | a fork; idioms that hold in any language are rules in `base-quality` and `base-oop` |
| `base-readme`, core tier in 2.90.0 | `templates/base/core/readme.md` | a fork; the core tier requires `README.md` and prescribes no structure |
| `base-cli`, `base-skills`, `base-examples` | `templates/base/core/cli.md`, `templates/base/core/skills.md`, `templates/base/core/examples.md` | a fork |
| `backend-templating` | `templates/backend/templating.md` | a fork |
| `backend-quality` | `templates/backend/quality.md` | `backend-http` and the other backend templates; the layering and its pattern catalogue are removed |
| `frontend-static-site` | `templates/frontend/static-site.md` | `frontend-quality` and `frontend-content`; its stack choices are removed |

## Template paths

Every template still shipped keeps its ID. Files under `templates/base/`
lose that folder, except `quality-gates.md`, which moves from `workflow/`
into `core/`:

| ID | 2.90.0 file | 3.0.0 file |
| -- | ----------- | ---------- |
| `backend-api` | `templates/backend/api.md` | unchanged |
| `backend-auth` | `templates/backend/auth.md` | unchanged |
| `backend-caching` | `templates/backend/caching.md` | unchanged |
| `backend-concurrency` | `templates/backend/concurrency.md` | unchanged |
| `backend-database` | `templates/backend/database.md` | unchanged |
| `backend-edge` | `templates/backend/edge.md` | unchanged |
| `backend-errors` | `templates/backend/errors.md` | unchanged |
| `backend-features` | `templates/backend/features.md` | unchanged |
| `backend-grpc` | `templates/backend/grpc.md` | unchanged |
| `backend-http` | `templates/backend/http.md` | unchanged |
| `backend-jobs` | `templates/backend/jobs.md` | unchanged |
| `backend-messaging` | `templates/backend/messaging.md` | unchanged |
| `backend-microservices` | `templates/backend/microservices.md` | unchanged |
| `backend-monitoring` | `templates/backend/monitoring.md` | unchanged |
| `backend-observability` | `templates/backend/observability.md` | unchanged |
| `backend-webhooks` | `templates/backend/webhooks.md` | unchanged |
| `base-agents` | `templates/base/core/agents.md` | `templates/core/agents.md` |
| `base-config` | `templates/base/core/config.md` | `templates/core/config.md` |
| `base-docs` | `templates/base/core/docs.md` | `templates/core/docs.md` |
| `base-git` | `templates/base/core/git.md` | `templates/core/git.md` |
| `base-oop` | `templates/base/core/oop.md` | `templates/core/oop.md` |
| `base-quality` | `templates/base/core/quality.md` | `templates/core/quality.md` |
| `base-review` | `templates/base/core/review.md` | `templates/core/review.md` |
| `base-testing` | `templates/base/core/testing.md` | `templates/core/testing.md` |
| `base-data-governance` | `templates/base/data/data-governance.md` | `templates/data/data-governance.md` |
| `base-data-migration` | `templates/base/data/data-migration.md` | `templates/data/data-migration.md` |
| `base-data-modeling` | `templates/base/data/data-modeling.md` | `templates/data/data-modeling.md` |
| `base-data-quality` | `templates/base/data/data-quality.md` | `templates/data/data-quality.md` |
| `base-cicd` | `templates/base/infra/cicd.md` | `templates/infra/cicd.md` |
| `base-containers` | `templates/base/infra/containers.md` | `templates/infra/containers.md` |
| `base-deployment` | `templates/base/infra/deployment.md` | `templates/infra/deployment.md` |
| `base-devsecops` | `templates/base/security/devsecops.md` | `templates/security/devsecops.md` |
| `base-security` | `templates/base/security/security.md` | `templates/security/security.md` |
| `base-quality-gates` | `templates/base/workflow/quality-gates.md` | `templates/core/quality-gates.md` |
| `frontend-quality` | `templates/frontend/quality.md` | unchanged |
| `frontend-ux` | `templates/frontend/ux.md` | unchanged |

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

An `Extras` ID that no longer resolves is listed in
[Removed templates](#removed-templates); a path a context file names maps
through [Template paths](#template-paths).

No guide document a project carries is renamed — see
[Guide documents](#guide-documents).

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

### Renames the merge meets

Git carries upstream's own files through each rename. The fork's files
that name an old path do not follow, so edit them in the merge:

| Upstream change | Fork action |
| --------------- | ----------- |
| Templates leave `templates/base/`, and `quality-gates.md` moves into `core/` ([#1941], [#1966]) | Update every template path the fork's files name, `DEPENDS ON` lines included, per [Template paths](#template-paths) |
| Tools named verb-first: `resolve.py`, `sync.py`, `release_check.py`, `template_quality.py` become `resolve_chain.py`, `sync_docs.py`, `check_release.py`, `score_templates.py` ([#2052]) | Update every call and mention in `tests/fork_checks.py`, `tests/fork_dispositions.py`, `tests/cases.py`, `tests/run_e2e.py` and `tools/fork_examples.py` |
| `tests/lib.py` becomes `tests/testkit/` ([#2053], [#2055]) | `from lib import` becomes `from testkit import` |
| One wrapper runs every suite: `py tests/run.py <suite>` ([#2055]) | Move `tests/run_e2e.py` to `tests/e2e/run.py`; replace `py tests/run_smoke.py` with `py tests/run.py smoke` |
| Specs move from `tests/specs/` to `docs/tests/specs/` ([#2053]) | Move the fork's own specs there |
| The lint config moves from the root to `.github/linters/` ([#2049]) | Keep the fork's `.markdownlint.json`; its checks read the `prose` and `decision_layout` keys |

`tests/fork_checks.py` and `tests/fork_dispositions.py` stay where they
are: the smoke and conformance runners import them from `tests/`.

[#1941]: https://github.com/solid-ai-dev/solid-ai-templates/pull/1941
[#1966]: https://github.com/solid-ai-dev/solid-ai-templates/pull/1966
[#2049]: https://github.com/solid-ai-dev/solid-ai-templates/pull/2049
[#2052]: https://github.com/solid-ai-dev/solid-ai-templates/pull/2052
[#2053]: https://github.com/solid-ai-dev/solid-ai-templates/pull/2053
[#2055]: https://github.com/solid-ai-dev/solid-ai-templates/pull/2055

### Traps

| Trap | What happens | Fix |
| ---- | ------------ | --- |
| Fork key appended at the manifest's end | A downstream fork's appends conflict with it | Place the key above `stacks:` |
| Rewriting the manifest | Its trailing blank line goes, and SYS-20 reads an edit | Keep the file's end byte-identical |
| A sync PR merged by squash | The upstream link is lost, and the next sync re-merges the range | Merge every sync PR with a merge commit |
| Upstream's history in the fork's log | The merged-work sweep reads upstream's `(#N)` as the fork's issue `#N` | Set `UPSTREAM_REPO` (below), so CI excludes upstream's commits |
| The changelog-deletion check on a merge | It reads upstream's bullet as one the fork deleted | Run it on `--first-parent` |
| A tag-triggered workflow never registered | `gh run list --workflow release-gates.yml` returns 404 | Register it (below) |

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
