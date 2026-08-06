# Context — memory-management

**Last updated:** 2026-08-06

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**The mode-memory question is resolved — by the platform, not by us.** Sentinel experiments
(2026-08-06, Claude Code 2.1.223) proved native memory is keyed to the **git root**: every session
inside a repo project reads and writes ONE store, so research/plan/make already share memory.
No mode-memory layer gets built.

- **Full experiment record:** `research/sources/native-memory-keying-and-symlink-experiments.md`
  (git-root keying · exactly one store per session, ancestors never stack — the opposite of
  CLAUDE.md · physical-path keying · all three symlink forms load · E5: a dangling memory symlink
  is silently empty and the next write forks it self-camouflagingly · transcripts are portable and
  resume-by-id is global).
- **The design:** `plan/mode-memory-design.md` — shared topic files only (one canonical copy +
  file symlink + per-store index line), MEMORY.md never shared, store-dir symlinks demoted to
  repair tool. Four audit.py checks specified and **required before any symlink exists**.
- **Transcript housekeeping executed:** 46 dead dirs (294 MB) archived, 83 deep transcript items
  folded to project level. **Session-launch convention (Carter):** sessions open at
  `<container>/` (`~/Projects`, `~/Clients`, …), `<project>/`, or `<project>/<mode>/` —
  never deeper. Tools: `make/memory-repair/transcript_sweep.py` +
  `transcript_consolidate.py`; procedure: `docs/transcript-housekeeping-runbook.md` (the seed for
  a future dream skill).
- **Consequence now queued:** container stores stay live for
  container sessions, but a project-specific fact filed there never loads in the project sessions
  that need it — one store per session, ancestors never stack. Phase 2.5 is therefore a
  **placement** migration, not a dormancy rescue; full proposal in
  `plan/container-consolidation-manifest.md`, awaiting Carter's rulings.
- `worktree-skill-relocation` is **merged** (main moved to a31e76c; branch gone). This session's
  branch `worktree-mode-memory-research` (7 commits) awaits merge.
- Machine state verified clean twice today: 24 stores, 315 topic files, audit exit 0.

## ⏭️ Next steps / open

Full list in `plan/ROADMAP.md` (new Phase 2.5).

1. **Next session (planned with Carter):** merge `worktree-mode-memory-research`; run
   `transcript_consolidate.py --execute` to fold this session's transcript out of the worktree dir
   **before** removing the worktree (fold-then-delete order — see runbook); then start the
   **container-store consolidation** (Phase 2.5), capturing the process as a runbook.
2. **Build the four `audit.py` checks** (spec in `plan/mode-memory-design.md`).
3. **Correction sweep** — root `CLAUDE.md` table, `docs/memory-repair-runbook.md`, `audit.py`
   orphan message, and close-session's Phase-5 text all still claim exact-cwd keying. Also update
   the **`close-session` and `new-session` skills** to the new memory patterns (git-root keying,
   one store per session, launch convention, worktree handoff case) — Carter's ask, 2026-08-06.
4. **Review worktree memory promotion** (Carter's ask, 2026-08-06): project memory in worktrees
   merges via git (fine); the *native* store a worktree session keys is ephemeral and orphans on
   worktree deletion — no promotion path exists. Details in `plan/ROADMAP.md` Phase 2.5.
5. Still open from before: **sentinel-test the folder-level skills symlink** (today's memory tests
   do NOT cover the skills loader — different mechanism); post-relocation floor re-measure;
   `/context-dashboard`.

## 🧠 Recent decisions

See `decisions.md` (two entries 2026-08-06). The load-bearing ones:

- **No mode-memory layer** — git-root keying makes it redundant; symlinks would add a proven
  fork surface (E5).
- **Shared topic files are the one adopted sharing mechanism**; copying is forking; index line
  mandatory in each consuming store.
- **Sessions open at container, project, or mode level** — transcripts key to the exact launch
  cwd, so launch discipline is what keeps the transcript map readable.
- **Housekeeping tools are standing maintenance, not one-offs** — worktrees and background jobs
  recreate deep transcript dirs constantly.

## 💡 What we learned

- **Platform findings carry a version stamp.** "Native memory does not walk up" was true of
  non-git dirs and false inside repos — overgeneralized provenance, caught only by re-testing.
- **Exactly one memory store loads per session; ancestor stores never stack** — the opposite
  shape of the CLAUDE.md chain. Layered instructions vs one flat notebook per project.
- **The worst symlink failure self-camouflages:** a dangling store link reads as empty memory,
  and the next write recreates the stale target so resolve-checks pass again (E5).
- **Transcripts are logs, not knowledge** — keyed to launch cwd, portable, resume-by-id global;
  only `memory/` folders matter for recall.
- **Capture the process the first time it runs** (Carter) — the runbook written at first
  execution is the seed dream promotes into a skill.

## 📂 Files touched · 🌿 git

Project at `~/Projects/memory-management/`. This session (branch `worktree-mode-memory-research`,
7 commits): `research/sources/native-memory-keying-and-symlink-experiments.md` (new),
`plan/mode-memory-design.md` (new), `docs/transcript-housekeeping-runbook.md` (new),
`make/memory-repair/transcript_sweep.py` + `transcript_consolidate.py` (new), `plan/ROADMAP.md`,
`decisions.md`, this file. Outside the repo: `~/.claude/projects/` (83 dirs → 30: 46 archived to
`~/Claude/_archive/projects-transcripts_2026-08-06/`, 6 dirs folded up),
`reference-claude-code-loading-mechanics.md` in the `~/Projects` store (corrected + extended),
`~/Claude/personal-backlog.md` (terminal side-panel renderer TODO),
`~/Claude/session-logs/thinking-patterns.md`.
