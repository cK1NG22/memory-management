#!/usr/bin/env python3
"""Fold transcript dirs deeper than <container>/<project>/ up into the project-level
dir (Carter's session-launch convention, 2026-08-06). Mode-level dirs
(<project>/research|plan|make) stay. memory/ folders never move. Dirs with write
activity in the last hour are skipped (a session may be running there).

Usage: transcript_consolidate.py [--execute]   (default: dry run)"""
import os, sys, time, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit import resolve

ROOT = os.path.expanduser("~/.claude/projects")
HOME = os.path.expanduser("~")
CONTAINERS = {"Projects", "Sandbox", "Clients", "Optimal", "School", "Research", "Vault"}
MODES = {"research", "plan", "make"}
EXECUTE = "--execute" in sys.argv


def encode(path):
    return path.replace("/", "-").replace(".", "-")


def recently_active(path, seconds=3600):
    now = time.time()
    for dp, _, fs in os.walk(path):
        for f in fs:
            try:
                if now - os.path.getmtime(os.path.join(dp, f)) < seconds:
                    return True
            except OSError:
                pass
    return False


for d in sorted(os.listdir(ROOT)):
    src = os.path.join(ROOT, d)
    if not os.path.isdir(src):
        continue
    full, _, _ = resolve(d)
    if not full or not full.startswith(HOME + "/"):
        continue
    parts = full[len(HOME) + 1:].split("/")
    if parts[0] not in CONTAINERS or len(parts) <= 2:
        continue                                   # top-level, project-level, or elsewhere
    if len(parts) == 3 and parts[2] in MODES:
        continue                                   # mode-level dirs stay
    movable = [e for e in os.listdir(src) if e != "memory"]
    if not movable:
        continue
    if recently_active(src):
        print(f"SKIP (active in last hour): {d}")
        continue
    tgt = os.path.join(ROOT, encode(f"{HOME}/{parts[0]}/{parts[1]}"))
    print(f"MOVE {len(movable):>3} items  {d}  ->  {os.path.basename(tgt)}")
    if EXECUTE:
        os.makedirs(tgt, exist_ok=True)
        for e in movable:
            shutil.move(os.path.join(src, e), os.path.join(tgt, e))
        if not os.listdir(src):
            os.rmdir(src)

print("\n" + ("EXECUTED" if EXECUTE else "dry run — nothing moved; re-run with --execute"))
