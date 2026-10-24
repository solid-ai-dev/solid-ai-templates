# Base — Agent Context Files

[ID: base-agents]

How a project's agent context files are structured and written.

## Output files

| File | Role |
| --- | --- |
| `AGENTS.md` | The cross-agent file, read by any agent without a native file |
| `CLAUDE.md` | The file Claude Code reads |

- Carry both files in every project, whichever agent it uses (MUST)
- Generate both with the same rules, or let `CLAUDE.md` import `AGENTS.md`
  (`@AGENTS.md`) and add only Claude-specific rules
- Never let the two disagree; a change to one is a change to both
- Add an agent's native context file of another name beside the two
- Generate every copy of the agent-to-file mapping from the one table in
  the documentation rules, and gate the copy like any generated block

## Choosing a model

| | Inline | Hybrid |
| --- | --- | --- |
| Runtime | Every adopted rule in context | Silent, unenforced rules in context; the rest read on demand |
| Reliability | Highest | High; every rule a missed read would break stays in context |
| Maintenance | Rules drift from the templates | Project rules drift; referenced rules stay in sync |
| Best for | A project that does not vendor the templates | A project that vendors them as a submodule |

- Generate inline or hybrid; never a file that delivers its rules by
  reference alone, which nothing loads (MUST NOT)
- Default to hybrid when the project vendors the templates, inline
  otherwise
- Regenerate a file made under the deprecated reference model as hybrid

## Placing a rule

| Breaking the rule... | A test, linter or CI step enforces it | Nothing enforces it |
| --- | --- | --- |
| shows an error | MAY reference | MAY reference |
| is silent | MAY reference | MUST inline |

- Inline a rule whose breaking is silent and that no test, linter or CI
  step enforces (MUST)
- Reference any other rule by naming the template that holds it (MAY)

## Quality bar

- Make every line a rule the agent applies on the next turn; no changelog,
  architecture notes or progress log
- Keep every qualifier a rule needs; never compress away a load-bearing
  clause
- Never treat a rule's length, shortened or lengthened, as a reason to
  write a decision record
- Put explanations in the documents they belong to, not the context file
- Point to a rule that is authoritative in a skill, ADR, README or template;
  never restate it unless the model below inlines it
- State the override order near the top when more than one rule source
  governs the project
- Name the check beside each mechanically checkable rule: the command in a
  fenced block, the pass condition in prose

### Self-check

Run against a drafted file before delivering it; a failing item is a fix,
not a note.

- [ ] Every line states a rule the agent applies next turn
- [ ] Every qualifier a rule needs survives
- [ ] No prose restates a rule authoritative elsewhere, beyond what the
      model inlines
- [ ] The precedence order is stated where several authorities govern
- [ ] Every mechanically checkable constraint names its check
- [ ] The project-structure section points to the README map, with no
      second directory tree

## Required parts

[ID: agents-project-questions]

- Carry each part, in any order, numbering or naming (MUST): the project's
  identity, structure and commands; the rules it adopts; how a change is
  reviewed; and its answers to the questions below
- State a part that does not apply as not applicable; never drop it
- Answer each of these questions, or name it as open for the project to
  decide (MUST):
  - Who approves a change?
  - How is work tracked?
  - What is a release?
- Render an end-of-session checklist verbatim, or delegate it with an
  order to read it and execute each item in sequence, without summarizing
  or skipping any; never paraphrase it into a shorter list (MUST NOT)

## Inline model

- Inline every rule the project adopts, so the file is self-contained; a
  template rule it has not adopted stays out
- Regenerate without widening the adopted set: a rule upstream adds after
  adoption stays out until the project adopts it (MUST)
- Add `Model: inline` to the overview
- Number the headings so other documents can cite a rule, such as "see
  section 2.3" (SHOULD); a project MAY keep its own numbering

```markdown
# [Project Name]

[One-sentence description]
[Owner, repo URL, live URL if applicable]
- Model: inline

## 1. Project
### 1.1 Overview
### 1.2 Project structure
[Pointer to the README map, plus agent-specific placement rules]
### 1.3 Commands

## 2. Code conventions
### 2.1 Git
### 2.2 [Language]

## 3. Quality
### 3.1 Testing

## 4. Identity
[Design and brand voice, if applicable]

## 5. Review process
[Priority order and checklists from templates/core/review.md]

## 6. Session protocol
[How a session starts, proceeds and ends]
```

## Hybrid model

- Inline every rule "Placing a rule" marks MUST inline, and reference the
  templates for the rest
- Add `Model: hybrid` to the overview, so agents read the referenced
  templates before starting
- Inline these, which most often break silently: git conventions, file
  placement rules, language safety rules, content and style rules, and the
  session protocol
- Reference only rules whose breaking shows an error or that a tool
  enforces, from quality, review, testing, documentation, accessibility,
  SEO and delivery; never reference one of these areas whole
- Inline the adoption boundary: adopted rules stay in force, and reading a
  new upstream rule or moving the pin adopts nothing (MUST)
- Exclude the vendored submodule from every tool that walks the tree
  (linters, formatters, secret scanners, spell and link checkers) before
  the first commit (MUST)

```markdown
# [Project Name]

[One-sentence description]

Quality conventions are defined in `docs/solid-ai-templates/` (submodule).
Key references:
- [Every template in the resolved chain]

## 1. Project
### 1.1 Identity
- Model: hybrid
[Owner, repo URL, stack, hosting]
### 1.2 Project structure
[Pointer to the README map, plus agent-specific placement rules]
### 1.3 Commands

## 2. Code conventions
[Inlined: git, language safety, content and data rules]

## 3. Quality
[Inlined: every rule "Placing a rule" marks MUST inline]

## 4. Identity
[Design and brand voice, if applicable]

## 5. Review process
[Inlined: every review rule marked MUST inline; reference the rest]

## 6. Session protocol
[How a session starts, proceeds and ends]
```

## Monorepos (if applicable)

- Add a package-level context file for package-specific rules, for agents
  that read every file from the root to the working directory
- Keep only rules that differ from or extend the root in a package file
  (SHOULD)

## Formatting

- Put every command and code sample in a fenced block with a language tag
- Write rules as bullet lists; avoid prose paragraphs inside rule sections
  (SHOULD)
- Wrap at the width the project declares in its own configuration
- Use Markdown only; no HTML

## Tone

- Write imperatives: "Use X", "Never do Y", "Always Z"
- Add explanatory prose only where a rule needs context to be followed
- Address the agent, not a human reader
