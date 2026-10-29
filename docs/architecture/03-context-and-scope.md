# 3. Context and scope

## 3.1 Business context

![Upstream holds the engine and shared policy; three forks, Imbra's among them, merge it with git merge upstream/main; each fork hands a project's agent the interview and a resolved chain](../diagrams/fork-model.png)

| Partner | Gives upstream | Takes from upstream |
|---------|----------------|---------------------|
| Fork | Defect reports and proposals for shared rules | The engine, the shared templates and the checks, by `git merge upstream/main` |
| Consumer project | Nothing directly; it works through a fork | A context file its agent generates from the fork's interview and a resolved chain |
| Coding agent | — | The chain and the output contract in `templates/core/agents.md` |

A project uses a fork, or forks upstream to make its own. Upstream alone
ships no stack and no interview. A project takes the fork's rules in one of
two ways.

| Way | When | How |
|-----|------|-----|
| Clone | To try it | The agent clones the fork next to the project and generates the context file from it |
| Submodule | To use it | The project adds the fork as a submodule pinned to a released tag, and moves the pin to adopt a release (playbook, "Vendor the templates in a project") |

## 3.2 What upstream owns

![Upstream keeps the engine, shared policy, language-neutral rules and the questions; each fork carries stacks, platforms, workflow, process and the answers; git.md, docs.md and quality-gates.md split between the two](../diagrams/template-boundary.png)

| Upstream owns | A fork owns |
|---------------|-------------|
| The resolver, sync and the checks (`tools/`, `tests/`) | Stacks and platforms |
| Shared policy: `core/`, `security/`, `infra/`, `data/`, `backend/`, `frontend/` | Workflow and process rules |
| The questions every project answers (`core/agents.md`) | The interview and the answers |
| The fixture stack and platform, test input only | Examples and generated chains |
| The manifest keys `core`, `base`, `backend`, `frontend` | `stacks`, `platform`, `fork_core` and keys of its own |

ADR-049 sets the fork model and ADR-050 the boundary.

## 3.3 Out of scope

The library states what software must satisfy. It does not own:

- product requirements or feature specification
- issue tracking or project management
- task decomposition, agent planning or multi-agent orchestration
- general-purpose prompt libraries
- CI infrastructure itself

| Question | Answered by |
|----------|-------------|
| What are we building? | Specification and intent |
| How should an agent perform a task? | A skill or methodology |
| What rules must the result satisfy? | **These templates** |
| How is work orchestrated? | Planning and orchestration tooling |
| Is the result correct? | Tests, CI, security and policy checks |
