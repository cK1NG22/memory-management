#!/usr/bin/env python3
"""Generate a MEMORY.md index for a store from its topic files' frontmatter.

    python3 mkindex.py <cwd> "<one-line blurb>"
    python3 mkindex.py /Users/carterking/Clients/outreach "Optimal AI cold outreach."

Overwrites MEMORY.md for that store. Only do this for a store you have just
rebuilt — for a curated index (anything you have hand-merged), append by hand
instead, because this throws away merged lines and editorial ordering.

The generated hook is the first clause of each `description:`, capped. That is
good enough for a project store. It is *not* good enough for a store that loads
on every session — there, merge related entries onto shared lines by hand. Every
line in MEMORY.md is a permanent per-session token cost; a topic file is free
until it is recalled.
"""
import os, sys, glob, re

ROOT = os.path.expanduser("~/.claude/projects")

SECTIONS = [("project", "Projects & work"), ("reference", "References"),
            ("feedback", "Working norms"), ("user", "Who / context"), ("?", "Other")]

STRIP = ("project-", "reference-", "feedback-", "user-",
         "project_", "reference_", "feedback_", "user_")


def frontmatter(path):
    text = open(path, errors="ignore").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    if m:
        for key in ("name", "description", "type"):
            hit = re.search(r"^\s*%s:\s*(.+)$" % key, m.group(1), re.M)
            if hit:
                out[key] = hit.group(1).strip().strip('"')
    return out


def title(filename, name):
    s = name or filename[:-3]
    for prefix in STRIP:
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    return s.replace("-", " ").replace("_", " ")


def hook(desc, limit=95):
    if not desc:
        return ""
    d = desc.strip()
    for sep in (" — ", "; ", ". "):
        i = d.find(sep)
        if 0 < i < limit:
            d = d[:i]
            break
    d = d.strip().rstrip(".")
    if len(d) > limit:
        d = d[:limit].rsplit(" ", 1)[0] + "…"
    return d


def build(cwd, blurb):
    store = os.path.join(ROOT, cwd.replace("/", "-"), "memory")
    if not os.path.isdir(store):
        sys.exit(f"no store for {cwd}  (expected {store})")
    files = sorted(f for f in glob.glob(store + "/*.md")
                   if os.path.basename(f) != "MEMORY.md")
    buckets = {k: [] for k, _ in SECTIONS}
    for f in files:
        meta = frontmatter(f)
        base = os.path.basename(f)
        kind = meta.get("type", "?")
        if kind not in buckets:
            kind = "?"
        buckets[kind].append(
            f"- [{title(base, meta.get('name'))}]({base}) — {hook(meta.get('description', ''))}")

    out = [f"# Memory Index — {cwd.replace(os.path.expanduser('~'), '~')}", "", f"*{blurb}*", ""]
    for key, label in SECTIONS:
        if buckets[key]:
            out += [f"## {label}", ""] + sorted(buckets[key]) + [""]
    text = "\n".join(out).rstrip() + "\n"
    open(os.path.join(store, "MEMORY.md"), "w").write(text)
    print(f"{len(files)} entries, {len(text)}B -> {store}/MEMORY.md")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
