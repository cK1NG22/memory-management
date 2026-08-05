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
            name = "-".join(tokens[i:j])
            if not name:
                continue
            cand = os.path.join(base, name)
            if os.path.isdir(cand):
                got = walk(cand, j)
                if got:
                    return got
            # a dot-directory encodes as an empty token before the name
            if tokens[i] == "" and j > i + 1:
                cand = os.path.join(base, "." + "-".join(tokens[i + 1:j]))
                if os.path.isdir(cand):
                    got = walk(cand, j)
                    if got:
                        return got
        return None

    full = walk("/", 0)
    return full, best[0], "/".join(tokens[best[1]:])


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
