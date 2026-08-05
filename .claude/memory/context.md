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
- **Skill relocation tranche 1 is done:** the 11 project-scoped symlinks now load from
  `~/School/.claude/skills/` and `~/Optimal/.claude/skills/` instead of global — 102 global
  skills, ~1,440 tokens lighter in every session. Remaining tranches: `plan/skill-relocation-plan.md`.
- The **two-system split is settled** — native memory for Carter-and-machine facts, project memory
  for the work. **This project is the Gen 4 trial.**

## ⏭️ Next steps / open

Full list in `plan/ROADMAP.md`.

1. **Carter's calls on relocation tranche 2** — the physical-move candidates and their proposed
   destinations are in `plan/skill-relocation-plan.md` (notion-transcript retire?, curriculum
   skills, `daily-standup`/`source-leads` → Optimal, file-type skills question).
2. **Read the post-relocation floor** off the next normal session's `.jsonl` — the free re-measure.
3. **Build `/context-dashboard`** — read `[[project-orchestrator-agent-deferred]]` first.
4. Then **restructure projects to the mode shape** (templates + auto-symlinked mode skills — the
   symlink halves of this now have a proven pattern *and* a proven failure mode).

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

Project at `~/Projects/memory-management/`. This session (branch `worktree-skill-relocation`):
`plan/skill-relocation-plan.md` (new), `plan/ROADMAP.md`, this file, `decisions.md`.
Outside the repo: `~/.claude/skills/` (12 links fixed → 11 then relocated),
`~/School/.claude/skills/` (new, 5 links), `~/Optimal/.claude/skills/` (new, 6 links).
