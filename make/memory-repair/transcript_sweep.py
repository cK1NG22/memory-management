#!/usr/bin/env python3
"""Sweep transcript-only dirs out of ~/.claude/projects.

Dirs under ~/.claude/projects hold session transcripts (*.jsonl + per-session UUID
folders) and sometimes a memory/ store. Transcript dirs for working directories that
no longer exist (deleted worktrees, throwaway experiment trees, retired shift dirs)
are dead weight — they can't be resumed and nothing reads them.

Default run is a read-only report. `--archive` moves dead dirs to
~/Claude/_archive/projects-transcripts_<date>/ (never deletes).

A dir containing any file under memory/ is NEVER moved — that's a store; stores are
audit.py's jurisdiction and a human decision.
"""
import os, sys, glob, shutil, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit import resolve

ROOT = os.path.expanduser("~/.claude/projects")
# ponytail: date comes from the wall clock — fine here, this never runs inside a workflow script
STAMP = datetime.date.today().isoformat()
ARCHIVE = os.path.expanduser(f"~/Claude/_archive/projects-transcripts_{STAMP}")


def classify():
    dead, live, stores = [], [], []
    for d in sorted(os.listdir(ROOT)):
        path = os.path.join(ROOT, d)
        if not os.path.isdir(path):
            continue
        if glob.glob(os.path.join(path, "memory", "*")):
            stores.append(d)
            continue
        size = sum(
            os.path.getsize(os.path.join(dp, f))
            for dp, _, fs in os.walk(path) for f in fs
        )
        full, _, _ = resolve(d)
        (live if full else dead).append((size, d, full))
    return dead, live, stores


def main():
    do_archive = "--archive" in sys.argv
    dead, live, stores = classify()

    print(f"{len(stores)} memory stores (untouchable) · {len(live)} live transcript dirs · "
          f"{len(dead)} dead transcript dirs ({sum(s for s, _, _ in dead)/1e6:.1f} MB)")
    for size, d, _ in sorted(dead, key=lambda r: -r[0]):
        print(f"  {size/1e6:>7.1f}MB  {d}")

    if not dead:
        print("✅ nothing to sweep")
        return 0
    if not do_archive:
        print(f"\nread-only report. Re-run with --archive to move these to {ARCHIVE}")
        return 1
    os.makedirs(ARCHIVE, exist_ok=True)
    for _, d, _ in dead:
        shutil.move(os.path.join(ROOT, d), os.path.join(ARCHIVE, d))
    print(f"\narchived {len(dead)} dirs -> {ARCHIVE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
