# Base — Documentation

[ID: base-docs]

## Rule language

A rule is either a plain imperative ("Use X", "Never Y") or a sentence
carrying one of the **RFC 2119** key words below. A plain imperative reads
as MUST or MUST NOT. Use a key word where strength matters: SHOULD or MAY
for anything weaker, MUST to stress an absolute one.

| Word       | Meaning                                                         |
| ---------- | --------------------------------------------------------------- |
| MUST       | Absolute requirement — no exceptions without explicit rationale |
| MUST NOT   | Absolute prohibition                                            |
| SHOULD     | Recommended — deviations require justification                  |
| SHOULD NOT | Not recommended — may be ignored with justification             |
| MAY        | Optional — developer decides without further discussion         |

## Single source of truth

- `README.md` is the single source of truth for project structure
- Do not duplicate structure in other documents — reference `README.md` instead
- Agent context files (`CLAUDE.md` / `AGENTS.md`) keep their Project
  structure section as a pointer to the README section plus
  agent-specific placement rules — never a second directory tree
- No references to non-existent files, components, or services

## Standard documents

Every project MUST carry these three. Their layout is the project's own.
`core/agents.md` states what `AGENTS.md` and `CLAUDE.md` must contain and
offers a default layout; no template prescribes the README's.

| File        | Purpose                                         |
| ----------- | ----------------------------------------------- |
| `README.md` | What the project is and how to use it           |
| `AGENTS.md` | Agent context and project rules, for any agent  |
| `CLAUDE.md` | Agent context and project rules, for Claude Code |

## Documentation rule

Before every commit, update all relevant documentation:

- **`CLAUDE.md`** — update if architecture, stack, design rules, or conventions
  change
- **`README.md`** — update if project structure, stack, or setup steps change
- **`AGENTS.md`** — update whenever `CLAUDE.md` changes, so the two agree

### Changing a document other repositories carry

A project that defines documents for other repositories — a template
system, a shared configuration, a house style — reaches only its own tree
with its own generator. Renaming or restructuring one of those documents
costs the consumers, and that cost is invisible from here.

- A proposal to rename or restructure such a document MUST state how many
  repositories carry it and what the change costs them, measured rather
  than estimated, and MUST carry the date the measurement was taken. A
  survey quoted later without its date asserts about today's trees what
  was true on the day it ran
- Measure by fetching each repository's default-branch tree once and
  testing exact paths against it, not by asking the host for each path
  separately. A per-path probe answers for a missing file by printing an
  error body, which a field selector reads as a value, so every repository
  reports a hit and the survey looks complete. Carry a control path that
  MUST be absent everywhere through the same probe: a survey whose control
  is found is measuring nothing
- Count occurrences over tracked files. A walk of the working tree reads
  the version-control directory and whatever the build left behind, and a
  count of matching lines counts a line carrying two mentions once — the
  two errors push in opposite directions, so agreement between them proves
  nothing. Reconcile the per-area sum against the total, so an area the
  enumeration missed shows as a gap rather than as a smaller number
  nobody questions

### When a document disagrees with the system

A project document that contradicts the live state of the system it
describes is not automatically the authority. Establish which one is
wrong before changing either.

- MUST check whether the rule is inherited. A document generated from a
  template can drift from the template while the system still matches
  it — in which case the document is stale and the system is correct
- MUST NOT act on the document's reading alone when the observed state
  is defensible. Acting first destroys a correct configuration to
  satisfy a sentence that was already out of date
- The order is: read the document, observe the system, then find the
  rule that governs both. Reconcile to whichever the governing rule
  supports, and fix the other

## Adopting shared rules

- Templates supply candidate conventions; the project chooses what it adopts.
  Resolve dependencies to discover the available rules, not to authorize work.
- Adopt a new rule when it addresses a named local defect, requirement, or
  credible material risk. Preventive security controls need no prior incident.
- A template update MUST NOT automatically create compliance work, tickets,
  or decision records. A newer tag alone is not a reason to update the pin.
- A declined candidate needs at most a line in the existing PR or discussion;
  no ADR, separate ticket, or decline register is required.
- Existing adopted rules remain effective until the project changes them.
  Keep the operative selection and any necessary precedence in the project's
  context file; a reference/hybrid file MUST inline this adoption boundary so
  reading a new upstream MUST cannot silently expand the adopted rule set.
- Assess security fixes in tools the project executes promptly. Review new
  conventions when a project need warrants it, rather than on every release.

## Retiring a document

- Retiring a document does not retire what it says. Scope the removal by
  searching the tree for the CONTENT — the incident, the identifier, the
  material — never by deleting the file named for it
- The journal is the surface most likely to be missed: it is append-only,
  organised by date rather than by topic, and its post-mortems routinely
  restate an incident in more detail than the report that triggered it
- Where a surviving copy is sensitive, state the finding to whoever owns the
  repository rather than widening the deletion unasked. What a repository
  publishes is that owner's decision
- The concept-retirement sweep in `templates/core/quality.md` does not
  cover this. That rule chases surviving instructions to APPLY a retired
  concept and explicitly settles for historical records; a record is exactly
  what carries the content here

## Writing style

- Markdown wraps at the width the project declares in configuration,
  never at a width written into a rule. A document is not code and
  does not inherit the source line limit; it gets its own, and the
  project chooses the number
- Declare the width ONCE — in the Markdown linter's configuration or
  in `.editorconfig` under the Markdown section, not both. A second
  copy drifts from the first and nothing says which one won
- The exemptions travel with the declaration. Which of fenced blocks,
  table rows and headings are excused is part of the configured rule,
  not a convention each author infers
- Two exemptions are structural rather than configured, because the
  line cannot be wrapped at all and no configuration expresses that.
  The first is a bracketed single-line directive a parser reads whole,
  such as a template's dependency header. Wrapping it changes what it
  means, so the check skips it wherever the width came from. Write
  such a directive's name in prose rather than its bracket form -- a
  parser scanning for the form finds it in the sentence describing it,
  backticks and all
- The second is an unbreakable token: a bare URL, or a Markdown link an
  author does not break across lines. A line is exempt when such a token
  plus its indentation does not fit the width, since no wrapping
  shortens it. Measure the token, not the line with the token deleted:
  the second test excuses every long line that happens to carry a link.
  State the exemption in the check rather than leaving it a convention,
  or the rule grants an excuse the check reports anyway -- and a report
  whose one standing finding is the one everybody dismisses stops being
  read
- A project that declares no width has no rule, whatever its documents
  happen to look like. Near-total compliance kept by hand is the
  signature of an unwritten rule: it looks healthy and decays at the
  edges with nothing to notice
- Check — the command reads the configured width rather than assuming
  one, reports how many files it inspected, and prints nothing after
  that. A project with no width configured fails it, because an unstated
  width is the defect and not a gap to fill with a default. A count of
  zero is a failure too: the enumeration reads the index, so a document
  that is not staged yet is invisible to it. The exemption narrows the
  findings and never the corpus — every tracked file is still read, so a
  line held up only by an unbreakable token stops being reported while an
  over-long line of prose beside it does not:

  ```bash
  py - <<'EOF'
  import json, pathlib, re, subprocess

  # The width and its exemptions come from project configuration, never
  # from this check. A project that declares no width fails here, because
  # an unstated width is the defect, not a default to fill in.
  width, source = None, None
  skip_fenced, skip_tables, skip_headings = True, True, False
  cfg = pathlib.Path(".markdownlint.json")
  if cfg.exists():
      rule = json.loads(cfg.read_text(encoding="utf-8")).get("MD013")
      if isinstance(rule, dict):
          width = rule.get("line_length")
          skip_fenced = not rule.get("code_blocks", True)
          skip_tables = not rule.get("tables", True)
          skip_headings = not rule.get("headings", True)
          source = str(cfg)
  if width is None:
      ec = pathlib.Path(".editorconfig")
      if ec.exists():
          section = None
          for line in ec.read_text(encoding="utf-8").splitlines():
              line = line.strip()
              if line.startswith("[") and line.endswith("]"):
                  section = line[1:-1]
              elif section and "md" in section and line.startswith("max_line_length"):
                  width = int(line.split("=")[1].strip())
                  source = str(ec)
  # An unstated width is the defect this reports, not a gap to fill with a
  # default, so it leaves on a failing status rather than a message.
  if width is None:
      print("no Markdown line width is configured; declare one")
      raise SystemExit(1)

  def is_directive(text):
      """A single-line directive a parser reads whole, such as [ID: x]."""
      text = text.strip()
      return (text.startswith("[") and text.endswith("]")
              and ":" in text.split("]")[0])

  # The two tokens no wrapping shortens: a Markdown link, which an author
  # does not break across lines, and a bare URL.
  UNBREAKABLE = re.compile(r"!?\[[^\]]*\]\([^)\s]+\)|<?https?://[^\s>)]+>?")

  def is_unwrappable(text, limit):
      """True where no wrapping brings the line under the limit.

      Measure the longest unbreakable token against the width, not the line
      with its tokens removed. The second test excuses any long line that
      merely contains a link, because deleting the link makes the rest fit;
      the first excuses only a line whose overflow survives every wrap.
      """
      indent = len(text) - len(text.lstrip())
      longest = max((len(m.group()) for m in UNBREAKABLE.finditer(text)),
                    default=0)
      return indent + longest > limit

  tracked = subprocess.run(["git", "ls-files", "*.md"], capture_output=True,
                           text=True).stdout.split()
  # git ls-files reads the index, so a document not yet staged is invisible
  # here and the assertion passes having never seen it.
  print("markdown files inspected: %d" % len(tracked))

  findings = []
  if not tracked:
      findings.append("no tracked Markdown found; the enumeration is broken, "
                      "not the tree clean")

  for name in tracked:
      fenced = False
      for number, line in enumerate(
              pathlib.Path(name).read_text(encoding="utf-8").splitlines(), 1):
          if line.lstrip().startswith("```"):
              fenced = not fenced
              continue
          if fenced and skip_fenced:
              continue
          if skip_tables and line.lstrip().startswith("|"):
              continue
          if skip_headings and line.lstrip().startswith("#"):
              continue
          if is_directive(line):
              continue
          if len(line) > width and not is_unwrappable(line, width):
              findings.append("%s:%d %d > %d (%s)"
                              % (name, number, len(line), width, source))

  for finding in findings:
      print(finding)

  raise SystemExit(1 if findings else 0)
  EOF
  ```

- Write in present tense — past or future tense indicates out-of-sync
  documentation
- Write as little as necessary but as much as needed — documentation that goes
  out of sync is worse than no documentation
- Remove redundant, inconsistent, or outdated documentation promptly
- Use full, grammatically correct sentences — enumerations are exempt
- Use bold and italic sparingly — never bold inline code or a whole sentence,
  and use at most one short bold label per list item
- Code-format only identifiers (file names, paths, env vars); summarize whole
  commands and flags in prose rather than transcribing them as inline code
- Summarize intent and link to the source — do not transcribe methods,
  constants, or flags into prose
- The same holds for a self-documenting source. A hand-maintained table
  restating a CLI's `--help`, a generated schema, or generated API docs
  is a second copy that drifts the moment someone adds an option and
  forgets the table, leaving readers trusting a list that is quietly
  wrong. Point at the command or the generated artifact instead, and
  document only what it cannot state itself — why an option exists,
  which combinations are meaningful
- A figure a document states about the tree MUST come from a generator,
  or the document MUST NOT state it. A count, a ratio or a file total
  written into a sentence is right on the day it is typed and wrong the
  next time the tree moves, and nothing says so. Where the number carries
  the point, emit it into a generated block the sync command rewrites and
  its `--check` gates; where it does not, name the thing without counting
  it. A figure is a numeral and the thing it counts, spelled or in digits
  and with or without a modifier between them — `Eight files`, `14
  manifest-reading checks` and `7 top-level directories` are one form, and
  a detector reading a digit against a bare noun finds none of them.
  Check — no documentation figure sits outside a generated block.
  Pass condition: the command reports the documents it scanned and the
  ungated figures it found, the first non-zero and the second zero, and
  exits zero; any figure it lists reaches a non-zero status. A
  table restating a generator is covered by the rule above, and a fenced
  block is a transcript, so both are out of scope here.

  The corpus is every tracked Markdown document: a document stating a
  figure about the tree is one wherever it sits, and a path list drawn
  around the documents someone thought of leaves the rest unchecked. What
  the check excludes it excludes by kind. A **dated record** states what
  was true on its date; a document whose whole purpose is that is named as
  a path, and a live document carrying such a passage marks it with a
  comment naming the date, which is what makes the figure a record rather
  than an exemption. A file whose numerals are the project's **source
  material** — a rule stating a threshold, a fixture, anything generated
  from one — states a specification and not a measurement; name those
  roots, and a project whose Markdown is all documentation leaves the list
  empty:

  ```bash
  py - <<'EOF'
  import pathlib, re, subprocess
  NOUNS = ("file", "files", "template", "templates", "stack", "stacks",
           "chain", "chains", "check", "checks", "test", "tests", "root",
           "roots", "directory", "directories", "document", "documents",
           "section", "sections", "example", "examples")

  # Prose style favours a spelled numeral under ten, which is where most
  # counts fall. Below five it is an ordinary quantifier -- "two templates",
  # "four sections" -- and states no measurement, so the list starts at five.
  WORDS = ("five", "six", "seven", "eight", "nine", "ten", "eleven",
           "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
           "seventeen", "eighteen", "nineteen", "twenty", "dozen")

  # A modifier may sit between the numeral and its noun: "14
  # manifest-reading checks", "75 Markdown template files". A function word
  # or a unit may not -- "a 15 KB document" measures a size, not a
  # population, and "5 means tests" is two clauses.
  STOP = ("of|in|on|at|to|for|from|and|or|the|a|an|is|are|was|were|be"
          "|means|per|than|as|by|with|that|which|into|out|up|down|over"
          "|under|kb|mb|gb|kib|mib|byte|bytes|character|characters|word"
          "|words|line|lines|minute|minutes|second|seconds|token|tokens"
          "|page|pages")
  GAP = r"(?:\s+(?!(?:%s)\b)[\w-]+){0,2}" % STOP
  FIGURE = re.compile(r"(?<![\w.\-])(\d{1,6}|%s)%s\s+(%s)\b"
                      % ("|".join(WORDS), GAP, "|".join(NOUNS)), re.I)
  GENERATED = re.compile(r"<!--\s*/?generated:")

  # A passage stating the date it was measured on: a record of a tree, not
  # a claim about this one.
  MEASURED = re.compile(r"<!--\s*measured:\s*\d{4}-\d{2}-\d{2}")
  MEASURED_END = re.compile(r"<!--\s*/measured\s*-->")
  FENCE = re.compile(r"^\s*```")
  # A dated record states what was true on its date.
  HISTORY = ("CHANGELOG.md", "docs/dev-journal.md", "docs/decisions/",
             "docs/audits/")

  # Roots whose numerals are the project's own subject matter. Set per
  # project; leave empty where all Markdown is documentation.
  SOURCES = ("templates/", "generated/", "examples/")

  out = subprocess.check_output(["git", "ls-files", "-z", "*.md"])
  paths = [p for p in out.decode("utf-8").split(chr(0))
           if p.endswith(".md") and not p.startswith(HISTORY)
           and not p.startswith(SOURCES)]

  # A corpus the command did not produce is not a corpus. An empty list here
  # means the pathspec reached nothing, which reports zero findings from a
  # scan that never ran.
  if not paths:
      raise SystemExit("no tracked Markdown reached; the pathspec drifted")
  findings = []
  for rel in sorted(paths):
      generated = fenced = measured = False
      lines = pathlib.Path(rel).read_text(encoding="utf-8").splitlines()
      for number, line in enumerate(lines, 1):
          if FENCE.match(line):
              fenced = not fenced
              continue
          if GENERATED.search(line):
              generated = not generated
              continue

          # Matched separately: a toggle cannot tell which end it met, so
          # an unterminated record would exempt the rest of the file.
          if MEASURED.search(line):
              measured = True
              continue
          if MEASURED_END.search(line):
              measured = False
              continue
          if fenced or generated or measured or line.lstrip().startswith("|"):
              continue
          for hit in FIGURE.finditer(line):
              findings.append("%s:%d states '%s %s' outside a generated block"
                              % (rel, number, hit.group(1), hit.group(2)))
  print("documents scanned: %d" % len(paths))
  print("ungated figures: %d" % len(findings))
  for finding in findings:
      print(finding)

  # The counts are the reading; the status is the verdict.
  raise SystemExit(1 if findings else 0)
  EOF
  ```

## Writing for a reader who lacks the context
[ID: docs-cold-reader]

A ticket is read by whoever is deciding to pick the work up, a pull request
by whoever is deciding to approve it, and a defect record by whoever meets
the defect again. None of them has the code in their head, and a ticket can
sit for months before anyone does. The author is in the one state of
knowledge the reader will never share: they have just finished the
investigation. The per-type body formats fix what sections a ticket has;
this fixes the writing inside them.

- State the symptom before the mechanism. What a reader would observe comes
  first, why it happens second. An opening that starts inside the mechanism
  asks the reader to hold it before they know what it explains
- Expand a term taken from the code the first time it appears, or avoid it.
  A symbol name is exact and means nothing to somebody who has not opened
  the file
- Show the example rather than describing it. Real values a reader can
  compare beat a sentence about what would happen to them
- One idea per sentence. A reader who has to go back and re-read has found
  a defect in the sentence, not in themselves
- Separate how bad it is now from how bad it becomes. A latent defect and a
  live one want different words, and a description merging them either
  overstates today or conceals tomorrow
- An agent needs this written down more than a person does. A person
  re-reads a ticket once and notices the density; an agent does not, and
  files a body that is correct, complete, conformant and opaque. A rule
  governing what an agent says in a session stops at the session, and the
  ticket is the artifact that outlives it

The same fact, written both ways:

```text
Two packets that serialize to identical bytes are NOT reachable as unequal
without an assignment -- the generic and concrete PDUs use different formats
and so produce different bytes for the same values.
```

```text
You have to change a value after creating the packet to run into this.
Nothing in the library does that yet, so no current behaviour is wrong.
```

The first needs two passes and a double negative unpacked, opens with the
mechanism, and names two types without saying what they are. Both are
accurate, and only one of them answers the question its reader arrived with.

This is judgement and stays declarative: a rule that is not mechanically
checkable gets no check invented for it. A sentence-length gate passes prose
nobody can follow and fails a long sentence that reads cleanly, so the
enforcement is review rather than a gate.

## Diagrams and assets

- Prefer text-based diagram formats: Mermaid for flowcharts, sequence diagrams,
  and Gantt charts; Draw.io for complex visual diagrams
- Commit all raw editable sources alongside rendered outputs
- An artefact committed as a hand-editable source has exactly one
  authority. Where a generator produced it, the generator is scaffolding
  and is NOT committed — otherwise the tree holds two authorities for one
  artefact, whoever opens the editor and moves a box has their work
  silently reverted by the next run, and nothing in the tree says which
  of the two is current
- Committing the generator instead is equally coherent, but then the
  artefact is build output and MUST NOT be described or edited as a
  source. Either choice is fine; having both in the tree is the defect
- Do not use proprietary formats (Word, Illustrator, Affinity Designer)
- Diagrams MUST be version-controlled — binary-only diagrams are not acceptable
- Use uniform node shapes; split a diagram that serves two purposes (e.g.
  happy path vs error path, or build vs runtime)
- In Mermaid notes, avoid `;` (a statement separator) and a bare `<` (opens a
  tag inside `<br/>` notes) — both silently break rendering

## Docs-as-code

- Technical documentation lives in the repository alongside the code
- Documentation follows the same review process as code
- All documentation MUST be written in Markdown

## Citing the software (if applicable)

Where the project expects to be cited, the citation of record MUST be a
persistent identifier, not a URL. A repository URL or project domain can
move, lapse, or be rebranded, and rots every citation pointing at it; a
persistent identifier resolves to an archived, immutable snapshot and is
independent of any website, so the domain stays freely swappable.

- SHOULD archive each release and mint a persistent identifier, then
  cite the identifier that resolves to the latest version rather than a
  per-version one
- SHOULD ship a machine-readable citation file at the repository root so
  the forge renders a "cite this repository" affordance, and record the
  identifier in it
- A project domain or vanity URL is a convenience for readers and MUST
  NOT be presented as the citation of record

## Generated files

Files committed to the repository but produced by a tool (rendered
docs, generated configs, resolved template chains, code-from-schema
output) rot in four predictable ways: maintainers hand-edit them,
the source changes but the committed output is not refreshed, a
formatter touches the file at commit time and a later check flags
it as stale, or the output is produced with a different invocation
than the documented one.

- The fourth mode is the one that defeats review. The file is not
  stale, not hand-edited and not reformatted — it is simply generated
  differently, and for a visual or binary output the property that
  differs is usually not one the artifact displays. An export committed
  at half the documented scale renders every arrow correctly, and the
  smaller file reads in the diffstat as a compression win, so every
  signal available to a reviewer points the wrong way. The staleness
  gate MUST re-render rather than rely on inspection
- Committed diagram exports are the common instance. A rendered `.png`
  beside its editable source is a generated file by the definition
  above, but it reads as an asset, so a project can apply `--check`
  faithfully to its config and schema output and never think to point
  it at `docs/assets/`
- Every generated file SHOULD start with a banner identifying the
  tool that produced it and the command to refresh it. Example:

  ```markdown
  <!-- Generated by `python3 tools/generator.py`. Edit the source
       (path/to/source.yaml) or the renderer, not this file. Run
       `python3 tools/generator.py --check` to verify the committed
       file is up to date. -->
  ```

- Every generator SHOULD expose a `--check` flag that re-renders
  in memory and exits non-zero on diff or missing file. This is
  the CI-staleness gate; wire it into pre-commit and CI as a
  required check
- Formatters (Prettier, Black, gofmt, etc.) SHOULD ignore generated
  paths — otherwise the formatter reformats the file at commit time
  and `--check` then reports a confusing stale-file failure on the
  next run
- When a generated file's inputs change (a rename, move, or schema
  bump), re-run the generator rather than string-editing the artifact
  — the banner's "do not edit" header is a contract, and the next
  `--check` run flags a hand-edited file as stale against freshly
  generated content
- The `--check` rule applies whether the script renders one file or
  rewrites many entries inside one source-of-truth file. A bulk-emit
  script that mutates multiple slugs / entries / records in a single
  file MUST support `--check` and be wired into CI as a required gate
  — otherwise extractor drift accumulates silently and surfaces as a
  multi-hundred-line diff during an unrelated, narrow PR
- A bulk-emit `--check` failure MUST report the count of stale entries,
  not just the file path. "19 of 19 entries stale" tells the maintainer
  the extractor itself drifted; a bare filename reads like a one-line
  edit and hides the scale
- A generator that renders per-field output (report columns, table
  sections, config stanzas) MUST derive the field enumeration from the
  data schema it renders, never from a hardcoded list. A fixed list
  fails both ways at once: it renders dead columns for fields the data
  lacks, and silently omits fields it has — and the omission hides
  exactly the records the artifact exists to surface. The dead columns
  are the visible tell; treat them as a defect, not cosmetics
- A round-trip generated file — one the generator scaffolds and then
  refreshes in place while preserving human-owned edits (annotation
  files, mark-up review tables, scaffolded configs with user sections)
  — MUST on refresh either preserve human-entered content or fail loud
  naming what it would discard. Silently reverting an edit that does not
  match the preservation convention (an unmarked cell) is data loss even
  when documented. Two compliant behaviours: treat divergent unmarked
  content as a correction to keep, or refuse the refresh naming the cell

## Output file by agent

| Agent            | Context file                      |
| ---------------- | --------------------------------- |
| Claude Code      | `CLAUDE.md`                       |
| Cursor           | `.cursor/rules/project.mdc`       |
| GitHub Copilot   | `.github/copilot-instructions.md` |
| OpenAI Codex CLI | `AGENTS.md`                       |
| Generic / other  | `AGENTS.md`                       |
