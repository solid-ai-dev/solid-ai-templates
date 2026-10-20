# Base — Documentation

[ID: base-docs]

Which documents a project keeps, and how they stay true.

## Rule language

- Read a plain imperative ("Use X", "Never Y") as MUST or MUST NOT
- Add an RFC 2119 key word where strength matters: SHOULD or MAY for a
  weaker rule, MUST to stress an absolute one

| Word | Meaning |
| --- | --- |
| MUST | Absolute requirement; no exception without stated rationale |
| MUST NOT | Absolute prohibition |
| SHOULD | Recommended; a deviation needs a justification |
| SHOULD NOT | Not recommended; may be ignored with a justification |
| MAY | Optional; the developer decides |

## Standard documents

- Carry these three in every project (MUST); their layout is the project's
  own, and `templates/core/agents.md` offers a default for the agent files

| File | Purpose |
| --- | --- |
| `README.md` | What the project is and how to use it |
| `AGENTS.md` | Agent context and project rules, for any agent |
| `CLAUDE.md` | Agent context and project rules, for Claude Code |

## Single source of truth

- Keep the project structure in `README.md` only, and reference it
  elsewhere
- Keep the agent files' project-structure section a pointer to the README
  plus placement rules, never a second directory tree
- Never reference a file, component or service that does not exist

## Upkeep

- Update every document a change touches, in the same commit:
  - `CLAUDE.md` when architecture, stack, design rules or conventions change
  - `README.md` when structure, stack or setup steps change
  - `AGENTS.md` whenever `CLAUDE.md` changes, so the two agree
- Write in present tense; past or future tense signals a stale document
- Write as little as needed; a document that drifts is worse than none
- Remove redundant, inconsistent or outdated text in the change that finds
  it

## Disagreements

- Establish which is wrong before changing a document or the system it
  contradicts
- Check whether the rule is inherited: a document generated from a template
  can drift while the system still matches the template
- Never act on the document alone when the observed state is defensible
  (MUST NOT)
- Read the document, observe the system, find the rule that governs both,
  then fix whichever one that rule does not support

## Adopting shared rules

- Treat template rules as candidates; the project chooses what it adopts
- Adopt a rule when it addresses a named local defect, a requirement or a
  credible material risk; a preventive security control needs no incident
- Never let a template update create compliance work, tickets or decision
  records by itself (MUST NOT); a newer tag alone is no reason to move the
  pin
- Record a declined candidate in at most one line, in the existing pull
  request or discussion
- Keep adopted rules in force until the project changes them, and keep the
  operative selection in the project's context file
- Inline this adoption boundary in a reference or hybrid context file
  (MUST), so a new upstream MUST cannot widen the adopted set
- Assess security fixes in tools the project runs promptly; review new
  conventions when a project need warrants it

## Line width

- Wrap Markdown at the width the project declares, never at one written
  into a rule
- Declare the width as the line-length setting in the Markdown linter's
  configuration (MUST); the linter reads no other file, so a width set only
  in `.editorconfig` goes unenforced
- Declare in the same place which of fenced blocks, table rows and headings
  are exempt
- Exempt a line only where an unbreakable token, a bare URL or a Markdown
  link, holds it over the width
- Enforce the width with the Markdown linter's line-length rule in CI
  (MUST), passing the configuration and the files to lint explicitly; a
  project that declares no width has no rule

```bash
CONFIG=<markdownlint-config>
widths=$(grep -c 'line_length' "$CONFIG" || true)
echo "width settings in $CONFIG: $widths"
status=0
out=$(npx --yes markdownlint-cli2 --config "$CONFIG" "**/*.md" 2>&1) || status=$?
files=$(echo "$out" | sed -n 's/^Linting: \([0-9]*\) file.*/\1/p')
echo "files linted: ${files:-0}"
echo "$out" | grep -E ' MD[0-9]{3}' || true
[ "$widths" -gt 0 ] && [ "${files:-0}" -gt 0 ] && exit "$status"
exit 1
```

Pass condition: both counts are non-zero, nothing follows them, and the
block exits zero. A zero width count means the linter falls back to its
default width, a zero file count means the globs reached nothing, and
either exits non-zero.

## Writing style

- Use full, grammatically correct sentences; lists are exempt
- Use bold and italic sparingly: never bold inline code or a whole
  sentence, and use at most one short bold label per list item
- Code-format only identifiers: file names, paths, environment variables
- Summarise a command, method, constant or flag in prose and link to its
  source; never transcribe it
- Point at a self-documenting source, such as `--help`, a generated schema
  or generated API docs, rather than restating it; document only what it
  cannot state itself
- State a count about the tree only inside a block a generator writes and
  gates; elsewhere name the thing without counting it

## Cold readers

[ID: docs-cold-reader]

- State the symptom before the mechanism
- Expand a term taken from the code at its first use, or avoid it
- Show a real example rather than describe one
- Keep to one idea per sentence
- Separate how bad it is now from how bad it becomes
- Apply these to every ticket, pull request and defect record an agent
  writes; the record outlives the session

## Diagrams and assets

- Prefer text-based diagrams: Mermaid for flowcharts, sequence diagrams and
  Gantt charts; Draw.io for complex visuals
- Commit every editable source beside its rendered output; never commit a
  binary-only diagram
- Give a committed artefact one authority: commit its editable source or
  its generator, never both
- Never use proprietary formats such as Word, Illustrator or Affinity
  Designer
- Use uniform node shapes, and split a diagram that serves two purposes

## Docs as code

- Keep technical documentation in the repository, in Markdown, under the
  same review as code

## Generated files

- Start every generated file with a banner naming the tool that wrote it
  and the command that refreshes it (SHOULD)
- Give every generator a `--check` flag that re-renders in memory and exits
  non-zero on a diff or a missing file, and require it in pre-commit and CI
  (SHOULD)
- Re-render to judge staleness; never rely on inspection, above all for a
  visual or binary output such as a diagram export
- Exclude generated paths from formatters
- Re-run the generator when its inputs change; never edit its output
- Derive a per-field generator's fields from the schema it renders, never
  from a hardcoded list (MUST)

## Citing the software (if applicable)

- Cite a persistent identifier as the citation of record, never a URL
  (MUST)
- Archive each release, mint an identifier, and cite the one that resolves
  to the latest version (SHOULD)
- Ship a machine-readable citation file at the repository root that records
  the identifier (SHOULD)
- Never present a project domain or vanity URL as the citation of record
  (MUST NOT)

## Output file by agent

| Agent | Context file |
| --- | --- |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/project.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| OpenAI Codex CLI | `AGENTS.md` |
| Generic or other | `AGENTS.md` |
