# Rationale: embedded checks

Why the rules in `templates/core/embedded-checks.md` say what they say. The
template states each rule as one instruction; the reasoning is here, one
heading per section ID.

## embedded-checks-extraction

- **Indentation.** A renderer strips the fence's indentation from every line,
  so a block indented five spaces under a step turns a four-space nested line
  into a three-space one and stops compiling.
- **Escapes.** An inline `-c` string loses escapes to shell expansion. A
  lost escape inside a pattern leaves a check that parses, runs and matches
  the wrong set; a quoted heredoc keeps every escape as written.
- **Extraction.** A check is only proven in the form a reader copies, so it
  is extracted from the committed file, and a tool that skips checks it
  cannot read reports how many it skipped.

The continuation locator keeps two counts so its deliberate narrowing to check
languages stays visible: it once reported two valid continuations inside a
documented `run:` step for as long as it scanned every language.
