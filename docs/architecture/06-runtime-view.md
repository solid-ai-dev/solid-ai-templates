# 6. Runtime view

## 6.1 Generating a context file

```text
fork's interview ─┐
                  ├─► agent ─► merges base defaults + stack overrides
resolved chain  ──┤            + interview answers
core/agents.md  ──┘            └─► writes AGENTS.md / CLAUDE.md
```

1. The user gives the agent a fork's interview and a stack, or the fork's
   pre-resolved chain for that stack
2. The agent reads the stack and loads its dependencies, upstream's and the
   fork's
3. The agent asks the required questions; defaults come from the chain
4. The agent merges base defaults, stack overrides and answers, in the
   precedence of chapter 8
5. The agent writes the file to the output contract in
   `templates/core/agents.md`

Generation stays an agent reading Markdown: no build step or compiler sits
between the fork and the context file.

## 6.2 Lifecycle of a project

```text
1. SETUP (once)     interview -> context file, inline or hybrid
2. DEVELOPMENT      agent reads the context file; a hybrid file names
                    templates the agent opens when they apply
3. UPDATE           fork merges upstream; project moves its pin
```

Moving the pin changes nothing in an existing context file. An inline file
keeps its rules until the project regenerates it or adopts a change by
hand, and a newer version never adopts itself: the project assesses what
changed and adopts it deliberately ("Adopting shared rules" in
`templates/core/docs.md`).

## 6.3 Declaration block and startup resolution (target)

Proposed, not implemented: no interview writes the block and no tool reads
it, so it is outside the 3.x frozen surface and a minor may change its
fields (ADR-053). The generated file would carry a machine-readable header
instead of a hand-curated file list, and each session would resolve the
chain from it:

```text
SETUP (once)          interview -> context file with a declaration block
STARTUP (per session) context file -> fork's manifest -> resolved chain
UPDATE                after the pin moves, the next session resolves
                      the new chain
```

```markdown
Stack: stack-astro
Extras: base-data-quality, base-360, base-issues, base-scope, base-readme
Platform: platform-github
```

| Field | Required | Holds |
|-------|----------|-------|
| `Stack` | MUST | A stack ID from the fork's manifest |
| `Extras` | MAY | Template IDs outside the stack's chain, comma-separated |
| `Platform` | MAY | A platform ID from the fork |

The IDs above are the Imbra fork's; `py tools/resolve.py --roots` lists the
ones a checkout carries.

## 6.4 Resolution

Input: a root and the manifest. Output: the ordered list of files to load.
Today `tools/resolve.py` resolves one root, steps 1 to 3 and 6. Steps 4 and
5 belong to the declaration block of section 6.3 and are proposed.

Without Python, follow steps 1 to 3 by hand: load every file in the
manifest's `core:` list, then the root's file and every file its
`[DEPENDS ON]` lines name, transitively. Skipping the `core:` list loses
rules with no error, because no template declares those files.

```text
1. Seed the core tier: core:, then fork_core:
2. Look up the stack ID in the manifest
3. Resolve depends_on recursively, depth-first, deduplicated
4. Resolve each extra the same way: its tree first, then itself,
   skipping anything already resolved
5. Resolve the platform the same way, if declared
6. Return the ordered list
```

Order is base, then layer, then stack: a topological sort of the graph, and
within one depth the order `depends_on` declares. `core/agents.md` is not
appended; a project that wants it in the chain declares it as an extra.

```bash
py tools/resolve.py <id>            # the file list
py tools/resolve.py <id> --concat   # the concatenated chain
```

## 6.5 A fork taking an upstream change

```text
upstream main ──merge──► fork ──► fork's smoke ──► fork's projects
                  │
                  └─ commit with "Fork-merge: ours":
                     merge it with -s ours, move the fork's templates
                     to its own keys, restore upstream's text
```

`py tests/run_fork_sync.py` simulates this on every pull request: it lands
the change on a fork that appends a stack and edits its fork-owned files,
and asserts the merge is otherwise clean. The playbook, "Sync with upstream
as a fork", gives the steps.
