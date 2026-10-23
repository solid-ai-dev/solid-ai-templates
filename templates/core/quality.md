# Base — Quality Attributes

[ID: base-quality]

How code is designed, kept clean, swept and checked.

## Principles

- Keep one authoritative representation of each piece of knowledge (DRY);
  the third copy is a bug
- Extract shared logic only where substantial logic repeats; a few similar
  lines inline are not duplication
- Choose the simplest solution a stated requirement justifies (KISS)
- Build what is needed now, never for a hypothetical requirement (YAGNI)
- Record beside every deferral the concrete condition that reopens it
- Record missing evidence as the finding of a spike that cannot clear its
  bar
- Never lower a spike's bar to ship an answer
- Delete a path once evidence shows it unreachable or obsolete: no caller,
  or a retired input
- Treat a real-data probe that never reaches a path as a lead, not proof;
  a sample misses rare cases

## Revisit triggers

[ID: quality-revisit-trigger]

- Reopen a deferral in the change whose step fires its trigger, as a
  superseding record or a ticket carrying the evidence (MUST)
- Search the records for triggers naming a piece of state before changing
  it
- Write triggers in one consistent, greppable form
- State what would detect each trigger: a scheduled check, a failing gate,
  or a person looking
- Re-verify a trigger against the system, not by re-reading its record,
  and state that check beside the condition

## Architecture

- Keep editable content in a data directory, never in source modules
- Compute derived counts and statistics from the data; never hardcode them
- Remove unused modules, assets and data files promptly

## Naming

- Name a function with a verb, a class or module with a noun, and a boolean
  with `is`, `has` or `can`
- Rename a name that needs a comment to explain it
- Name a function so a call site reads without its body
- Use a single-letter name only for a loop counter or an ecosystem
  convention such as `err` or `e`
- Abbreviate only what the domain abbreviates universally (`url`, `id`)
- Use the same name for the same concept in every module
- Name a public enum member, CLI flag or result discriminator for the
  capability it offers, never the library behind it: `Transport.HEADED`,
  not `Transport.PLAYWRIGHT` (MUST). A private symbol MAY name its library

## Complexity

- Keep cognitive complexity at or under 15 per function, enforced by the
  analyser the project's language tooling binds
- Nest at most three levels; use guard clauses and early returns
- Prefer a positive condition (`if is_enabled`) to a negated one
- Replace a boolean flag that selects behaviour with an enum or two named
  functions
- Replace a flag that selects how many rules apply with an operation
  returning findings, each naming its rule, plus a guard that raises when
  the findings are not empty

  ```
  validate(cfg, strict=False)                 which rules ran? none named
  errors = findings(cfg); require_none(errors)  each names its rule
  ```

- Name every magic number and magic string as a constant
- Size a numeric threshold from the measured distribution of its quantity
  (p95, p99, maximum legitimate), and name the data source in the
  constant's docstring

## Dependencies

- Keep the module graph acyclic; break a cycle with a third module or an
  interface, never with a divergent local copy
- Keep coupling shallow: a change inside one module MUST NOT require
  changes in unrelated modules
- Talk only to direct dependencies, and keep together what changes together
  (SHOULD)
- Reach a heavy, native or platform-limited dependency through one module
  that owns its import and names the install command when it is missing
- Run one CI leg without the optional dependency installed, importing the
  package (MUST)
- Declare a directional import ban where one part of the tree must not
  import another (MAY), and check every ban declared

```bash
pre-commit run find-import-bans --all-files --verbose
```

Pass condition: the bans-declared and modules-inspected counts are above
zero and `import-ban violations` is zero. Each ban is a
`--forbid IMPORTER:IMPORTED` argument; `not applicable` means none is
declared.

## Errors

- Validate input at boundaries and fail at once on invalid state
- Read a value from its source-of-truth field, and raise when the field is
  missing; never fall back to a value derived from a slug, name or hash
- Bound every wait on another thread, process or connection, report why it
  gave up, and check the worker's liveness as well as the deadline
- Derive every deliberate raise from one package base
- Derive each type also from the built-in its site raised before, where the
  language lets an error type have two bases
- Split an error type only where a caller could act differently
- Keep a test that walks every raise in the package and fails on one
  outside the hierarchy
- Never let a caller-side input filter stand in for a precondition: widen
  the filter, or assert the precondition inside the function

## Deprecation and renames

- Deprecate a public symbol, naming its replacement, before a later change
  removes it
- Deprecate every part of one call site together, such as a method and its
  keyword arguments, or break the whole call; never alias the outer name
  alone
- Keep a one-line shim under the old name when widening a return type, and
  remove it in a later change
- Retire a concept by sweeping every surface that still instructs its use,
  tickets and plans included, until a search returns only historical
  records

## Module structure

- Build an internal module ready for extraction where it is reused or an
  extraction is planned: inject host values as constructor parameters, and
  give it its own public API, README, tests and requirements (SHOULD)
- Keep a CLI a thin layer over a library that holds its logic
- Port a function to another language exactly: the same operation order,
  character classes and edge cases, citing the original
- Keep constants beside the functions that use them

## Variants

- Prefer a per-configuration flag with a safe default to a global
  auto-detect, unless inputs partition cleanly on a measurable signal

## Library output

[ID: quality-library-output]

- Never write to the host's standard output or error from a library, and
  never configure logging beyond the library's own logger (MUST)
- Make the library's logger injectable, falling back to its module logger
- Check the silence in a fresh process; a test runner's handler hides the
  default

## Encoding and line endings

- Encode every committed file in UTF-8, with LF line endings (MUST)
- Keep identifiers ASCII (MUST); comments, docstrings, strings and
  documentation carry no charset restriction

```bash
pre-commit run check-ascii-identifiers --all-files --verbose
```

Pass condition: the inspected count is above zero and
`non-ASCII identifiers` is zero. The hook reads Python; `not applicable`
means the project tracks none.

- Set a program's output encoding explicitly, and pin its line ending where
  another program reads the output. In Python, at the entry point:
  `sys.stdout.reconfigure(encoding="utf-8", newline="\n")`
- Commit an `.editorconfig` and a `.gitattributes` with `* text=auto`,
  adding `eol=lf` for hard LF
- Mark a text path exempt from LF with `-text` in `.gitattributes`
- Let a linter format on save, and keep manual style rules to a minimum
  (SHOULD)

```bash
git ls-files --eol | awk -F'\t' '
  $2 ~ /\.(md|py|ya?ml|json|txt|toml|cfg|ini|sh|sql|css|js|ts)$/ {
    seen++
    if ($1 !~ /^i\/lf/) { bad[++n] = $0 }
  }
  END {
    printf "text files inspected: %d\n", seen + 0
    printf "files not filed i/lf: %d\n", n + 0
    for (i = 1; i <= n; i++) print "  " bad[i]
    exit (seen == 0 || n > 0)
  }'
```

Pass condition: exit zero, given only when the inspected count is above
zero and the count of files not filed `i/lf` is zero. It matches "not
`i/lf`" so a file git filed as `i/-text` for a stray carriage return is
caught too.

- Refresh a checkout older than `.gitattributes` by rewriting its files or
  re-cloning; the index being right does not make the checkout right

```bash
eol() { git ls-files --eol | awk -F'\t' "$1"; }
total=$(eol '$1 ~ /^i\/lf/' | wc -l)
drifted=$(eol '$1 ~ /^i\/lf/ && $1 !~ /w\/lf/' | wc -l)
echo "text files tracked: $total"
echo "checked out against a different convention: $drifted"
eol '$1 ~ /^i\/lf/ && $1 !~ /w\/lf/ { print "  " $2 }'
if [ "$total" -eq 0 ]; then
  echo "no text file reached; the extension or index pattern drifted"
  exit 1
fi
[ "$drifted" -eq 0 ] || exit 1
```

Pass condition: the first count is above zero and the second is zero;
either failing exits non-zero.

## Comments

- Prefer code that needs no comment; comment only intent the code cannot
  express
- Re-verify a comment explaining why something is safe whenever the code
  is next read
- Never cite a ticket, PR or ADR number in a code comment, docstring or
  commented configuration; state the substance (MUST NOT)
- Name a source (author, year, method) where non-obvious or scientific
  logic needs one (MAY)
- Enforce the citation ban with a test that greps comments, docstrings and
  commented configuration for `#\d+` and `ADR\s*\d+`
- Audit the citations to an item when it closes without action or is
  superseded, and fix each one still pointing at it; a citation to
  completed work stands

```bash
rg -n "#<number>\b"
```

Pass condition: no line it prints still points at the dropped or
superseded item.

- Place a block comment directly above the item it documents: never to
  the right of code, tool directives excepted, and never separated from the
  item by a blank line (MUST)
- Separate comment-plus-item groups with one blank line; a comment opening
  a block or bracket needs none above it
- Wrap comment prose to the project's line-length limit, in commented
  configuration too

```bash
pre-commit run check-comment-layout --all-files --verbose
```

Pass condition: the files-checked count is above zero and
`layout violations` is zero. The hook reads Python, tracked and untracked
but never ignored; whether a comment sits above the right item takes a
person.

## Debug code

- Commit no debug output (`print()`, `console.log()`) and no hardcoded
  breakpoint
- Delete commented-out code
- Gate debug tooling behind a flag or environment variable, off by default

### Probe scripts

- Write a probe, a throwaway script that measures data or behaviour,
  rather than guess
- Name a probe as temporary (`probe_*.py`, `scratch_*.ts`), and delete it
  before the commit that uses its findings (MUST)
- Keep findings in source comments, decision records or docs, never in
  the probe
- Use a probe for one mechanical edit repeated across many identical call
  sites (MAY); review the diff, then delete the probe

### Scripts directory

- Keep a file under `scripts/` only while a documented command invokes it,
  CI runs it, or such a file imports it; delete it otherwise (MUST)
- Hold `scripts/` to the review and formatting rules of shipped source

```bash
pre-commit run find-unreferenced-scripts --all-files --verbose
```

Pass condition: the scripts-inspected and files-searched counts are above
zero and `unreferenced` is zero. `--dir` names the directory;
`not applicable` means it holds no script.

## Rejected mechanisms

[ID: quality-rejected-mechanism-sweep]

- Grep the codebase for a construct a comment records as not working,
  before moving on: `grep -rn '<the construct>' <source root>`
- Read every hit as a suspected instance of the same defect, not a style
  question

## New constraints

[ID: quality-constraint-corpus-sweep]

- Run a new constraint (a rule, a check, a tightened bound, a narrowed
  exemption) against the existing corpus before it merges (MUST)
- Record in that change where the sweep looked, how many items it
  inspected, how many violate, and what was done (MUST)
- Name what a partial sweep left out (MUST)
- State whether the violations were fixed or frozen; a freeze names each
  instance, gates new work and reports an instance that stops violating
- Record a constraint shipped without a check as such, with the instances
  already known

## Destructive operations

[ID: quality-destructive-ownership]

- Delete, truncate, overwrite or kill only what the operation can prove it
  created: process ancestry, a key scheme, a filename prefix, a marker file
  or an ownership tag; never a path, a configuration value or a file
  extension
- Find nothing where the proof is unavailable: no error, no prompt, no
  guess
- Validate the input as well: reject an empty configuration value, and
  match the key scheme
- Apply this to every reaper: a cache clean, an output-directory clear, a
  log rotation, a temp-file sweep

```
match on ".html"              wrong directory -> README.html deleted
match on "[0-9a-f]{16}.html"  wrong directory -> nothing matched
```

## Check trust

[ID: quality-cross-validation]

### Tools

- Confirm a validation, scraping, migration or codemod tool is correct
  before acting on its output in bulk
- Treat a physically implausible output as a tool defect: fix it, re-run,
  then apply
- Cross-check an independent source before overwriting stored data with a
  source that looks wrong

### Self-match

- Test a check whose scan can reach its own source: run it from a tree with
  and without that source; the inspected count rises and the findings stay
  identical
- Constrain the scan to where the pattern can legitimately appear, such as
  the comment half of a line, rather than excluding a path
- Name what an unavoidable exclusion excludes, and why (MUST)
- Constrain by the narrowest property separating a real occurrence from a
  quoted one

### Verdicts and readings

- Verify a measurement against an independent check before tuning a gate
  or budget threshold it disagrees with
- Refuse, as a finding and never as exit 3, when the command that should
  yield a comparison baseline yields none, and print the baseline on its
  own line (MUST)
- Reach an automatic verdict on every threshold a check declares; the
  judgement is what remains (MUST)
- Read that threshold from the check's pass condition, never from a sample
  of its output (MUST)
- Say which counts carry the verdict and which are for a reader, where a
  check carries both (MUST)
- Report what a check saw whatever its verdict (MUST)
- Carry a shipped check's verdict in its exit status, and prove the status
  separates a planted violation from a clean tree (MUST)
- Say beside a check whose verdict takes a person what that judgement is
- Never wire a governance signal as a build gate where the project's own
  rules oblige the change that trips it (MUST NOT)

  ```
  rule: each new fenced block adds an entry to the dispositions file
  gate: fail any change that edits a test file -> every conforming change fails
  ```

- Never weaken the rule behind a check to make it green or quiet

## Enforcement

- Enforce these conventions through the gates: editor, pre-commit, CI
- Make a generator emit output that passes the linters natively; a needed
  `lint --fix` is a generator bug (MUST)
- Merge to `main` only with passing tests
