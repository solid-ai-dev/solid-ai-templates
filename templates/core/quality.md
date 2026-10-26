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
- Delete a path once evidence shows it unreachable or obsolete: no caller,
  or a retired input
- Treat a real-data probe that never reaches a path as a lead, not proof;
  a sample misses rare cases

## Architecture

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

- Keep cognitive complexity at or under 15 per function
- Nest at most three levels; use guard clauses and early returns
- Prefer a positive condition (`if is_enabled`) to a negated one
- Replace a boolean flag that selects behaviour with an enum or two named
  functions
- Name every magic number and magic string as a constant
- Size a tuned threshold, such as a latency alert, from its measured
  distribution (p95, p99, maximum legitimate); name the data source in
  the constant's docstring
- Take a limit a specification fixes, such as a protocol's maximum
  message size, from that specification and name it, never from an
  observed percentile

## Dependencies

- Keep the module graph acyclic; break a cycle with a third module or an
  interface, never with a divergent local copy
- Keep coupling shallow: a change inside one module MUST NOT require
  changes in unrelated modules
- Talk only to direct dependencies, and keep together what changes together
  (SHOULD)
- Reach a heavy, native or platform-limited dependency through one module
  that owns its import and names the install command when it is missing

### Optional dependencies

[LOAD: add-dependency]

- Where a dependency is optional, run one CI leg without it installed,
  importing the package (MUST)

### Import bans

[LOAD: add-check]

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
- Never break a public catch contract: a raise callers catch by a built-in
  type keeps that type
- Add an error type only where a caller could act differently
- Never let a caller-side input filter stand in for a precondition: widen
  the filter, or assert the precondition inside the function

## Deprecation and renames

[LOAD: deprecate]

- Deprecate a public symbol, naming its replacement, before a later change
  removes it
- Deprecate every part of one call site together, such as a method and its
  keyword arguments, or break the whole call; never alias the outer name
  alone
- Retire a concept by sweeping every surface that still instructs its use,
  tickets and plans included, until a search returns only historical
  records

## Module structure

- Keep a CLI a thin layer over a library that holds its logic
- Keep constants beside the functions that use them

## Library output

[ID: quality-library-output]

- Never write to the host's standard output or error from a library, and
  never configure logging beyond the library's own logger (MUST)
- Make the library's logger injectable, falling back to its module logger
- Check the silence in a fresh process; a test runner's handler hides the
  default

## Encoding and line endings

- Encode every committed text file in UTF-8, with LF line endings (MUST)
- Keep identifiers ASCII (MUST); comments, docstrings, strings and
  documentation carry no charset restriction

```bash
pre-commit run check-ascii-identifiers --all-files --verbose
```

Pass condition: the inspected count is above zero and
`non-ASCII identifiers` is zero. The hook reads Python; `not applicable`
means the project tracks none.

- Set a program's output encoding explicitly, and pin its line ending where
  another program reads the output
- Commit a `.gitattributes` with `* text=auto`, adding `eol=lf` for hard
  LF
- Mark a text path exempt from LF with `-text` in `.gitattributes`
- Check line endings on every tracked file, whatever its name, exempting a
  `-text` file; count a file Git files `i/-text` as binary only when it
  holds a NUL byte
- Let a linter format on save, and keep manual style rules to a minimum
  (SHOULD)

```bash
seen=0 exempt=0 binary=0 bad=()
while IFS= read -r -d '' rec; do
  info=${rec%%$'\t'*} path=${rec#*$'\t'} seen=$((seen + 1))
  case " ${info#*attr/} " in *" -text "*) exempt=$((exempt + 1)); continue ;; esac
  case $info in "i/ "* | i/lf* | i/none*) continue ;; esac
  nuls=$(git cat-file blob ":0:$path" | tr -dc '\000' | wc -c)
  [[ $info == i/-text* && $nuls -gt 0 ]] && binary=$((binary + 1)) && continue
  bad+=("$path")
done < <(git ls-files -z --eol)
printf 'files inspected: %d\nexempt by -text: %d\n' "$seen" "$exempt"
printf 'binary by content: %d\nfiles not filed i/lf: %d\n' "$binary" "${#bad[@]}"
for f in "${bad[@]}"; do echo "  $f"; done
[ "$seen" -gt 0 ] && [ "${#bad[@]}" -eq 0 ]
```

Pass condition: exit zero, given only when the inspected count is above
zero and the not-`i/lf` count is zero. An empty `i/none` file passes; a
stray carriage return, filed `i/-text` with no NUL byte, still fails.

## Comments

- Prefer code that needs no comment; comment only intent the code cannot
  express
- Re-verify a comment explaining why something is safe whenever the code
  is next read
- Never cite a ticket, PR or ADR number in a code comment, docstring or
  commented configuration; state the substance (MUST NOT)
- Name a source (author, year, method) where non-obvious or scientific
  logic needs one (MAY)

## Debug code

- Commit no debug output (`print()`, `console.log()`) and no hardcoded
  breakpoint
- Delete commented-out code
- Gate debug tooling behind a flag or environment variable, off by default

### Probe scripts

- Write a probe, a throwaway script that measures data or behaviour,
  rather than guess
- Delete a probe before the commit that uses its findings (MUST)
- Keep findings in source comments, decision records or docs, never in
  the probe

## Rejected mechanisms

[ID: quality-rejected-mechanism-sweep]

- Grep the codebase for a construct a comment records as not working,
  before moving on: `grep -rn '<the construct>' <source root>`
- Read every hit as a suspected instance of the same defect, not a style
  question

## New constraints

[ID: quality-constraint-corpus-sweep]
[LOAD: add-check]

- Run a new constraint (a rule, a check, a tightened bound, a narrowed
  exemption) against the existing corpus before it merges (MUST)

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

- Confirm a validation, scraping, migration or codemod tool is correct
  before acting on its output in bulk
- Treat a physically implausible output as a tool defect: fix it, re-run,
  then apply
- Cross-check an independent source before overwriting stored data with a
  source that looks wrong
- Never weaken the rule behind a check to make it green or quiet

## Enforcement

- Enforce these conventions through the gates: editor, pre-commit, CI
- Merge to `main` only with passing tests

### Generated output

[LOAD: regenerate]

- Make a generator emit output that passes the linters natively; a needed
  `lint --fix` is a generator bug (MUST)

## Completion

[ID: quality-completion]

Adding pagination, for example, ends with bounded results, their tests and
an updated contract. It does not end with a rewrite of the service layer.

- Finish a task when the requested behaviour works through the entry point
  its user or caller reaches, and the checks that prove it pass
- Report a check that could not run as not run, never as a pass
- Add an abstraction, infrastructure or a process step only when a stated
  requirement, a demonstrated defect or a material risk justifies it
- Report a problem found outside the task, or file it as its own task,
  rather than fixing it in the same change (SHOULD)
