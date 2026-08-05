#!/usr/bin/env python3
"""Move topic files out of dead stores into live ones, per an explicit manifest.

    python3 route.py my-manifest.py

The manifest names every file. That is deliberate: a glob would move files you
never looked at, and the whole point of the triage step is that a human (or a
model that read the descriptions) decided about each one. A file that is in
neither `routes` nor `delete` is reported as LEFT — the run is not finished
until every store reports LEFT 0.

Refuses to overwrite: if the destination already holds a file with that name it
reports a COLLISION and skips. Duplicates across stores are real — resolve them
by hand, because the two copies have usually drifted.

Manifest format:

    MANA = "/Users/carterking/Clients/mana-ventures"

    JOBS = [
      {
        "src": "-Users-carterking-Projects-Clients-mana-ventures",
        "routes": {
          MANA: ["project-drive-organization.md", "reference-mana-install-prompt.md"],
          "/Users/carterking/Projects": ["reference-bumblebee-scanner.md"],
        },
        "delete": ["project-superseded-thing.md"],
        "rename": {"old_underscore_name.md": "new-hyphen-name.md"},   # optional
      },
    ]

Destination keys are absolute working directories, not slugs — the encoding is
applied here so the manifest stays readable.
"""
import os, sys, shutil, glob, importlib.util

ROOT = os.path.expanduser("~/.claude/projects")


def load(path):
    spec = importlib.util.spec_from_file_location("manifest", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(manifest_path):
    manifest = load(manifest_path)
    moved_all = deleted_all = left_all = 0

    for job in manifest.JOBS:
        src = os.path.join(ROOT, job["src"], "memory")
        if not os.path.isdir(src):
            print(f"!! MISSING SOURCE {job['src']}")
            continue
        print(f"\n=== {job['src']}")
        rename = job.get("rename", {})
        moved = deleted = 0
        missing = []

        for cwd, files in job.get("routes", {}).items():
            dest = os.path.join(ROOT, cwd.replace("/", "-"), "memory")
            os.makedirs(dest, exist_ok=True)
            ok = 0
            for f in files:
                s = os.path.join(src, f)
                if not os.path.exists(s):
                    missing.append(f)
                    continue
                d = os.path.join(dest, rename.get(f, f))
                if os.path.exists(d):
                    print(f"  !! COLLISION skipped: {f} -> {cwd}")
                    continue
                shutil.move(s, d)
                moved += 1
                ok += 1
            print(f"  -> {cwd}  ({ok})")

        for f in job.get("delete", []):
            s = os.path.join(src, f)
            if not os.path.exists(s):
                missing.append(f)
                continue
            os.remove(s)
            deleted += 1
        if deleted:
            print(f"  -> deleted {deleted}")

        left = [os.path.basename(f) for f in glob.glob(src + "/*.md")
                if os.path.basename(f) != "MEMORY.md"]
        print(f"  moved {moved}, deleted {deleted}, LEFT {len(left)}")
        if left:
            print("     LEFT:", ", ".join(left))
        if missing:
            print("     NAMED BUT NOT FOUND:", ", ".join(missing))
        moved_all += moved
        deleted_all += deleted
        left_all += len(left)

    print(f"\nTOTAL moved {moved_all}, deleted {deleted_all}, left {left_all}")
    if left_all:
        print("Not finished — every file must be routed or deleted explicitly.")
    return 1 if left_all else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
