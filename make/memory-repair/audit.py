#!/usr/bin/env python3
"""Health check for every native-memory store on this machine.

Run with no arguments. Answers three questions:

  1. Does each store's working directory still exist?   (orphan detection)
  2. Does every MEMORY.md link resolve to a real file?  (dangling links)
  3. Is every topic file listed in its index?           (invisible memories)

Exit code is 0 when clean, 1 when anything needs attention — so this can be
wired into a cron or a pre-move check.

Why the path resolution is not a simple string replace: the store directory
name encodes the absolute cwd with '/' replaced by '-'. That is lossy —
'mana-ventures' and 'mana/ventures' encode identically. So we walk the real
filesystem, trying every possible split, and report the deepest path that
exists. A store whose path cannot be fully resolved is an orphan.
"""
import os, sys, glob, re

ROOT = os.path.expanduser("~/.claude/projects")

# Files deliberately kept out of an index (reachable from a parent memory).
# Add to this rather than letting real omissions hide in the noise.
INTENTIONALLY_UNINDEXED = {
    "project-team-cli-agent-automations-vision.md",
    "project-team-cli-agent-idea.md",
    "project-team-cli-agent-philosophy.md",
    "project-team-cli-agent-substrate-shape.md",
    "project-team-cli-agent-v01-build-notes.md",
    "reference-notion-multi-workspace-safety.md",
}


def resolve(slug):
    """Walk the filesystem to turn an encoded slug back into a real path.

    Returns (full_path_or_None, deepest_existing_prefix, unresolved_remainder).
    """
    if slug == "-":                       # the filesystem root store
        return "/", "/", ""
    tokens = slug.split("-")
    if tokens and tokens[0] == "":
        tokens = tokens[1:]

    best = ["/", 0]                       # deepest prefix reached, tokens consumed

    def walk(base, i):
        if i > best[1]:
            best[0], best[1] = base, i
        if i >= len(tokens):
            return base
        for j in range(i + 1, len(tokens) + 1):
            span = tokens[i:j]
            if not "".join(span):
                continue
            # the CLI encodes both "/" and " " as "-" (probe-verified on
            # ~/Standard Works, 2026-08-06), so a multi-token span may be a
            # dashed name or a spaced name.
            # ponytail: mixed "-"/" " in one name would need per-gap choice — none exist yet
            for name in {"-".join(span), " ".join(span)}:
                cand = os.path.join(base, name)
                if os.path.isdir(cand):
                    got = walk(cand, j)
                    if got:
                        return got
            # a dot-directory encodes as an empty token before the name
            if span[0] == "" and j > i + 1:
                for sep in ("-", " "):
                    cand = os.path.join(base, "." + sep.join(tokens[i + 1:j]))
                    if os.path.isdir(cand):
                        got = walk(cand, j)
                        if got:
                            return got
        return None

    full = walk("/", 0)
    return full, best[0], "/".join(tokens[best[1]:])


CONTAINERS = ("Projects", "Clients", "Sandbox", "Optimal", "Research", "Vault", "School")


def git_root(d):
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def check_imports():
    """Every @import line in a CLAUDE.md must load, and a broken one is SILENT
    (verified on 2.1.223 — no warning, the line just sits as literal text).
    Two ways to break: the target doesn't resolve (incl. a dead symlink), or —
    for project-level files only — the literal path escapes the project
    (containment is checked before symlink resolution, so an in-project symlink
    to ~/.claude/modes/ is the sanctioned escape; a direct home path is not).
    The user-level ~/.claude/CLAUDE.md is exempt from containment (verified)."""
    home = os.path.expanduser("~")
    files = [os.path.join(home, ".claude", "CLAUDE.md")]
    for c in CONTAINERS:
        files += glob.glob(os.path.join(home, c, "*", "CLAUDE.md"))
        files += glob.glob(os.path.join(home, c, "*", "*", "CLAUDE.md"))
    bad = []
    for f in files:
        if not os.path.isfile(f):
            continue
        base = os.path.dirname(f)
        user_level = f.startswith(os.path.join(home, ".claude") + os.sep)
        fenced = False
        for line in open(f, errors="ignore"):
            line = line.strip()
            if line.startswith("```"):
                fenced = not fenced
                continue
            if fenced or not line.startswith("@") or len(line) < 2:
                continue
            raw = line.split()[0][1:]
            if "/" not in raw and not raw.endswith(".md"):
                continue                             # "@handle" prose, not an import path
            target = os.path.expanduser(raw)
            if not os.path.isabs(target):
                target = os.path.join(base, target)
            literal = os.path.normpath(target)
            if not os.path.exists(literal):          # follows symlinks: dead link fails here
                bad.append((f, raw, "target missing — import fails silently"))
                continue
            if not user_level:
                root = git_root(base) or base
                if os.path.commonpath([literal, root]) != root:
                    bad.append((f, raw, "literal path outside the project — never loads"))
    return bad


def audit():
    orphans, dangling, unindexed, live = [], [], [], []
    total_topics = 0

    for store in sorted(glob.glob(os.path.join(ROOT, "*", "memory"))):
        slug = os.path.basename(os.path.dirname(store))
        topics = {os.path.basename(f) for f in glob.glob(store + "/*.md")} - {"MEMORY.md"}
        index = os.path.join(store, "MEMORY.md")
        if not topics and not os.path.exists(index):
            continue
        total_topics += len(topics)

        full, deepest, remainder = resolve(slug)
        if full:
            live.append((len(topics), full))
        else:
            orphans.append((len(topics), slug, deepest, remainder))

        text = open(index, errors="ignore").read() if os.path.exists(index) else ""
        links = set(re.findall(r"\]\(([^)#]+\.md)\)", text))
        for missing in sorted(links - topics):
            dangling.append((full or slug, missing))
        for extra in sorted(topics - links - INTENTIONALLY_UNINDEXED):
            unindexed.append((full or slug, extra))

    print(f"{'topics':>6}  path")
    print("-" * 78)
    for n, path in sorted(live, key=lambda r: -r[0]):
        print(f"{n:>6}  {path}")
    print("-" * 78)
    print(f"{len(live)} live stores, {total_topics} topic files\n")

    problems = 0

    if orphans:
        problems += len(orphans)
        print(f"❌ ORPHANED STORES ({len(orphans)}) — the working directory no longer exists.")
        print("   These memories are invisible: native memory is keyed to the exact cwd")
        print("   and does not walk up the tree.\n")
        for n, slug, deepest, rem in sorted(orphans, key=lambda r: -r[0]):
            print(f"   {n:>4} files  {deepest}/[{rem}]")
            print(f"              slug: {slug}")
        print()

    if dangling:
        problems += len(dangling)
        print(f"❌ DANGLING INDEX LINKS ({len(dangling)}) — MEMORY.md points at a file that is gone.\n")
        for where, link in dangling:
            print(f"   {where}  ->  {link}")
        print()

    broken_imports = check_imports()
    if broken_imports:
        problems += len(broken_imports)
        print(f"❌ BROKEN CLAUDE.md IMPORTS ({len(broken_imports)}) — these fail with no warning at all.\n")
        for f, raw, why in broken_imports:
            print(f"   {f}")
            print(f"      @{raw}  ->  {why}")
        print()

    if unindexed:
        problems += len(unindexed)
        print(f"⚠️  UNINDEXED FILES ({len(unindexed)}) — on disk but absent from MEMORY.md.")
        print("   Still recallable by `description:` match, but not findable by browsing.")
        print("   If deliberate, add the name to INTENTIONALLY_UNINDEXED in this script.\n")
        for where, f in unindexed:
            print(f"   {where}  ->  {f}")
        print()

    if not problems:
        print("✅ Clean. Every store resolves, every link resolves, everything is indexed.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(audit())
