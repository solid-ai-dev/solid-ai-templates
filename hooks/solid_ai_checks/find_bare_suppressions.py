"""Find a lint suppression that names no rule.

A bare suppression absorbs every rule that later applies to its line; a
named one keeps failing on the next.
"""

import argparse
import re
import tokenize

from .support.files import read_lines, tracked

# One ESLint pattern covers the whole-file, same-line and next-line forms.
# The first lookahead refuses a longer directive name, so the short form
# cannot match the front of a long one and read the long one's rule as
# missing.
SUPPRESSIONS = (
    ("noqa", re.compile(r"noqa(?![:])")),
    ("nosec", re.compile(r"nosec(?![:]|[ ][A-Z][0-9])")),
    ("nolint", re.compile(r"nolint(?![:])")),
    ("eslint-disable",
     re.compile(r"eslint-disable(?:-next-line|-line)?(?![-\w])"
                r"(?![ \t]*[a-zA-Z@])")),
)

HASH = (".py", ".sh", ".rb", ".yml", ".yaml")
SLASH = (".js", ".ts", ".go", ".jsx", ".tsx")


def python_comments(path):
    """(row, text) for each comment the Python tokenizer finds.

    A `#` inside a string is part of the string's token, so a quoted
    directive is never read as one.
    """
    with tokenize.open(path) as handle:
        src = handle.readlines()
    tokens = tokenize.generate_tokens(iter(src).__next__)
    return src, [(t.start[0], t.string[1:]) for t in tokens
                 if t.type == tokenize.COMMENT]


def hash_comments(path):
    """(row, text) after the first `#` on each line, for the shell family."""
    src = read_lines(path)
    return src, [(n, line.split("#", 1)[1])
                 for n, line in enumerate(src, 1) if "#" in line]


def slash_comments(path):
    """(row, text) of each comment on each line, for the slash family.

    Every comment boundary on a line is followed, so a block comment that
    closes and is followed by another on the same line is read, and one
    left open carries on into the lines below until `*/`. Each comment is
    yielded alone, so the words of the next one never name a rule for it.
    Reading lines, not tokens, over-reports a directive quoted in a string
    rather than hide a real one: telling a regular expression from a
    division, or a template's `${...}` from its text, takes a parser.
    """
    src = read_lines(path)
    found, in_block = [], False
    for number, line in enumerate(src, 1):
        at = 0
        while at < len(line):
            if in_block:
                end = line.find("*/", at)
                if end < 0:
                    found.append((number, line[at:]))
                    break
                found.append((number, line[at:end]))
                at, in_block = end + 2, False
                continue
            opened = [k for k in (line.find("//", at), line.find("/*", at))
                      if k >= 0]
            if not opened:
                break
            at = min(opened)

            # A line comment runs to the end of the line; a block comment
            # opens here and is read by the branch above.
            if line.startswith("//", at):
                found.append((number, line[at + 2:]))
                break
            at, in_block = at + 2, True
    return src, found


def comments(path):
    """The source lines of `path` and every comment in it, by language."""
    if path.endswith(SLASH):
        return slash_comments(path)
    if path.endswith(".py"):
        try:
            return python_comments(path)

        # Source the tokenizer cannot finish is still scanned, line by
        # line, so a broken file over-reports rather than hides a finding.
        except (tokenize.TokenError, SyntaxError):
            pass
    return hash_comments(path)


def main(argv, report):
    parser = argparse.ArgumentParser(prog="find-bare-suppressions")
    parser.add_argument("--root", action="append", default=[],
                        help="directory to scan; repeatable")
    args = parser.parse_args(argv)

    files = report.count("files scanned", tracked(HASH + SLASH, args.root))
    total = 0
    for path in files:
        # Only a comment can hold a directive; reading code too would match
        # a quoted one, such as this module's own pattern table.
        src, found = comments(path)
        for number, comment in found:
            for name, pattern in SUPPRESSIONS:
                if name in comment:
                    total += 1
                    if pattern.search(comment):
                        report.finding(path, number, "BARE",
                                       src[number - 1].strip())

    report.count("suppressions found", total)
    report.count("bare (naming no rule)", report.findings)

    # Zero files means the suffix list misses the project's languages.
    return report.finish(bool(report.findings) or not files)
