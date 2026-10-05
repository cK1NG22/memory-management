# Mode-files delivery runbook

Captured 2026-08-06 while executing the Phase 2.5 mode-files delivery (manifest Tranche 4).
Use when delivering the shared mode files to a new machine, re-wiring them, or stamping a new
project's mode folders (Phase 3 does this per project).

## The mechanics this rides on (verified on CLI 2.1.223 — re-test after CLI upgrades)

Full record: `reference-claude-code-loading-mechanics` in the memory-management native store.

- A CLAUDE.md `@import` only expands when the **literal** path sits inside the importing file's
  project (containment is checked *before* symlink resolution).
- Therefore `@~/.claude/modes/X.md` in a project file **silently never loads** — but an
  **in-project symlink** pointing at `~/.claude/modes/X.md`, imported by filename, loads fine.
- The user-level `~/.claude/CLAUDE.md` is exempt from containment: it imports
  `@~/.claude/modes/ALWAYS.md` directly, no symlink.
- A broken import (missing target, dead symlink, containment escape) fails **with no warning
  anywhere** — exit 0, empty stderr, the `@line` just sits as literal text. This is why
  `audit.py`'s imports check exists; never wire an import without it.

## Procedure

1. `python3 make/memory-repair/audit.py` → must be clean before touching anything.
2. Back up any store whose topics will be folded/deleted:
   `cp -R ~/.claude/projects/<store>/memory ~/Claude/_archive/container-stores_<date>/<name>`.
   Verify the copy by file count, not by eyeball.
3. Write / update the canonical files: `~/.claude/modes/ALWAYS.md`, `RESEARCH-MODE.md`,
   `PLAN-MODE.md`, `MAKE-MODE.md`. Fold each memory topic's rule + why + how-to-apply; the topic
   files are deleted afterward, so the fold must carry everything load-bearing.
4. Global wiring (once per machine): `~/.claude/CLAUDE.md` gets
   `@~/.claude/modes/ALWAYS.md`. Remove any global-CLAUDE.md text the fold now covers — only if
   the removal is recall-neutral (ALWAYS.md loads in every session; a mode file loads only in
   projects that are wired, so those demotions wait for Phase 3).
5. Per-project wiring (this is what Phase 3 stamps everywhere):
   ```
   ln -s ~/.claude/modes/RESEARCH-MODE.md <project>/research/RESEARCH-MODE.md   # abs target —
   ln -s ~/.claude/modes/PLAN-MODE.md     <project>/plan/PLAN-MODE.md           # survives a
   ln -s ~/.claude/modes/MAKE-MODE.md     <project>/make/MAKE-MODE.md           # project move
   ```
   and each mode `CLAUDE.md` ends with `@<MODE>-MODE.md` (the symlink's filename — same dir).
6. Verify delivery, don't assume it: headless probe from a mode dir asking whether a phrase that
   exists only in the mode file is present in context. `claude -p "... is '<phrase>' present?"`.
7. Only after the probe passes: delete the folded topic files and strip their `MEMORY.md` index
   lines (a dangling index line is an audit failure).
8. `python3 make/memory-repair/audit.py` → exit 0. The imports check runs on every audit from now
   on; it scans `~/.claude/CLAUDE.md` plus `<container>/*/CLAUDE.md` and
   `<container>/*/*/CLAUDE.md`, flags missing targets and containment escapes, and has a negative
   test proving it can fail.

## Failure modes this procedure exists to prevent

| Symptom | Cause | Caught by |
| --- | --- | --- |
| Mode rules silently absent | import target missing / symlink dead | audit imports check, step 6 probe |
| Mode rules silently absent everywhere | `@~/...` home path used in a project file | audit containment check |
| Rule lost entirely | topic deleted before fold verified | step ordering (6 before 7) |
| Fold lost on disaster | no backup | step 2 |
