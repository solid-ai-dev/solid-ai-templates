"""Compile every Python check embedded in Markdown as a heredoc.

A check that does not compile when a reader extracts it looks enforced and
is not.
"""

import argparse
import re

from .support.fences import blocks
from .support.files import read_lines, tracked

OPENER = "<<'EOF'"
NEWLINE = chr(10)

# A heredoc fed to a Python interpreter, on the line that opens it. Another
# heredoc in the same block, such as a file written with cat, is not Python.
INTERPRETER = re.compile(r"(^|[\s;|&(/])(py|python[0-9.]*)(\s|$)")


def heredocs(body):
    """Yield (opening offset, source) for every Python heredoc in a block.

    A block can hold several checks, and each one is compiled, so a valid
    first check cannot hide an invalid second. One left open runs to the
    end of the block.
    """
    n = 0
    while n < len(body):
        line = body[n]
        if OPENER not in line or not INTERPRETER.search(line):
            n += 1
            continue
        end = n + 1
        while end < len(body) and body[end].strip() != "EOF":
            end += 1
        yield n, NEWLINE.join(body[n + 1:end])
        n = end + 1


def main(argv, report):
    parser = argparse.ArgumentParser(prog="compile-embedded-checks")
    parser.add_argument("--root", action="append", default=[],
                        help="directory holding rule documents; repeatable")
    args = parser.parse_args(argv)

    files = report.count("markdown files scanned",
                         tracked([".md"], args.root))
    found = 0
    for path in files:
        for start, _, body in blocks(read_lines(path)):
            for offset, source in heredocs(body):
                found += 1
                try:
                    compile(source, path, "exec")
                except SyntaxError as error:
                    report.finding(path, start + offset + (error.lineno or 1),
                                   "COMPILE", error.msg)

    report.count("embedded checks found", found)
    report.count("checks that do not compile", report.findings)
    if not files:
        return report.finish(True)
    if not found:
        return report.not_applicable(
            "no embedded check to compile in %d file(s)" % len(files))
    return report.finish(bool(report.findings))
