"""List the lines of a fenced check that end in a line continuation.

A continuation lost in copying joins two lines and nothing reports it. This
locator cannot tell a lost one from a kept one; it lists where to look.
"""

import argparse

from .support.fences import blocks
from .support.files import read_lines, tracked

# A fenced workflow or a table of output is an example, where a line ending
# in a continuation is valid. Only a block a reader copies and runs counts.
CHECK_LANGUAGES = ("bash", "sh", "python", "py")

BACKSLASH = chr(92)


def main(argv, report):
    parser = argparse.ArgumentParser(prog="find-line-continuations")
    parser.add_argument("--root", action="append", default=[],
                        help="directory holding rule documents; repeatable")
    args = parser.parse_args(argv)

    files = report.count("markdown files scanned",
                         tracked([".md"], args.root))
    found = inspected = 0
    for path in files:
        for start, language, body in blocks(read_lines(path)):
            found += 1
            if language not in CHECK_LANGUAGES:
                continue
            inspected += 1
            for offset, line in enumerate(body):
                if line.rstrip().endswith(BACKSLASH):
                    report.finding(path, start + offset, "CONTINUATION",
                                   "line ends in a continuation")

    report.count("fenced blocks found", found)
    report.count("blocks in a check language", inspected)
    report.count("lines ending in a continuation", report.findings)
    if not files:
        return report.finish(True)
    if not inspected:
        return report.not_applicable(
            "no fenced block in a check language in %d file(s)" % len(files))

    # The continuation count is a reading, not a verdict: a person reads
    # each line against what was written.
    return report.finish(False)
