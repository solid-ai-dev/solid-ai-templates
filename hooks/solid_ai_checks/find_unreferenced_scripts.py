"""Find a maintained script nothing in the repository refers to.

An unshipped script sits outside packaging, coverage and often the lint
freeze, so no other gate reaches it. A script named outside the directory
is an entry point, and a script an entry point imports or names is reached
too. A name appearing anywhere counts, which under-reports on purpose:
every finding is a file nothing reaches.
"""

import argparse
import ast

from .support.files import normalised, tracked

SUFFIXES = (".py", ".sh", ".ts", ".js")


def read(path):
    """The file's text, or None when it cannot be opened."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as handle:
            return handle.read()
    except OSError:
        return None


def named(path, text):
    """Whether `text` names the file by its path or its file name."""
    return path in text or path.rsplit("/", 1)[-1] in text


def dotted(path):
    """The dotted name of a .py path; a package's is its __init__ module's."""
    parts = path[:-len(".py")].split("/")
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def imported(path, text, directory):
    """Yield every name, dotted from the tree's root, a script imports.

    A script run directly finds its own directory on the path, one run as
    a module finds the tree's root, and a project may put the scripts
    directory there, so an absolute import is tried against all three.
    """
    try:
        tree = ast.parse(text, path)
    except (SyntaxError, ValueError):
        return
    here = path.split("/")[:-1]
    roots = [here, directory, []]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            heads, names = roots, [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):

            # A relative import reaching above the tree's root fails when
            # it runs, so it reaches nothing.
            if node.level > len(here):
                continue
            heads = ([here[:len(here) - node.level + 1]] if node.level
                     else roots)
            base = [node.module] if node.module else []
            names = [".".join(base)] if base else []
            names += [".".join(base + [alias.name]) for alias in node.names
                      if alias.name != "*"]
        else:
            continue
        for head in heads:
            for name in names:
                yield ".".join(head + [name])


def reachable(scripts, entries, directory):
    """The entry points and every script they reach by import or by name."""
    modules = {dotted(p): p for p in scripts if p.endswith(".py")}
    seen, pending = set(entries), list(entries)
    while pending:
        path = pending.pop()
        text = read(path) or ""
        found = {p for p in scripts if p != path and named(p, text)}

        # Importing a.b.c runs a and a.b first, so each package on the way
        # is reached as well.
        if path.endswith(".py"):
            for name in imported(path, text, directory):
                parts = name.split(".")
                for n in range(1, len(parts) + 1):
                    if ".".join(parts[:n]) in modules:
                        found.add(modules[".".join(parts[:n])])
        pending.extend(found - seen)
        seen |= found
    return seen


def main(argv, report):
    parser = argparse.ArgumentParser(prog="find-unreferenced-scripts")
    parser.add_argument("--dir", default="scripts",
                        help="the directory of maintained scripts")
    args = parser.parse_args(argv)

    scripts = report.count("scripts inspected",
                           tracked(SUFFIXES, [args.dir]))
    if not scripts:
        return report.not_applicable("%s holds no script" % args.dir)

    inside = normalised([args.dir])
    corpus = []
    for path in tracked(("",)):
        if path.startswith(inside):
            continue
        text = read(path)
        if text is not None:
            corpus.append(text)
    report.count("files searched for a reference", corpus)
    blob = "\n".join(corpus)

    directory = inside[0].rstrip("/").split("/") if inside else []
    entries = [p for p in scripts if named(p, blob)]
    reached = reachable(scripts, entries, directory)
    for path in scripts:
        if path not in reached:
            report.finding(path, 0, "UNREFERENCED",
                           "nothing outside %s names it, and no script "
                           "reached from there imports or names it"
                           % args.dir)
    report.count("unreferenced", report.findings)

    # A searched count of zero means the corpus never loaded, which reads
    # the same as a directory where everything is referenced.
    return report.finish(bool(report.findings) or not corpus)
