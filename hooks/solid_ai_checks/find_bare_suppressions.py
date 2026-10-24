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

# The quotes that open a string literal in each slash language. Go's
# backtick string is raw, so a backslash inside it escapes nothing.
QUOTES = {".go": {'"': True, "'": True, "`": False}}
JS_QUOTES = {'"': True, "'": True, "`": True}

# A `/` opens a JavaScript regular expression where an expression can
# start: after an operator, an opening bracket or one of these keywords,
# or at the start of the file. After a name, a number, a closing bracket
# or a postfix `++`/`--` it divides.
REGEX_AFTER = set("(,=:[!&|?{};+-*%<>~^")
REGEX_KEYWORDS = {"return", "typeof", "case", "do", "else", "in", "of",
                  "new", "delete", "void", "throw", "yield", "await",
                  "instanceof"}


def before(text, j):
    """The index of the last non-blank character at or before `j`, or -1."""
    while j >= 0 and text[j] in " \t\r\n":
        j -= 1
    return j


def opens_regex(text, i):
    """Whether the `/` at `i` opens a regular expression literal."""
    j = before(text, i - 1)
    if j < 0:
        return True

    # A postfix operator ends an operand, so `a++ / b` divides.
    if text[j] in "+-" and j > 0 and text[j - 1] == text[j]:
        return False
    if text[j] in REGEX_AFTER:
        return True
    start = j
    while start > 0 and (text[start - 1].isalnum() or text[start - 1] in "_$"):
        start -= 1
    if text[start:j + 1] not in REGEX_KEYWORDS:
        return False

    # A keyword spelled as a property, as in `obj.return / b`, is a name.
    return text[before(text, start - 1)] != "." if start > 0 else True


def regex_end(text, i):
    """The index just past the regular expression opening at `i`.

    A `/` inside a character class does not close it, and neither does an
    escaped one; a literal left open ends at the line, as the parser's
    error would.
    """
    i, in_class = i + 1, False
    while i < len(text) and text[i] != "\n":
        char = text[i]
        if char == "\\":
            i += 1
        elif char == "[":
            in_class = True
        elif char == "]":
            in_class = False
        elif char == "/" and not in_class:
            i += 1
            break
        i += 1
    while i < len(text) and (text[i].isalnum() or text[i] == "_"):
        i += 1
    return i


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
    """(row, text) for each `//` and `/* */` comment outside a string.

    The scan skips string and template literals, and in JavaScript regular
    expression literals, so a directive quoted in code is not read as one.
    A block comment is reported on the row it opens.
    """
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    suffix = path[path.rfind("."):]
    quotes = QUOTES.get(suffix, JS_QUOTES)
    regexes = suffix != ".go"
    found = []
    row, counted, i, end = 1, 0, 0, len(text)
    while i < end:
        char = text[i]
        if char in quotes:
            i += 1
            while i < end and text[i] != char:
                if quotes[char] and text[i] == "\\":
                    i += 1

                # Only a template or raw string spans lines; any other
                # quote left open ends at the line, as the parser's error
                # would, instead of swallowing the comments below it.
                elif char != "`" and text[i] == "\n":
                    break
                i += 1
            i += 1
            continue

        # Skipped before its contents are read, since a quote inside a
        # pattern such as /"/ would otherwise open a string that swallows
        # the comment after it.
        if regexes and char == "/" and text[i + 1:i + 2] not in ("/", "*") \
                and opens_regex(text, i):
            i = regex_end(text, i)
            continue
        if text.startswith("//", i):
            stop = text.find("\n", i)
            closer = 0
        elif text.startswith("/*", i):
            stop = text.find("*/", i + 2)
            closer = 2
        else:
            i += 1
            continue
        stop = end if stop < 0 else stop
        row, counted = row + text.count("\n", counted, i), i
        found.append((row, text[i + 2:stop]))
        i = stop + closer
    return text.split("\n"), found


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
