# Base — Embedded Checks

[ID: base-embedded-checks]
[DEPENDS ON: templates/core/quality-gates.md]

For documents that carry checks a reader copies out and runs: context
files, runbooks, rule templates.

## Extraction

[ID: embedded-checks-extraction]

- Never indent a fenced check deeper than its code's first indentation; put
  it flush and point to it from the step
- Prefer a quoted heredoc to an inline `-c` string
- Never write a heredoc opener in prose
- Confirm a line continuation survived into the committed file
- Fold a command onto one line, or bind its parts to shell variables,
  rather than continue it (SHOULD)
- Extract a check from the committed file and run it before merging its rule

## Checks

- Find every check stated outside a fence; the hook matches whole
  paragraphs, since prose wraps:

```bash
pre-commit run find-unfenced-checks --all-files --verbose
```

- Require paragraphs above zero and `checks stated outside a fence` zero
- Pass a `--root` for each directory of documents with checks; zero paragraphs
  means the roots named nothing
- Compile every embedded check as a reader extracts it (MUST):

```bash
pre-commit run compile-embedded-checks --all-files --verbose
```

- Require files and checks above zero and `checks that do not compile`
  zero; each later line names a failing check
- Read `not applicable` as no Python heredoc check in any Markdown file;
  the hook compiles no other language
- List each line where a continuation could be lost, and read it against
  the source; the hook cannot see one already lost:

```bash
pre-commit run find-line-continuations --all-files --verbose
```

- Read a non-zero continuation count as a list to review, not a failure
