"""Fenced blocks in Markdown, read the way a renderer reads them."""

import re

# A CommonMark fence: three or more backticks or tildes. A backtick fence's
# info string may hold no backtick, or the line is inline code instead.
OPENING = re.compile(r"^([ ]*)(`{3,}(?=[^`]*$)|~{3,})(.*)$")


def spans(lines):
    """Yield (opening index, closing index, indent, language) per block.

    A block left open runs to the end of the document, as a renderer reads
    it, and its closing index is the line count. The language is the info
    string's first word, empty when it has none.
    """
    n = 0
    while n < len(lines):
        opened = OPENING.match(lines[n])
        if not opened:
            n += 1
            continue
        indent, fence = len(opened.group(1)), opened.group(2)
        words = opened.group(3).split()

        # Only a run of the opening character at least as long, with
        # nothing after it, closes the block, so a shorter fence inside a
        # longer one is part of its body.
        closing = re.compile(
            r"^[ ]*%s{%d,}[ \t]*$" % (re.escape(fence[0]), len(fence)))
        end = n + 1
        while end < len(lines) and not closing.match(lines[end]):
            end += 1
        yield n, end, indent, words[0] if words else ""
        n = end + 1


def blocks(lines):
    """Yield (first body line number, language, body lines) per block.

    A fence indented under a list item has that indent stripped by a
    renderer, so it is stripped from the body here too.
    """
    for opening, closing, indent, language in spans(lines):
        body = [line[indent:] if not line[:indent].strip() else line
                for line in lines[opening + 1:closing]]
        yield opening + 2, language, body
