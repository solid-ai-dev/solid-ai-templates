# SOLID-AI Templates

*Forged in real work, not theorized — every rule here came from a real
AI-assisted project.*

You've shipped the same CLAUDE.md three times this quarter. Each copy is
slightly different, none of them are right, and the agent still doesn't
know your team's conventions.

You're not alone, and it's not negligence — writing context files from
scratch is the quiet cost of every agent-assisted team. Everyone pays
it, few teams have a system for it, and the codebase drifts a little
further from your standards every sprint.

This repo gives you composable templates that codify your team's
conventions once — base rules, stack rules, company rules — and feed
them to every agent on every project. Tax paid. Move on.

Back to the work that actually moves the product. The spikes, the design
conversations, the reviews that catch bugs instead of churning style nits.

## What it does

- Build `CLAUDE.md` or `AGENTS.md` from reusable layers — core, backend/frontend,
  and a stack from a fork
- Fork and extend — layer your team's stacks and process on the shared policy
  without modifying it
- Codify industry standards — 12-factor app, OWASP, SOLID
- Assemble the templates you need, override where needed, or create new ones

This repository holds the composition engine and the policy every team
shares. Stacks, platforms, process rules, the interview, examples and
pre-resolved chains live in forks
([ADR-049](docs/decisions/049-forks-carry-stacks-and-process.md),
[ADR-050](docs/decisions/050-what-stays-upstream.md)).

## How to use

**Prerequisites:** a local coding agent that can read files from
your project directory (Claude Code, Cursor, Codex CLI, Windsurf,
or similar). The optional `tools/` scripts also need Python 3 and
PyYAML (`pip install pyyaml`); commands below use `python3`, which
on Windows is `py`.

**Output:** a `CLAUDE.md` or `AGENTS.md` file placed at your project
root, containing coding conventions tailored to your stack. Works
for new projects and refactoring alike — the context file describes
how code *should be written*, giving your agent a consistent target
whether starting from scratch or improving existing code. Review and
adjust the output before adopting it — results vary by model and
prompt size.

Upstream alone ships no stacks and no interview, so a project generates
its context file from a fork: use one, or fork this repository.

### Use a fork

For Imbra's stacks, platforms and process, use
[imbra-ai-templates](https://github.com/Imbra-Ltd/imbra-ai-templates). It
carries the interview and a resolved chain for each stack; its README
describes how to hand them to your agent.

### Fork it

To carry your own stacks, platforms and process, fork this repository on
GitHub and keep it current by merging upstream:

```bash
git remote add upstream https://github.com/solid-ai-dev/solid-ai-templates.git
git fetch upstream
git merge upstream/main
```

A fork follows the rules in
[ADR-049](docs/decisions/049-forks-carry-stacks-and-process.md):

- Append under `stacks:`, `platform:` and top-level manifest keys of your
  own, and add to every chain's core tier under `fork_core:`
- Never edit `core:`, `base:`, `backend:` or `frontend:` in the manifest;
  smoke check SYS-20 fails when a fork does
- Keep `README.md`, `CLAUDE.md` and `CHANGELOG.md` as your own, resolving
  them in your favour on every merge
- Merge an upstream commit carrying the `Fork-merge: ours` trailer in two
  steps: its parent normally, then the commit with `git merge -s ours`.
  Then move your own templates out of upstream's keys into your own key
  and `fork_core:`

### Take an update

Template updates are selective: adopt new conventions for a project need or
material risk, not merely because a tag exists. Existing adopted rules remain
effective; declining a new rule needs no ADR or ticket. See the
[consumer migration guidance](docs/PLAYBOOK.md#adopt-a-template-policy-update).

## What a project picks

A project does not pick one template. It picks a **stack** and a
**platform** from a fork, and any **extras** it needs, and each one resolves
independently: the core tier plus that template's own `[DEPENDS ON]` tree.
An extra is guaranteed nothing from the stack it sits beside, which is why
it can be added to any of them.

```
your project
  |-- one stack        from a fork
  |-- one platform     from a fork
  `-- any extras       caching, jobs, deployment, ...
```

`python3 tools/resolve.py --roots` lists every root a project can pick. In
upstream these are the shared templates below; a fork adds its stacks and
platforms.

<!-- generated:readme-root-counts -->
Measured: 0 stacks and 38 orthogonal templates, 38 roots in all. An extra
resolves to the 6 core-tier files plus 0 to 5 of its own.
<!-- /generated:readme-root-counts -->

## Stacks

Upstream ships no stacks, so this table is empty here. A fork's sync fills
it with the stacks that fork carries.

<!-- generated:readme-stacks -->
| Template | Layer | Description |
|----------|-------|-------------|
<!-- /generated:readme-stacks -->

## Shared templates

Picked independently of the stack, each resolving as its own root.

<!-- generated:readme-extras -->
| Template | Kind | Description |
|----------|------|-------------|
| `templates/backend/api.md` | backend | API-first, OpenAPI, versioning, deprecation, pagination |
| `templates/backend/auth.md` | backend | Authn/authz, JWT, RBAC, sessions, API keys |
| `templates/backend/caching.md` | backend | Cache-aside, TTL, invalidation, resilience, stampede |
| `templates/backend/concurrency.md` | backend | Threads vs. processes vs. async, shared state, structured concurrency |
| `templates/backend/database.md` | backend | Migrations, transactions, no raw SQL, connection pooling |
| `templates/backend/edge.md` | backend | Reverse proxy / edge — TLS termination, forwarded headers, upstream routing, timeouts, edge security |
| `templates/backend/errors.md` | backend | Classification, propagation, recovery, external failures |
| `templates/backend/features.md` | backend | Feature flags, rollout strategy, experimentation |
| `templates/backend/grpc.md` | backend | Proto design, status codes, interceptors, health check |
| `templates/backend/http.md` | backend | URI design, methods, headers, HATEOAS, auth, errors |
| `templates/backend/jobs.md` | backend | Background jobs, idempotency, retry, DLQ, scheduling |
| `templates/backend/messaging.md` | backend | Brokers, producers, consumers, schema, DLQ, observability |
| `templates/backend/microservices.md` | backend | Service boundaries, inter-service comms, saga, contract testing |
| `templates/backend/monitoring.md` | backend | Key metrics, thresholds, alerts, dashboards, incidents |
| `templates/backend/observability.md` | backend | Log levels, log format, health check, error visibility |
| `templates/backend/quality.md` | backend | Layered architecture, security, performance, API stability |
| `templates/backend/webhooks.md` | backend | Inbound webhook intake, edge signature verification, fast-ack, retry amplification |
| `templates/core/agents.md` | core | Output structure, models (inline/hybrid), formatting rules |
| `templates/infra/cicd.md` | infra | Pipeline stages, triggers, environments, IaC, deployment |
| `templates/core/config.md` | core | Env vars, secrets, fail-fast validation |
| `templates/infra/containers.md` | infra | Dockerfile, runtime security, resource limits, Kubernetes |
| `templates/data/data-governance.md` | data | Classification, PII handling, retention, ownership, audit trail |
| `templates/data/data-migration.md` | data | Versioned migrations, zero-downtime, rollback strategies |
| `templates/data/data-modeling.md` | data | Schema design, naming, normalization, relationships, data types |
| `templates/data/data-quality.md` | data | Data sourcing, completeness, freshness, research, scoring — data-heavy projects |
| `templates/infra/deployment.md` | infra | Deployment targets (cloud/hybrid/offline), certs, LB, registries, secrets |
| `templates/security/devsecops.md` | security | SAST, SCA, SBOM, secret detection, license compliance |
| `templates/core/docs.md` | core | Rule language, documentation standards, ADR, diagrams, docs-as-code |
| `templates/core/git.md` | core | Committer identity, commits, branching, PR workflow, versioning |
| `templates/core/oop.md` | core | SOLID, OOP, GoF design patterns, AOP guidance |
| `templates/core/quality.md` | core | Architecture, code style, calibration, tool trust, testing |
| `templates/core/quality-gates.md` | core | Three-layer gate model (editor, pre-commit, CI), thresholds |
| `templates/core/review.md` | core | Peer review priority, MUST/SHOULD checklists, deviation rules |
| `templates/security/security.md` | security | Application security rules — input, output, injection, auth, sessions, TLS, headers |
| `templates/core/testing.md` | core | Test pyramid, coverage thresholds, naming conventions |
| `templates/frontend/quality.md` | frontend | CSS conventions, performance, SEO & analytics |
| `templates/frontend/static-site.md` | frontend | Abstract SSG rules — content, assets, SEO |
| `templates/frontend/ux.md` | frontend | UX principles, WCAG 2.1 AA, responsive breakpoints |
<!-- /generated:readme-extras -->

Upstream commits no pre-resolved chains. Attach a template and the core
tier directly, or run `python3 tools/resolve.py <root> --concat` to get its
chain in one piece.

## Supported agents

<!-- generated:readme-agents -->
| Agent | Output file |
|-------|-------------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/project.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| OpenAI Codex CLI | `AGENTS.md` |
| Generic / other | `AI_CONTEXT.md` |
<!-- /generated:readme-agents -->

See `templates/core/agents.md` for structure, models, and formatting rules.

## Links

- [System design and composition rules](docs/SPEC.md)
- [Changelog](CHANGELOG.md)
- [Project status and roadmap](https://github.com/solid-ai-dev/solid-ai-templates/milestones)
- [Imbra's fork, with stacks and examples](https://github.com/Imbra-Ltd/imbra-ai-templates)
- [Onboarding guide](docs/ONBOARDING.md)
- [Operational playbook](docs/PLAYBOOK.md)
- [Architecture decision records](docs/decisions/)
- [How to contribute](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Report an issue](https://github.com/solid-ai-dev/solid-ai-templates/issues)

## License

[CC BY 4.0](LICENSE) — Creative Commons Attribution 4.0 International.
You are free to use, share, and adapt the templates for any purpose,
including commercial use, as long as you give attribution.

## Author

[Branimir Georgiev](https://github.com/braboj) — [Imbra.io](https://imbra.io)
