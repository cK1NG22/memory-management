#!/usr/bin/env python3
"""Print name + description + size for every topic file in one or more stores.

    python3 dump.py -Users-carterking-Projects-Personal [more-slugs...]

This is the triage view. Read descriptions, not bodies — the `description:`
field is what recall actually matches on, so a file whose description does not
say what it is was already broken before it was orphaned.

Two signals to watch for:
  • `[?]` with "(no description)" — the file has no native frontmatter. It is
    probably not a memory at all, but a document written into the memory folder
    because that was the nearest writable place.
  • underscores in the filename — Gen 1 naming. Normalize to hyphens on the way
    out (route.py has a `rename` field for this).
"""
import os, sys, glob, re

ROOT = os.path.expanduser("~/.claude/projects")


def frontmatter(path):
    text = open(path, errors="ignore").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    found = {}
    if m:
        for key in ("name", "description", "type", "modified"):
            hit = re.search(r"^\s*%s:\s*(.+)$" % key, m.group(1), re.M)
            if hit:
                found[key] = hit.group(1).strip().strip('"')
    return found, len(text)


def main(slugs):
    for slug in slugs:
        store = os.path.join(ROOT, slug, "memory")
        if not os.path.isdir(store):
            print(f"!! no such store: {slug}")
            continue
        files = sorted(glob.glob(store + "/*.md"))
        topics = [f for f in files if os.path.basename(f) != "MEMORY.md"]
        print("\n" + "=" * 100)
        print(f"STORE: {slug}  ({len(topics)} topics)")
        print("=" * 100)
        for f in files:
            base = os.path.basename(f)
            meta, size = frontmatter(f)
            if base == "MEMORY.md":
                print(f"\n[INDEX] MEMORY.md  {size}B")
                continue
            print(f"\n• {base}  [{meta.get('type', '?')}] {size}B")
            print(f"  {meta.get('description', '(no description)')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
