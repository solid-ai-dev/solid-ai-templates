"""The files a hook reads: the tracked ones, never the working-tree walk."""

import os
import posixpath
import subprocess

# Vendored and installed code is not the project's own. Tracked copies of
# it still dominate any count they are left in.
VENDORED = ("node_modules", "vendor", "site-packages", ".venv", "venv",
            "build", "dist", ".tox")


class NotARepository(Exception):
    """Raised outside a git work tree, where nothing is tracked."""


class GitFailed(Exception):
    """Raised when git fails inside a work tree, so no listing is whole."""


def run_git(args):
    """Run git with its messages in English, returning the finished process.

    Under the C locale git does not translate its errors, so the one that
    means "no repository here" reads the same on every machine.
    """
    env = dict(os.environ, LC_ALL="C", LANGUAGE="C")
    try:
        return subprocess.run(["git"] + list(args), capture_output=True,
                              env=env)
    except OSError as error:
        raise GitFailed("cannot run git: %s" % error)


def ls_files(*args):
    """The paths `git ls-files -z` prints for `args`.

    Raises NotARepository outside a work tree and GitFailed when git fails
    inside one.
    """
    listing = run_git(["ls-files", "-z"] + list(args))
    if listing.returncode == 0:
        return [p for p in listing.stdout.decode("utf-8").split("\0") if p]

    # A malformed config, an unsafe owner or a corrupt index exits 128 just
    # as a missing repository does. Read as "does not apply", that failure
    # would pass a tree nobody scanned, so only git's own answer that this
    # is no work tree counts as one.
    probe = run_git(["rev-parse", "--is-inside-work-tree"])
    if probe.stdout.strip() == b"false" \
            or probe.stderr.startswith(b"fatal: not a git repository"):
        raise NotARepository("not inside a git work tree")
    reason = listing.stderr.decode("utf-8", "replace").strip()
    raise GitFailed("git ls-files exited %d: %s"
                    % (listing.returncode, reason.splitlines()[0]
                       if reason else "no message"))


def tracked(suffixes, roots=()):
    """Tracked paths ending in one of `suffixes`, under one of `roots`.

    Asking git keeps a scratch or ignored file out of the corpus, so a
    check reads the same tree on a laptop as in CI. An empty `roots`
    means the whole tree.
    """
    paths = ls_files()
    prefixes = normalised(roots)
    return sorted(
        p for p in paths
        if p.endswith(tuple(suffixes))
        and (not prefixes or p.startswith(prefixes))
        and not any(part in VENDORED for part in p.split("/")))


def normalised(roots):
    """Roots as the prefixes git prints; empty when one names the whole tree.

    git prints `docs/a.md`, so `./docs`, `docs/` and `docs\\` all have to
    become `docs/` before they can match it, and `.` means every path.
    """
    prefixes = []
    for root in roots:
        clean = posixpath.normpath(root.replace(chr(92), "/"))
        if clean in (".", ""):
            return ()
        prefixes.append(clean + "/")
    return tuple(prefixes)


def path_prefix(raw):
    """A path prefix spelled as git prints paths; empty for the whole tree.

    `./.github/workflows/` and `.github\\workflows\\` both become
    `.github/workflows/`. A trailing slash is kept, because `.env` names a
    file prefix and `migrations/` a directory, and the two match
    differently.
    """
    text = raw.strip().replace(chr(92), "/")
    clean = posixpath.normpath(text) if text else "."
    if clean == ".":
        return ""
    return clean + "/" if text.endswith("/") else clean


def read_lines(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().splitlines()
