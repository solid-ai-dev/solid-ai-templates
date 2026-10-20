"""Find a lint suppression that names no rule.

A bare suppression absorbs every rule that later applies to its line; a
named one keeps failing on the next.
"""

import argparse
import re

from .files import read_lines, tracked

SUPPRESSIONS = (
    ("noqa", re.compile(r"noqa(?![:])")),
    ("nosec", re.compile(r"nosec(?![:]|[ ][A-Z][0-9])")),
    ("nolint", re.compile(r"nolint(?![:])")),
    ("eslint-disable-next-line",
     re.compile(r"eslint-disable-next-line(?![ ]*[a-zA-Z@])")),
)

HASH = (".py", ".sh", ".rb", ".yml", ".yaml")
SLASH = (".js", ".ts", ".go", ".jsx", ".tsx")


def main(argv, report):
    parser = argparse.ArgumentParser(prog="find-bare-suppressions")
    parser.add_argument("--root", action="append", default=[],
                        help="directory to scan; repeatable")
    args = parser.parse_args(argv)

    files = report.count("files scanned", tracked(HASH + SLASH, args.root))
    total = 0
    for path in files:
        marker = "#" if path.endswith(HASH) else "//"
        for number, line in enumerate(read_lines(path), 1):
            # Only the comment half of a line can hold a directive; reading
            # the whole line matches this module's own pattern table.
            if marker not in line:
                continue
            comment = line.split(marker, 1)[1]
            for name, pattern in SUPPRESSIONS:
                if name in comment:
                    total += 1
                    if pattern.search(comment):
                        report.finding(path, number, "BARE", line.strip())

    report.count("suppressions found", total)
    report.count("bare (naming no rule)", report.findings)

    # Zero files means the suffix list misses the project's languages.
    return report.finish(bool(report.findings) or not files)
