# Mode: make

You are **building**, against a plan that already exists.

## What this mode is for

Skills, scripts, and hooks that operate the memory system. The design questions are settled in
`../plan/` — if one is not, that is a signal to stop, not to decide it here.

## How to work here

- **Verification is the product.** Every failure this project has fixed was silent: a rule that
  enforced nothing, a hook writing to a file nobody read, a symlink pointing at a deleted folder.
  Anything built here must be able to report that it did not work.
- **Check that pointers resolve.** Not that they exist — that they resolve. That single check would
  have caught 162 stranded files, 7 dead symlinks, and 2 hubs aimed at deleted directories.
- **Dry-run first for anything destructive.** Print the full impact list, then act on confirmation.

## Where things go

Code here. Read `../plan/` freely. Read `../.claude/memory/context.md` for current state.

**Write only inside `make/`.** If a plan needs changing, say so and stop — do not edit `../plan/`
from here, and do not route around that with `python -c` or `node -e`.
