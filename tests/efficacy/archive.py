"""Archive a round's raw data, restore a working root from an archive, and
verify that the two read the same.

A run root and its scoring area live on the machine that ran the round, so a
report is only as checkable as that disk. This module copies what the report
reads, and what a later scoring or judging needs, into a directory kept in
the private repository `braboj/tariff-runs`. An archive is verified by
restoring it and reading the report's figures from both roots. Only a
verified archive stamps the scoring area, and the report refuses to write
under `docs/audits/` without a current stamp.
"""

import argparse
import datetime
import glob
import hashlib
import io
import json
import os
import shutil
import sys
import tarfile
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lib  # noqa: E402
from harness import (TrialError, assert_outside_repository,  # noqa: E402
                     project_folder, remove_tree, scoring_area, write_run)

MANIFEST = "ARCHIVE.json"
STAMP = "archived.json"

# The scoring area's per-trial readings the report aggregates, each a JSON
# file named for its trial.
READINGS = ("scores", "scores-change", "security-scores")

# What a frozen workspace holds that no reading needs and any scoring
# rebuilds: tool caches, compiled bytecode, and every virtual environment,
# found by its `pyvenv.cfg` whatever the agent named it.
CACHE_DIRS = frozenset(["__pycache__", ".pytest_cache", ".mypy_cache",
                        ".ruff_cache", ".hypothesis", ".tox", "node_modules",
                        "htmlcov"])
CACHE_FILES = frozenset([".coverage"])
CACHE_SUFFIXES = (".pyc", ".pyo")
VENV_MARKER = "pyvenv.cfg"

# GitHub rejects a file over 100 MB and warns from 50 MB, so an archive
# holding a larger one could not be pushed whole.
MAX_BYTES = 50 * 1024 * 1024

# A voided workspace is not archived; its directory's name is, because the
# report reads the loss from that name.
VOID_MARKER = "VOIDED"


def sha256(path):
    digest = hashlib.sha256()
    with io.open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path):
    with io.open(path, encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path, data, sort_keys=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2, sort_keys=sort_keys)


def venv_roots(names):
    """Every directory in a tarball's member names that holds a venv."""
    return {name.rsplit("/", 1)[0] for name in names
            if name.endswith("/" + VENV_MARKER)}


def stripped(name, venvs):
    """Whether a tarball member is left out of the archive."""
    parts = name.split("/")
    if any(part in CACHE_DIRS for part in parts):
        return True
    if parts[-1] in CACHE_FILES or parts[-1].endswith(CACHE_SUFFIXES):
        return True
    return any(name == venv or name.startswith(venv + "/") for venv in venvs)


def strip_tarball(source, target):
    """Copy a frozen tarball without what `stripped` leaves out; return what
    was removed."""
    with tarfile.open(source) as archive:
        members = archive.getmembers()
    venvs = venv_roots(member.name for member in members)
    removed, removed_bytes = 0, 0
    with tarfile.open(source) as archive, tarfile.open(target, "w") as out:
        for member in archive.getmembers():
            if stripped(member.name, venvs):
                removed += 1
                removed_bytes += member.size
                continue
            out.addfile(member, archive.extractfile(member)
                        if member.isfile() else None)
    return {"members_removed": removed, "bytes_removed": removed_bytes,
            "venvs": sorted(venvs)}


def readings_digest(root):
    """A hash of every file the report reads, keyed by its place."""
    area = scoring_area(root)
    files = {os.path.basename(path): path
             for path in glob.glob(os.path.join(root, "run-*.json"))}
    patterns = [os.path.join(kind, "*.json") for kind in READINGS]
    patterns += [os.path.join("judge", "T*.json"),
                 os.path.join("judge", "map.json")]
    for pattern in patterns:
        for path in glob.glob(os.path.join(area, pattern)):
            files[os.path.relpath(path, area).replace(os.sep, "/")] = path
    return {key: sha256(path) for key, path in sorted(files.items())}


def stamp_problem(root):
    """Why the round at `root` is not archived as it stands; None if it is."""
    path = os.path.join(scoring_area(root), STAMP)
    if not os.path.isfile(path):
        return ("the round has not been archived; run archive.py --root %s "
                "--into <a fresh directory in braboj/tariff-runs>" % root)
    held = load_json(path).get("readings", {})
    now = readings_digest(root)
    changed = sorted(key for key in set(held) | set(now)
                     if held.get(key) != now.get(key))
    if changed:
        return ("the round changed since it was archived (%d file(s): %s); "
                "archive it again into a fresh directory"
                % (len(changed), ", ".join(changed[:5])))
    return None


def refuse_unless_empty(path):
    if os.path.isdir(path) and os.listdir(path):
        raise TrialError("%s is not empty; an archive is written once, "
                         "into a fresh directory" % path)


def copy_file(source, target):
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(source, target)


def archive(root, into):
    """Copy the round at `root` into `into` and its scoring sibling; return
    the manifest written beside it."""
    root, into = os.path.abspath(root), os.path.abspath(into)
    area, into_area = scoring_area(root), scoring_area(into)
    runs = sorted(glob.glob(os.path.join(root, "run-*.json")))
    if not runs:
        raise TrialError("no run record in %s; nothing to archive" % root)
    assert_outside_repository(into)
    refuse_unless_empty(into)
    refuse_unless_empty(into_area)

    manifest = {"archived_at":
                datetime.datetime.now().isoformat(timespec="seconds"),
                "source": root, "tarballs": {}, "transcripts": {},
                "voided": []}
    templates, suites = set(), set()
    for run in runs:
        copy_file(run, os.path.join(into, os.path.basename(run)))
        for record in load_json(run).get("trials", []):
            if record.get("templates_tree"):
                templates.add(record["templates_tree"])

    os.makedirs(into, exist_ok=True)
    for tarball in sorted(glob.glob(os.path.join(root, "*.tar"))):
        name = os.path.basename(tarball)
        removed = strip_tarball(tarball, os.path.join(into, name))
        manifest["tarballs"][name] = dict(removed,
                                          original_sha256=sha256(tarball))

    # Only the sessions' transcripts leave the scratch home: the rest of it
    # holds the account's credentials. A transcript's time is kept apart,
    # because a clone does not keep it and the report reads it to tell a
    # re-run's sessions from the blocked attempt's in the same folder.
    projects = os.path.join(root, "home", ".claude", "projects")
    for folder, _, files in os.walk(projects):
        for file in files:
            source = os.path.join(folder, file)
            relative = os.path.relpath(source, root).replace(os.sep, "/")
            copy_file(source, os.path.join(into, relative))
            manifest["transcripts"][relative] = os.path.getmtime(source)

    voided = os.path.join(root, "void")
    for entry in sorted(os.listdir(voided) if os.path.isdir(voided) else []):
        marker = os.path.join(into, "void", entry, VOID_MARKER)
        os.makedirs(os.path.dirname(marker))
        with io.open(marker, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(os.path.join(voided, entry) + "\n")
        manifest["voided"].append(entry)

    for kind in READINGS:
        for path in sorted(glob.glob(os.path.join(area, kind, "*.json"))):
            copy_file(path, os.path.join(into_area, kind,
                                         os.path.basename(path)))
            suite = load_json(path).get("suite_revision")
            if suite:
                suites.add(suite)

    # A judging's bundle is rebuilt from its tree, so only the judgings, the
    # unblinding map and a failed judging's output tail are kept.
    for path in sorted(glob.glob(os.path.join(area, "judge", "*"))):
        if os.path.isfile(path):
            copy_file(path, os.path.join(into_area, "judge",
                                         os.path.basename(path)))
    lock = os.path.join(area, "tool-lock.txt")
    if os.path.isfile(lock):
        copy_file(lock, os.path.join(into_area, "tool-lock.txt"))

    manifest["templates_tree"] = sorted(templates)
    manifest["suite_revision"] = sorted(suites)
    manifest["files"] = {}
    oversize = []
    for base, label in ((into, "root"), (into_area, "scoring")):
        for folder, _, files in os.walk(base):
            for file in files:
                path = os.path.join(folder, file)
                key = "%s/%s" % (label, os.path.relpath(path, base)
                                 .replace(os.sep, "/"))
                size = os.path.getsize(path)
                manifest["files"][key] = {"sha256": sha256(path),
                                          "bytes": size}
                if size > MAX_BYTES:
                    oversize.append("%s (%d MB)" % (key, size >> 20))
    if oversize:
        remove_tree(into)
        remove_tree(into_area)
        raise TrialError("over the %d MB a pushed file may hold: %s"
                         % (MAX_BYTES >> 20, ", ".join(oversize)))
    dump_json(os.path.join(into, MANIFEST), manifest)
    return manifest


def moved(path, into, *parents):
    """`path`'s last component under `into`, below `parents`."""
    if not path:
        return path
    return os.path.join(into, *(parents + (os.path.basename(path),)))


def restore(source, into):
    """Make a working root at `into` from the archive at `source`."""
    source, into = os.path.abspath(source), os.path.abspath(into)
    manifest = load_json(os.path.join(source, MANIFEST))
    assert_outside_repository(into)
    refuse_unless_empty(into)
    refuse_unless_empty(scoring_area(into))
    shutil.copytree(source, into, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(MANIFEST))
    if os.path.isdir(scoring_area(source)):
        shutil.copytree(scoring_area(source), scoring_area(into),
                        dirs_exist_ok=True)
    for relative, mtime in manifest["transcripts"].items():
        os.utime(os.path.join(into, relative), (mtime, mtime))

    # The records name the root they ran in. The tarball and the voided
    # directory are read by path, so they are pointed at the restored copies;
    # the workspace is not, because the transcripts are filed under its name.
    for run in sorted(glob.glob(os.path.join(into, "run-*.json"))):
        data = load_json(run)
        for record in data.get("trials", []):
            void = record.get("void")
            if void:
                void["dir"] = moved(void.get("dir"), into, "void")
            frozen = record.get("frozen") or {}
            if frozen.get("tarball"):
                frozen["tarball"] = (
                    os.path.join(void["dir"], os.path.basename(
                        frozen["tarball"])) if void
                    else moved(frozen["tarball"], into))
            if record.get("substitutes"):
                record["substitutes"] = moved(record["substitutes"], into,
                                              "void")
        dump_json(run, data, sort_keys=False)
    return into


def figures(root, seed):
    """What the report computes from a root, with paths left out."""
    import report

    trials = report.load(root)
    report.exclude_reached(trials, report.reaches(root))
    table = report.collect(trials)
    results = report.contrasts(table, seed, report.crossed_labels(trials))
    withdrawn = report.withdrawals(trials)
    report.withdraw(withdrawn, table, results)
    return {"table": table, "results": results, "withdrawn": withdrawn,
            "escalation": report.assess_escalation(trials, results, seed,
                                                   withdrawn),
            "reach": report.reaches(root),
            "lost": [{key: value for key, value in loss.items()
                      if key != "kept"}
                     for loss in report.lost_trials(root)]}


def verify(root, source, seed):
    """The parts of the report that differ between `root` and the archive at
    `source`, restored; empty when they agree."""
    scratch = tempfile.mkdtemp(prefix="efficacy-verify-")
    try:
        restored = restore(source, os.path.join(scratch, "round"))
        ours, theirs = figures(root, seed), figures(restored, seed)
    finally:
        remove_tree(scratch)
    return sorted(part for part in ours
                  if json.dumps(ours[part], sort_keys=True, default=str)
                  != json.dumps(theirs[part], sort_keys=True, default=str))


def stamp(root, into):
    dump_json(os.path.join(scoring_area(root), STAMP),
              {"archive": os.path.abspath(into),
               "archived_at":
               datetime.datetime.now().isoformat(timespec="seconds"),
               "readings": readings_digest(root)})


def plant_tarball(path, name, extra=()):
    """A frozen workspace holding code, a venv, caches and a git dir."""
    entries = {"src/pkg/__init__.py": b"VALUE = 1\n",
               "src/pkg/__pycache__/__init__.cpython-313.pyc": b"\0" * 64,
               ".venv/pyvenv.cfg": b"home = x\n",
               ".venv/Lib/site-packages/big.py": b"x" * 4096,
               "env2/pyvenv.cfg": b"home = x\n",
               "env2/Lib/other.py": b"y" * 1024,
               ".pytest_cache/v/cache": b"{}",
               ".coverage": b"data",
               ".git/HEAD": b"ref: refs/heads/main\n",
               "tariff.db": b"sqlite"}
    entries.update(extra)
    with tarfile.open(path, "w") as archive:
        for member, data in sorted(entries.items()):
            info = tarfile.TarInfo("%s/%s" % (name, member))
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))


def plant_root(scratch):
    """A round with two build trials, one change trial, one voided attempt
    and its re-run, scored, judged, read for security and archived nowhere."""
    root = os.path.join(scratch, "round")
    area = scoring_area(root)
    started = datetime.datetime(2026, 10, 1, 12, 0, 0)
    records = []
    for arm, task in (("none", "build"), ("full", "build"),
                      ("none", "change")):
        name = "%s-1" % arm if task == "build" else "change-%s-1" % arm
        workspace = os.path.join(root, name)
        tarball = os.path.join(root, "%s.tar" % name)
        os.makedirs(root, exist_ok=True)
        plant_tarball(tarball, name)
        records.append({"arm": arm, "trial": 1, "task": task,
                        "outcome": "completed", "workspace": workspace,
                        "templates_tree": "abc123",
                        "started_at": started.isoformat(),
                        "frozen": {"head": "h", "tarball": tarball}})

    # The voided attempt ran in full-1's workspace before its re-run, so its
    # transcript sits in the same folder and is older than the re-run's start.
    void_dir = os.path.join(root, "void", "full-1-2026-10-01T11-00-00")
    os.makedirs(void_dir)
    records.insert(1, {"arm": "full", "trial": 1, "task": "build",
                       "outcome": "blocked", "reason": "planted",
                       "workspace": records[1]["workspace"],
                       "started_at": "2026-10-01T11:00:00",
                       "void": {"dir": void_dir},
                       "frozen": {"tarball": os.path.join(void_dir,
                                                          "full-1.tar")}})
    write_run(os.path.join(root, "run-planted.json"), started, records)
    for record in records:
        if record["outcome"] != "completed":
            continue
        folder = os.path.join(root, "home", ".claude", "projects",
                              project_folder(record["workspace"]))
        os.makedirs(folder, exist_ok=True)
        session = os.path.join(folder, "%s.jsonl" % record["task"])
        with io.open(session, "w", encoding="utf-8") as handle:
            handle.write("{}\n")
    blocked = os.path.join(root, "home", ".claude", "projects",
                           project_folder(records[2]["workspace"]),
                           "blocked.jsonl")
    with io.open(blocked, "w", encoding="utf-8") as handle:
        handle.write("{}\n")
    early = (started - datetime.timedelta(hours=1)).timestamp()
    os.utime(blocked, (early, early))
    with io.open(os.path.join(root, "home", ".claude", ".credentials.json"),
                 "w", encoding="utf-8") as handle:
        handle.write('{"token": "planted-secret"}')

    for name, arm in (("none-1", "none"), ("full-1", "full")):
        for kind in READINGS:
            dump_json(os.path.join(area, kind, "%s.json" % name),
                      {"name": name, "arm": arm, "trial": 1,
                       "suite_revision": "suite1"})
    dump_json(os.path.join(area, "judge", "T1.json"),
              {"trial": "none-1", "blind_id": "T1", "outcome": "judged",
               "answer": {"rubric": {}}})
    dump_json(os.path.join(area, "judge", "map.json"),
              {"seed": 1, "blind": {"none-1": "T1"}})
    os.makedirs(os.path.join(area, "judge", "T1"))
    with io.open(os.path.join(area, "judge", "T1", "bundle.txt"), "w",
                 encoding="utf-8") as handle:
        handle.write("bundle")
    with io.open(os.path.join(area, "tool-lock.txt"), "w",
                 encoding="utf-8") as handle:
        handle.write("ruler==1.0\n")
    return root, blocked


def self_test():
    """Prove an archive keeps what the report reads and only that, restores
    to a root that reads the same, and that each refusal fires."""
    import report

    scratch = os.path.join(tempfile.gettempdir(), "efficacy-archive-self-test")
    remove_tree(scratch)
    root, blocked = plant_root(scratch)
    into = os.path.join(scratch, "runs", "round")
    seed = report.parse_args([]).seed
    manifest = archive(root, into)

    with tarfile.open(os.path.join(into, "none-1.tar")) as kept:
        names = set(kept.getnames())
    files = manifest["files"]
    checks = [
        ("code, git and data stay in the stripped tarball",
         {"none-1/src/pkg/__init__.py", "none-1/.git/HEAD",
          "none-1/tariff.db"} <= names),
        ("venvs by pyvenv.cfg, caches and bytecode are stripped",
         not any(part in name for name in names
                 for part in (".venv", "env2", "__pycache__",
                              ".pytest_cache", ".coverage"))
         and manifest["tarballs"]["none-1.tar"]["venvs"]
         == ["none-1/.venv", "none-1/env2"]),
        ("the original tarball's hash is recorded",
         manifest["tarballs"]["none-1.tar"]["original_sha256"]
         == sha256(os.path.join(root, "none-1.tar"))),
        ("transcripts come, the scratch home's credentials do not",
         len(manifest["transcripts"]) == 4
         and not any("credentials" in key for key in files)),
        ("readings, judgings, map and lock come; bundles do not",
         {"scoring/scores/none-1.json", "scoring/security-scores/full-1.json",
          "scoring/scores-change/none-1.json", "scoring/judge/T1.json",
          "scoring/judge/map.json", "scoring/tool-lock.txt"} <= set(files)
         and not any("bundle" in key for key in files)),
        ("a voided directory is kept as a marker",
         manifest["voided"] == ["full-1-2026-10-01T11-00-00"]
         and os.path.isfile(os.path.join(into, "void", manifest["voided"][0],
                                         VOID_MARKER))),
        ("the revisions are recorded",
         manifest["templates_tree"] == ["abc123"]
         and manifest["suite_revision"] == ["suite1"]),
    ]

    restored = restore(into, os.path.join(scratch, "restored"))
    records = load_json(os.path.join(restored, "run-planted.json"))["trials"]
    relative = os.path.relpath(blocked, root).replace(os.sep, "/")
    checks += [
        ("a restored record points at the restored tarball and void",
         records[0]["frozen"]["tarball"]
         == os.path.join(restored, "none-1.tar")
         and records[1]["void"]["dir"]
         == os.path.join(restored, "void", "full-1-2026-10-01T11-00-00")
         and records[0]["workspace"] == os.path.join(root, "none-1")),
        ("a restored transcript keeps its time",
         abs(os.path.getmtime(os.path.join(restored, relative))
             - os.path.getmtime(blocked)) < 1),
        ("the restored root reads as the original does",
         verify(root, into, seed) == []),
    ]

    # The control: a reading changed in the archive must show in the verify,
    # or its clean result above proves nothing.
    changed = os.path.join(scoring_area(into), "security-scores",
                           "full-1.json")
    before = load_json(changed).get("security_probe_pass_rate")
    dump_json(changed, dict(load_json(changed),
                            security_probe_pass_rate={"value": 0.5}))
    landed = (before is None and load_json(changed)
              ["security_probe_pass_rate"] == {"value": 0.5})
    checks.append(("a reading changed in the archive fails the verify",
                   landed and verify(root, into, seed) != []))

    checks.append(("an unarchived round has a stamp problem",
                   stamp_problem(root) is not None))
    stamp(root, into)
    checks.append(("a stamped round has none", stamp_problem(root) is None))
    score = os.path.join(scoring_area(root), "scores", "none-1.json")
    dump_json(score, dict(load_json(score), planted=True))
    checks.append(("a reading changed after the stamp is a problem",
                   "scores/none-1.json" in (stamp_problem(root) or "")))
    out = os.path.join(scratch, "audits")
    checks.append(("the report refuses docs/audits/ without a current stamp",
                   report.main(["--root", root]) == 2))
    checks.append(("the report still writes elsewhere",
                   report.main(["--root", root, "--out-dir", out]) == 0
                   and bool(os.listdir(out))))

    for label, target in (("a non-empty target is refused", into),
                          ("a target inside this repository is refused",
                           os.path.join(lib.ROOT, "tmp", "archive-probe"))):
        try:
            archive(root, target)
            checks.append((label, False))
        except TrialError:
            checks.append((label, True))
    big = os.path.join(scratch, "big")
    os.makedirs(big)
    write_run(os.path.join(big, "run-big.json"),
              datetime.datetime(2026, 10, 1), [])
    plant_tarball(os.path.join(big, "none-1.tar"), "none-1",
                  {"src/blob.bin": b"\0" * (MAX_BYTES + 1)})
    try:
        archive(big, os.path.join(scratch, "runs", "big"))
        checks.append(("a file past the push limit is refused", False))
    except TrialError:
        checks.append(("a file past the push limit is refused",
                       not os.path.exists(os.path.join(scratch, "runs",
                                                       "big"))))

    for label, ok in checks:
        print("  %-58s %s" % (label, "ok" if ok else "FAILED"))
    remove_tree(scratch)
    passed = sum(1 for _, ok in checks if ok)
    lib.print_verdict(passed == len(checks),
                      "%d/%d self-test checks passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Archive a round, restore a root from an archive, or "
                    "verify one.")
    parser.add_argument("--root", help="the round's run root")
    parser.add_argument("--into",
                        help="a fresh directory: the archive to write, or "
                             "with --restore the root to make")
    parser.add_argument("--from", dest="source",
                        help="an archive, for --restore and --verify")
    parser.add_argument("--restore", action="store_true",
                        help="make a working root from --from at --into")
    parser.add_argument("--verify", action="store_true",
                        help="compare --root with the archive at --from")
    parser.add_argument("--seed", type=int, default=None,
                        help="the report's bootstrap seed; its default "
                             "unless given")
    parser.add_argument("--self-test", action="store_true",
                        help="plant a round, archive, restore and verify it")
    return parser.parse_args(argv)


def main(argv):
    options = parse_args(argv)
    if options.self_test:
        return self_test()
    try:
        if options.restore:
            if not (options.source and options.into):
                print("--restore takes --from and --into")
                return 2
            print("Restored: %s" % restore(options.source, options.into))
            lib.print_verdict(True, "1 root restored")
            return 0
        if not options.root:
            print("--root is required")
            return 2
        import report
        seed = (options.seed if options.seed is not None
                else report.parse_args([]).seed)
        source = options.source if options.verify else options.into
        if not source:
            print("--into (or --verify with --from) is required")
            return 2
        if not options.verify:
            manifest = archive(options.root, source)
            print("Archived %d file(s) to %s"
                  % (len(manifest["files"]), source))
        differing = verify(options.root, source, seed)
    except TrialError as error:
        print("refused: %s" % error)
        lib.print_verdict(False, "nothing archived")
        return 1
    if differing:
        print("the archive reads differently in: %s" % ", ".join(differing))
        lib.print_verdict(False, "archive not verified; no stamp written")
        return 1
    stamp(options.root, source)
    lib.print_verdict(True, "archive verified; %s stamped"
                      % os.path.join(scoring_area(options.root), STAMP))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
