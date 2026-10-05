# Mode: make

You are **building**, against a plan that already exists.

## What this mode is for

Code, scripts, skills, and hooks. The design questions are settled in `../plan/`. If one is not,
that is a signal to stop, not to decide it here.

## How to work here

- **Verification is the product.** Anything built here must be able to report that it did not work.
  Silent success is the failure mode this structure exists to prevent.
- **Check that pointers resolve.** Not that they exist: that they resolve. Dead symlinks and missing
  import targets look identical to working ones from inside a session.
- **Dry-run first for anything destructive.** Print the full impact list, then act on confirmation.

## Where things go

Code here. Read `../plan/` freely. Read `../.claude/memory/context.md` for current state.

**Write only inside `make/`.** If a plan needs changing, say so and stop. Do not edit `../plan/` from
here, and do not route around that with `python -c` or `node -e`.

## Mode principles

The rule files in `.claude/rules/` beside this file. They load when a session starts in this folder.
They are copies from the mode library; `modes.py check` reports any that differ.
