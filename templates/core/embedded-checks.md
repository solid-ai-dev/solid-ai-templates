# Base — Embedded Checks

[ID: base-embedded-checks]
[DEPENDS ON: templates/core/quality-gates.md]

For a project whose own documents carry runnable checks: context files,
runbooks, rule templates. A reader copies such a check out of the Markdown
and runs it, so it has to survive the copy.

## Extraction

[ID: embedded-checks-extraction]

- Never indent a fenced check deeper than the first indentation of its
  code; put it flush and point to it from the step
- Prefer a quoted heredoc to an inline `-c` string, and never write the
  heredoc opener itself in prose
- Confirm that a line continuation survived into the committed file
- Fold a command onto one line, or bind its parts to shell variables,
  rather than continue it (SHOULD)
- Build an exact backslash in quoted text with `chr(92)` rather than
  transcribing it
- Write patterns without backslash escapes:

  | Instead of | Write |
  |------------|-------|
  | `\d` | `[0-9]` |
  | `\w` | `[A-Za-z0-9_]` |
  | `\b` at each end | `(?<![A-Za-z0-9])` and `(?![A-Za-z0-9])` |
  | a literal backslash | `chr(92)` |

Every embedded check MUST compile when extracted the way a reader extracts
it:

```bash
pre-commit run compile-embedded-checks --all-files --verbose
```

Pass condition: the files-scanned and checks-found counts are above zero
and `checks that do not compile` is zero; each line after the counts names
a check that does not compile. `not applicable` means no Markdown file
holds a heredoc check.

List the lines where a continuation could be lost. The hook cannot detect
one already lost, so read its list against the source:

```bash
pre-commit run find-line-continuations --all-files --verbose
```

Pass condition: it reports the files scanned, the fenced blocks, those in a
check language and the lines among them ending in a continuation, then
lists those lines. A non-zero continuation count is a list to read, not a
failure.
