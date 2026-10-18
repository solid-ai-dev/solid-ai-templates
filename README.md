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

- Build `CLAUDE.md` or `AGENTS.md` from reusable layers — base, backend/frontend, stack
- Fork and extend — layer your team's conventions on the base without modifying it
- Codify industry standards — 12-factor app, OWASP, SOLID, SemVer, conventional commits
- Assemble templates you need, override if needed or create new ones

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

### Try it — clone and point the agent at the templates

*Fastest path. The agent picks the stack on its own — least
input from you, most variance in output.*

Clone the repo and tell the agent to generate from it:

```bash
git clone https://github.com/solid-ai-dev/solid-ai-templates.git
```

1. Open your agent in your project directory
2. Tell the agent:

```
Use solid-ai-templates/ to generate a CLAUDE.md for this
project. Start by reading templates/manifest.yaml to discover
the available stacks. Load every id in its core: list, then
follow the [DEPENDS ON] chain for the stack that fits. The
resolver seeds the core tier; a template may declare a core
file as well, but not every core file is declared, so the
chain alone is not enough.
```

3. The agent picks a matching stack, resolves the chain, and
   drafts the file
4. Review, adjust, and place at your project root

### Use it — clone and run the interview

*Guided path. The agent asks about your project before generating —
slower, but tighter fit to your context.*

Clone the templates and let the agent guide you through setup:

```bash
git clone https://github.com/solid-ai-dev/solid-ai-templates.git
```

1. Open your agent in your project directory
2. Tell the agent to read `solid-ai-templates/templates/INTERVIEW.md`
3. The agent asks about your project, proposes a stack, and reads
   the relevant templates
4. Confirm the stack — the agent generates `CLAUDE.md` or `AGENTS.md`
5. Place the generated file at your project root

The interview tends to produce a tighter fit than the
manifest-discovery path, because the agent gathers project
specifics from you before resolving the dependency chain (base
rules, layer rules, stack rules). Results depend on the model and
context window available.

### Adopt it — vendor as a submodule

For teams that want version-pinned templates inside their repo:

```bash
cd my-project
git submodule add https://github.com/solid-ai-dev/solid-ai-templates.git docs/solid-ai-templates
```

1. Open your agent in your project directory
2. Tell the agent to read `docs/solid-ai-templates/templates/INTERVIEW.md`
3. Follow the interview — the agent reads templates from the
   submodule and generates your context file
4. Commit the generated file alongside the submodule

To update templates: `git submodule update --remote`. Then
re-run the interview to regenerate your context file with the
latest rules.

## Model limitations

Template updates are selective: adopt new conventions for a project need or
material risk, not merely because a tag exists. Existing adopted rules remain
effective; declining a new rule needs no ADR or ticket. See the
[consumer migration guidance](docs/PLAYBOOK.md#adopt-a-template-policy-update).


Measured rather than estimated. Each row takes the largest resolved
chain in that category — the file under `generated/` an adopter
attaches — and converts it at 3.5 characters per token, a rate held
below the four-per-token rule of thumb because Markdown carrying
tables, fenced code and hyphenated identifiers tokenizes worse than
prose. The minimum window adds 18K tokens for the interview and the
file the model has to write back, then rounds up to the next window a
model actually sells.

`python3 tools/sync.py` regenerates the table from the chains and
`python3 tools/sync.py --check` fails when it drifts, so the figures move
when a base template grows instead of ageing quietly.

- **Output token limit < 16K** (e.g. GPT-4o default): generated file
  may be truncated — generate section by section or set `max_tokens`
  to the model maximum
- **Output token limit 32K+**: full inline file fits in one pass

## What a project picks

A project does not pick one template. It picks a **stack**, a **platform**,
and any **extras** it needs, and each one resolves independently: the core
tier plus that template's own `[DEPENDS ON]` tree. An extra is guaranteed
nothing from the stack it sits beside, which is why it can be added to any
of them.

```
your project
  |-- one stack        python-fastapi, go-service, htmx, ...
  |-- one platform     github, gitlab, linear
  `-- any extras       caching, jobs, release, deployment, ...
```

`python3 tools/resolve.py --roots` lists every root a project can pick. The
stacks are below; the rest are the extras table that follows them.

<!-- generated:readme-root-counts -->
Measured: 0 stacks and 38 orthogonal templates, 38 roots in all. An extra
resolves to the 6 core-tier files plus 0 to 5 of its own.
<!-- /generated:readme-root-counts -->

## Supported stacks

<!-- generated:readme-stacks -->
| Template | Layer | Description |
|----------|-------|-------------|
<!-- /generated:readme-stacks -->

## Platforms and extras

Picked independently of the stack, each resolving as its own root. The
examples under `examples/` cite several of these, so a reader who opens one
meets templates the stacks table does not list.

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

`generated/` holds a pre-resolved chain for each stack and none for these.
A stack chain spans dozens of files and is tedious to assemble by hand,
which is what a pre-resolved file is for; an extra brings a handful at
most, so reading the template and the core tier is the shorter path.
Attach the template directly, or run `python3 tools/resolve.py <root>
--concat` to get its chain the same way.

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
- [Example generated context files](examples/)
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
