"""Find a Python import that crosses a boundary the project declared closed.

A directional ban is distinct from the acyclic rule: two tiers that never
cycle can still cross a boundary, such as a domain layer importing an
adapter it is meant not to know.
"""

import argparse
import ast
import re

from .support.files import tracked

# A dotted module prefix: identifiers joined by single dots. A side that is
# not one can never match an import, so the ban it names checks nothing.
MODULE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*([.][A-Za-z_][A-Za-z0-9_]*)*$")


def imported(tree):
    """Every module name an import statement in the tree names."""
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def crosses(name, banned):
    return name == banned or name.startswith(banned + ".")


def main(argv, report):
    parser = argparse.ArgumentParser(prog="find-import-bans")
    parser.add_argument("--forbid", action="append", default=[],
                        metavar="IMPORTER:IMPORTED",
                        help="module prefix that must not import another; "
                             "repeatable")
    parser.add_argument("--root", action="append", default=[],
                        help="directory to scan; repeatable")
    args = parser.parse_args(argv)

    # A malformed ban dropped quietly leaves the boundary it meant to close
    # unchecked, so every supplied pair is validated and a bad one fails.
    bans = []
    for raw in args.forbid:
        parts = [p.strip() for p in raw.split(":")]
        if len(parts) != 2 or not all(MODULE.match(p) for p in parts):
            report.finding("--forbid", 0, "ARGUMENT",
                           "%r is not IMPORTER:IMPORTED, two dotted module "
                           "names" % raw)
            continue
        bans.append(tuple(parts))
    report.count("import bans declared", bans)
    if report.findings:
        return report.finish(True)
    if not bans:
        return report.not_applicable("no --forbid IMPORTER:IMPORTED declared")

    files = report.count("modules inspected", tracked([".py"], args.root))
    for path in files:
        module = path[:-len(".py")].replace("/", ".")
        with open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), path)
        for name in imported(tree):
            for importer, banned in bans:
                if crosses(module, importer) and crosses(name, banned):
                    report.finding(path, 0, "BANNED",
                                   "%s imports %s" % (module, name))
    report.count("import-ban violations", report.findings)
    return report.finish(bool(report.findings) or not files)
