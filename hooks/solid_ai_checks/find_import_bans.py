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


# A src layout keeps its packages one directory down, and code imports
# them by the name below it, never by a name starting with src.
SOURCE_ROOT = "src"


def importable_as(path):
    """Yield (module, package parts) for each name a tracked file goes by.

    The whole path is one name; under a src layout the part below the
    innermost src directory is another, listed first. A package's
    __init__ module is the package itself.
    """
    parts = path[:-len(".py")].split("/")
    package = parts[:-1]
    if parts[-1] == "__init__":
        parts = package
    if SOURCE_ROOT in package:
        below = len(package) - package[::-1].index(SOURCE_ROOT)
        if parts[below:]:
            yield ".".join(parts[below:]), package[below:]
    if parts:
        yield ".".join(parts), package


def imported(tree, package):
    """Yield (line, names) for every import statement in the tree.

    A relative import is resolved against `package`, the importing
    module's package. `from X import Y` names X and X.Y, since Y may be a
    submodule.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield node.lineno, [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = []
            if node.level:

                # A relative import reaching above the top-level package
                # fails when it runs, so it names no module to check.
                if node.level > len(package):
                    continue
                base = package[:len(package) - node.level + 1]
            base = ".".join(base + ([node.module] if node.module else []))
            yield node.lineno, [base] + ["%s.%s" % (base, alias.name)
                                         for alias in node.names
                                         if alias.name != "*"]


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
        with open(path, encoding="utf-8") as handle:
            tree = ast.parse(handle.read(), path)

        # One statement crossing one ban is one finding, whichever of the
        # file's names or the statement's names reached it first.
        flagged = set()
        for module, package in importable_as(path):
            for line, names in imported(tree, package):
                for importer, banned in bans:
                    name = next((n for n in names if crosses(n, banned)), None)
                    if (name and crosses(module, importer)
                            and (line, importer, banned) not in flagged):
                        flagged.add((line, importer, banned))
                        report.finding(path, line, "BANNED",
                                       "%s imports %s" % (module, name))
    report.count("import-ban violations", report.findings)
    return report.finish(bool(report.findings) or not files)
