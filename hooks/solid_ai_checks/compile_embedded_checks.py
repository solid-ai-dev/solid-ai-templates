"""Compile every Python check embedded in Markdown as a heredoc.

A check that does not compile when a reader extracts it looks enforced and
is not.
"""

import argparse

from .support.fences import blocks
from .support.files import read_lines, tracked

OPENER = "<<'EOF'"
NEWLINE = chr(10)


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
            text = NEWLINE.join(body)
            if OPENER not in text:
                continue
            found += 1
            source = text.split(OPENER, 1)[1].split(NEWLINE + "EOF", 1)[0]
            try:
                compile(source.lstrip(NEWLINE), path, "exec")
            except SyntaxError as error:
                report.finding(path, start + (error.lineno or 1), "COMPILE",
                               error.msg)

    report.count("embedded checks found", found)
    report.count("checks that do not compile", report.findings)
    if not files:
        return report.finish(True)
    if not found:
        return report.not_applicable(
            "no embedded check to compile in %d file(s)" % len(files))
    return report.finish(bool(report.findings))
