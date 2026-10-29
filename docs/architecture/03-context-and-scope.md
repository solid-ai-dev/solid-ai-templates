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

Each exchange of 3.1, the channel that carries it and who opens it.

| Exchange | Transport | Opened by |
|----------|-----------|-----------|
| Upstream changes to a fork | `git fetch upstream` from GitHub | The fork maintainer |
| Reports and proposals | An issue on GitHub, through an issue form | The reporter |
| A rule change with evidence | A pull request on GitHub | The contributor |
| Templates and tools to a project, solid-ai-dirigent among them | A clone, or a submodule pinned to a released tag, from upstream or a fork | The project |
| Chain and task skills to an agent | Files in the project's checkout, read through `tools/resolve_chain.py` | The agent |
| Hooks to a project's CI | pre-commit fetches upstream at a pinned revision | The project's pre-commit |
| A release to the benchmark | A clone of upstream or a fork at the release registered for the round | The benchmark |
| Efficacy results to upstream | A pull request adding the round's report under `docs/audits/` | The maintainer |
| Repository and CI runs | `git push` to GitHub, and Actions on every pull request and push to `main` | The maintainer and CI |

## 3.3 Out of scope

Upstream leaves these to the team and to other tools.

- product requirements or feature specification
- issue tracking or project management
- task decomposition, agent planning or multi-agent orchestration
- general-purpose prompt libraries
- CI infrastructure itself
