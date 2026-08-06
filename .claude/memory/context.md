# Context — memory-management

**Last updated:** 2026-08-05

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**Cleanup is finished and the pruning has started.** The fix → prune → measure sequence is underway
with the baseline safely captured.

- The **legacy hub is gone** (167 files harvested) and the **16 orphaned stores are resolved**
  (139 routed, 17 moved out of the memory system, 9 deleted). 23 live stores, 309 topic files,
  0 dangling links. Backup at `~/Claude/_archive/orphan-stores_2026-08-04/`.
- **The repair is written down and tooled** — `docs/memory-repair-runbook.md` plus
  `make/memory-repair/`. Run `python3 make/memory-repair/audit.py` before and after moving any folder.
- **`history.md` is retired** (executed 2026-08-05) — all four writers stopped, the Stop hook
  unwired and archived. Existing copies are inert.
- **The dead skill symlinks are fixed** (2026-08-05) — 12 were dead, not the recorded 7; 11
  re-pointed, 1 removed (target gone upstream). Zero dead links remain.
- **The context floor is measured, not estimated:** 44K–55K tokens at session start; the global
  skill catalog was 113 skills ≈ 7.8K tokens of it (~15–18% of the floor).
- **Skill relocation tranches 1 AND 2 are done — global is 96 skills, was 113 this morning**
  (~2,600 catalog tokens lighter per session). Tranche 1: the 11 project symlinks →
  `~/School/` and `~/Optimal/` `.claude/skills/`. Tranche 2 (Carter-approved): curriculum
  quizzes → `~/Projects/ai-engineering/`, `daily-standup`/`source-leads`/`notion-transcript` →
  `optimal-claude-skills` (kept, not retired — Carter), `connect-vault` → `~/Research/`.
  `resolve-vulns` parked in global, undecided. Full map: `plan/skill-relocation-plan.md`.
- **The mode-skill shape is decided:** one folder-level symlink per mode per project
  (`<mode>/.claude/skills → ~/.claude/modes/<mode>/skills`), per-skill links only inside the
  mode home. **Sentinel-test the folder-level link before building the templates** — unverified.
- **The automations-project direction is endorsed:** plist `WorkingDirectory` pinning dissolves
  the cron-locked category; dream colocates with memory-management instead. Shifts run in the
  relevant project's `make/` (possibly `make/shift-work/`) — design later.
- The **two-system split is settled** — native memory for Carter-and-machine facts, project memory
  for the work. **This project is the Gen 4 trial.**

## ⏭️ Next steps / open

Full list in `plan/ROADMAP.md`.

1. **Symlinked-memory design session is IN FLIGHT** (started 2026-08-05, ~4 PM) — testing whether
   native stores/topic files/MEMORY.md can be symlinks, then designing shared memory analogous to
   the mode-skill shape. Findings land in `research/`, the design in `plan/`. Don't duplicate it.
2. **Read the post-relocation floor** off the next normal session's `.jsonl` — the free re-measure
   that settles the suspended argument.
3. **Sentinel-test the folder-level skills symlink** — blocks the mode templates (the in-flight
   session's experiments may cover this — check before re-running).
4. **Build `/context-dashboard`** — read `[[project-orchestrator-agent-deferred]]` first.
5. Then **restructure projects to the mode shape**; create the automations project when Carter
   is ready. Undecided: `resolve-vulns` home, file-type skills mode. Also open: the nested
   `skill-factory` repo (inside `optimal-claude-skills`, own remote) has uncommitted changes.

## 🧠 Recent decisions

See `decisions.md`. The ones that shape everything else:

- Folders are a **loading** mechanism, not a locking one — nothing here is a hard write boundary.
- Memory lives **once at the project root**, never per mode.
- `history.md` is **deleted**, not capped — four writers (not three), zero readers.
- Fix symlinks **before** measuring; measure **before** relocating — each step protects the next
  one's honesty.
- Relocated skills are **symlinked into `<folder>/.claude/skills/`**, never physically moved
  without Carter; the gstack 53 stay put (installer-owned, only ~1.1K tokens).

## 💡 What we learned

- **Loading is not obeying.** A nearer, more specific instruction silently beats a distant general
  one even while the distant one sits fully loaded in context.
- **Native memory does not walk up the tree** — the mechanism behind every stranding.
- **A project that moves doesn't lose its memory — it silently starts a second one from zero.**
- **A dead symlink is a silent subtraction.** Fixing the 12 didn't just restore skills — it
  restored the truth of the baseline. Silent failures corrupt measurements, not just behavior.
- **Recorded counts drift; scans don't.** "7 dead symlinks" was true when written and wrong by
  execution. Anything cheap to re-derive should be re-derived, not trusted from notes.
- **A repair is worth less than the check that prevents the next one** — `audit.py` keeps paying;
  the project-level skill symlinks created today are exactly the kind of thing it should learn to
  check next.

## 📂 Files touched · 🌿 git

Project at `~/Projects/memory-management/`. This session (branch `worktree-skill-relocation`,
3 commits): `plan/skill-relocation-plan.md` (new), `plan/ROADMAP.md`, this file, `decisions.md`.
Outside the repo: `~/.claude/skills/` (113 → 96), `~/School/.claude/skills/` (new, 5 links),
`~/Optimal/.claude/skills/` (new, 9 links), `~/Optimal/optimal-claude-skills/` (3 skills moved
in, untracked), `~/Research/.claude/skills/` + `~/Projects/ai-engineering/.claude/skills/` (new,
real dirs).
