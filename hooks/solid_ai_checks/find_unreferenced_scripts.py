"""Find a maintained script nothing in the repository refers to.

An unshipped script sits outside packaging, coverage and often the lint
freeze, so no other gate reaches it. A name appearing anywhere counts,
which under-reports on purpose: every finding is a file nothing mentions.
"""

import argparse

from .support.files import normalised, tracked

SUFFIXES = (".py", ".sh", ".ts", ".js")


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
        try:
            with open(path, encoding="utf-8", errors="ignore") as handle:
                corpus.append(handle.read())
        except OSError:
            pass
    report.count("files searched for a reference", corpus)
    blob = "\n".join(corpus)

    for path in scripts:
        if path not in blob and path.rsplit("/", 1)[-1] not in blob:
            report.finding(path, 0, "UNREFERENCED",
                           "no tracked file outside %s names it" % args.dir)
    report.count("unreferenced", report.findings)

    # A searched count of zero means the corpus never loaded, which reads
    # the same as a directory where everything is referenced.
    return report.finish(bool(report.findings) or not corpus)
