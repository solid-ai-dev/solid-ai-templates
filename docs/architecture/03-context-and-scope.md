# 3. Context and scope

## 3.1 Business context

Upstream as one box, with the people and systems on its boundary. In and
out are seen from upstream.

![Upstream as one box with its neighbours. A fork maintainer sends reports and proposals in and takes the engine, templates and checks out by merge. An upstream contributor sends rule changes with evidence in and gets admission or a reasoned decline. A team using agents gets the templates and tools, from upstream or a fork, by clone or submodule. A coding agent gets the chain, the output contract and the task skills, and writes the context file from them. solid-ai-dirigent takes the rules as a pinned submodule. solid-ai-benchmark takes a tagged ref and returns efficacy results. pre-commit in a project's CI takes the shipped hooks. GitHub holds the repository and returns issues, pull requests and CI runs](../diagrams/context-business.png)

| Neighbour | Gives upstream | Gets from upstream | Source |
|-----------|----------------|--------------------|--------|
| Fork maintainer | Reports and proposals for shared rules | The engine, the shared templates and the checks, by merge | FR-08-01, FR-08-02, ADR-049 |
| Upstream contributor | A rule change with evidence that it helps | Admission, or a decline with its reason | FR-10-01, FR-10-02 |
| Team using agents | - | The templates and tools, from upstream or from a fork for its stacks, by clone or submodule | FR-08-04 |
| Coding agent | - | The chain, the output contract and the task skills, from which it writes the project's context file | FR-05-01, FR-05-02, FR-05-04, FR-06-04 |
| solid-ai-dirigent | - | The rules its developer and reviewer agents follow, as a pinned submodule | FR-08-04 |
| solid-ai-benchmark | Efficacy results for a release | A tagged ref to measure | QG-01-02 |
| pre-commit, in a project's CI | - | The shipped hooks | FR-07-02, ADR-055 |
| GitHub | Issues, pull requests and CI runs | The repository | Chapter 2, 2.3 #4 |

## 3.2 Technical context

Each exchange of 3.1, the channel that carries it and what the receiver
then does with it locally.

![Upstream holds the engine and shared policy; three forks, Imbra's among them, fetch it and merge it with git merge upstream/main; each fork hands a project's agent the interview and a resolved chain](../diagrams/fork-model.png)

| Exchange | Transport | Local step | Opened by | Source |
|----------|-----------|------------|-----------|--------|
| Upstream changes to a fork | `git fetch upstream` from GitHub | `git merge upstream/main` in the fork, then smoke | The fork maintainer | FR-08-01, ADR-049 |
| Reports and proposals | An issue on GitHub, through an issue form | Triage labels it, or closes it with the reason | The reporter | Chapter 2, 2.3 #4 |
| A rule change with evidence | A pull request on GitHub | CI runs the self-checks; the maintainer merges it or closes it with the reason | The contributor | FR-10-01, Chapter 2, 2.3 #1 |
| Templates and tools to a project, solid-ai-dirigent among them | A clone, or a submodule pinned to a released tag, from upstream or a fork | Moving the pin adopts a release | The project | FR-08-04, FR-09-03 |
| Chain and task skills to an agent | Files in the project's checkout | `tools/resolve_chain.py`, a root in and a file list, chain or emitted files out; the agent writes the context file | The agent | FR-04-01, FR-05-01, FR-06-03 |
| Hooks to a project's CI | pre-commit fetches upstream at a pinned revision | pre-commit runs the hooks `.pre-commit-hooks.yaml` lists | The project's pre-commit | FR-07-02, ADR-055 |
| A release to the benchmark | A clone of upstream or a fork at the release registered for the round | The benchmark generates the files and runs its tasks | The benchmark | QG-01-02 |
| Efficacy results to upstream | A pull request adding the round's report under `docs/audits/` | The maintainer reads it against the quality goals | The maintainer | QG-01-02 |
| Repository and CI runs | `git push` to GitHub | Actions runs CI on every pull request and push to `main` | The maintainer and CI | FR-10-01, Chapter 2, 2.3 #4 |

## 3.3 What upstream owns

![Upstream keeps the engine, shared policy, language-neutral rules and the questions; each fork carries stacks, platforms, workflow, process and the answers; git.md, docs.md and quality-gates.md split between the two](../diagrams/template-boundary.png)

| Upstream owns | A fork owns |
|---------------|-------------|
| The resolver, sync and the checks (`tools/`, `tests/`) | Stacks and platforms |
| Shared policy in `core/`, `security/`, `infra/`, `data/`, `backend/`, `frontend/` | Workflow and process rules |
| The questions every project answers (`core/agents.md`) | The interview and the answers |
| The fixture stack and platform, test input only | Examples and generated chains |
| The manifest keys `core`, `base`, `backend`, `frontend` | `stacks`, `platform`, `fork_core` and keys of its own |

ADR-049 sets the fork model and ADR-050 the boundary.

## 3.4 Out of scope

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
