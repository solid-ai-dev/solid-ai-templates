"""Fail on the two comment-layout violations a tokenizer can see.

A comment block with code directly above it and no blank line between, and
an aside to the right of code that is not a tool directive. Whether a
comment sits above the right item takes a person.
"""

import argparse
import tokenize

from .support.files import VENDORED, ls_files, normalised

DIRECTIVES = ("noqa", "nosec", "type:", "pragma:", "pylint:", "fmt:", "mypy:")

# A comment that is the first thing inside a block or bracket opens the
# first group rather than dividing two, so a line ending in one of these
# needs no blank line under it.
OPENERS = (":", "(", "[", "{")

# Tokens that are layout, not code: a line whose last code token is none
# of the rest holds no code that a comment below it could abut.
LAYOUT = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
          tokenize.DEDENT, tokenize.ENCODING, tokenize.ENDMARKER)


def candidates(roots):
    """Tracked Python plus the untracked files a commit could still add."""
    listed = ls_files("--cached", "--others", "--exclude-standard", "*.py")
    prefixes = normalised(roots)
    return sorted(set(
        p for p in listed
        if (not prefixes or p.startswith(prefixes))
        and not any(part in VENDORED for part in p.split("/"))))


def main(argv, report):
    parser = argparse.ArgumentParser(prog="check-comment-layout")
    parser.add_argument("--root", action="append", default=[],
                        help="directory to scan; repeatable")
    args = parser.parse_args(argv)

    files = report.count("python files checked", candidates(args.root))
    for path in files:
        # The rows tokenize reports index these lines, so both come from
        # one read: a split of its own would count a form feed as a line.
        with tokenize.open(path) as handle:
            src = handle.readlines()
        tokens = list(tokenize.generate_tokens(iter(src).__next__))

        # The last code token ending on each row. A `#` inside a string is
        # part of that string's token, so it can never pass for a comment.
        last_code = {}
        for tok in tokens:
            if tok.type not in LAYOUT:
                last_code[tok.end[0]] = tok.string
        for tok in tokens:
            if tok.type != tokenize.COMMENT:
                continue
            row, col = tok.start
            if src[row - 1][:col].strip():
                body = tok.string.lstrip("#").strip()
                if not body.startswith(DIRECTIVES):
                    report.finding(path, row, "ASIDE",
                                   "comment to the right of code")
            elif row > 1 and src[row - 2].strip() \
                    and row - 1 in last_code \
                    and last_code[row - 1] not in OPENERS:
                report.finding(path, row, "ABUTS",
                               "comment block with code directly above it")
    report.count("layout violations", report.findings)
    if not files:
        return report.not_applicable("no Python file to check")
    return report.finish(bool(report.findings))
