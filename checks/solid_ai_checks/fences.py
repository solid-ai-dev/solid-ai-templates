"""Fenced blocks in Markdown, read the way a renderer reads them."""

import re

FENCE = re.compile(r"^([ ]*)```(\w*)")


def blocks(lines):
    """Yield (first body line number, language, body lines) per block.

    A fence indented under a list item has that indent stripped by a
    renderer, so it is stripped from the body here too.
    """
    n = 0
    while n < len(lines):
        opened = FENCE.match(lines[n])
        if not opened:
            n += 1
            continue
        indent, language = len(opened.group(1)), opened.group(2)
        n += 1
        start, body = n + 1, []
        while n < len(lines) and not FENCE.match(lines[n]):
            line = lines[n]
            body.append(line[indent:] if not line[:indent].strip() else line)
            n += 1
        n += 1
        yield start, language, body
