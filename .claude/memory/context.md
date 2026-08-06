# Context — memory-management

**Last updated:** 2026-08-06 (session 2 — manifest review, mode-files design)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**The Phase 2.5 manifest is reviewed and the architecture is settled.** Carter reviewed
`plan/container-consolidation-manifest.md` line by line and the design went through two revisions
in one sitting, both his:

- **Rev 1 — the sorted MEMORY.md:** index entries sorted into Project / Research / Plan / Make /
  References sections.
- **Rev 2 — the mode files:** mode *principles* leave memory entirely and live once at
  `~/.claude/modes/RESEARCH-MODE.md` / `PLAN-MODE.md` / `MAKE-MODE.md`, pulled into each project's
  mode `CLAUDE.md` by one `@import` line (a reference, not a copy — nothing forks). The routing
  test (Carter, verbatim): project-specific → MEMORY.md (*Project Awareness*); mode principle →
  `<MODE>-MODE.md` (*Situational / Mode Awareness*). CLAUDE.md-vs-memory tiering recorded:
  **CLAUDE.mds explain and navigate; memory remembers.**
- **Ruled:** `newsession-focus-ghostty` DELETE · user-* GLOBAL approved · `subskill-vs-reference`
  fold-into-skill-factory-reference then delete · the three CLAUDE.md-promoted rules come back OUT
  of the global CLAUDE.md · **ALWAYS.md approved contingent on the `@import` sentinel test**
  (must also prove a *broken* import fails loud — silent would be E5 again).
- **Tranche state:** T1 53 routes (awaiting go) · T2 5 (2 of 5 ruled) · T3 26 (8 ASKs open) ·
  T4 90 (approved: 36 → mode files, 12 → ALWAYS.md, 42 stay as the `~/Projects` library).
- This session also: merged `worktree-mode-memory-research` into main (7fd111b), hand-folded that
  session's transcript (Procedure C), corrected the misrecorded launch convention **in place**
  (the decisions.md in-place-correction exception is now written in its header), answered the
  git-toplevel rules (containers never / projects yes / modes never), and recorded the
  worktree-memory-promotion TODO.
- Machine state: audit clean (24 stores / 315 topics), zero moves executed — the manifest is
  still a proposal in flight, exactly as designed.

## ⏭️ Next steps / open

Full list in `plan/ROADMAP.md`. **Carter's call: execution happens in a NEW session** — see
`handoffs/handoff-latest.md` for the ordered next actions. In short:

1. **Merge `worktree-phase25-manifest` into main** (8 commits, local only — no remote), then fold
   this session's transcript out of the worktree-keyed dir **before** deleting the worktree.
2. **Run the `@import` sentinel test** (home-path import loads; broken import loud or silent) —
   gates ALWAYS.md and the whole mode-files delivery.
3. **Get Carter's remaining gates:** Tranche 1 go (53 routes) · 3 unruled Tranche 2 files ·
   8 ASKs.
4. **Execute per the manifest's procedure** (backup → toplevel re-check → route.py → sectioned
   indexes per the template → fold 36+12 into mode files → CLAUDE.md demotion → audit exit 0),
   **capturing the runbook as it runs.**
5. Carried forward: the four audit.py checks · correction sweep + close-session/new-session skill
   updates (⚠️ two sessions old, unmoved) · worktree memory promotion review · skills-symlink
   sentinel · floor re-measure · mempalace re-mine of this memory dir post-merge.

## 🧠 Recent decisions

See `decisions.md` (three entry groups dated 2026-08-06). Load-bearing:

- **Mode principles live once, in shared mode files, delivered by `@import`** — copies drift,
  references can't fork.
- **The routing test:** Project Awareness vs Situational/Mode Awareness.
- **CLAUDE.mds explain and navigate; memory remembers** — the three-tier division.
- **Misrecordings are corrected in place, never by appending** — conflicting statements confuse
  agents; a misunderstanding was never a decision.
- **ALWAYS.md approved contingent on the `@import` sentinel test.**

## 💡 What we learned

- **Symlinks are whole-file only; `@import` is the block-level include.** The mechanism Carter
  wanted ("symlink a block of text") exists natively as the CLAUDE.md import line — one layer up,
  no filesystem link to dangle.
- **The recall gap closes at the instruction layer, not the memory layer.** Relocating memory
  never made rules load everywhere; mode files + import do — instructions are
  write-once-read-everywhere, memory is write-as-you-go, and June's failures came from mixing them.
- **A reviewed manifest beats a clever plan.** Carter's notes rerouted ~2% of Tranche 1 (falsifier
  threshold was 15%) but redesigned Tranche 4 entirely — the per-file layer was right, the
  architecture layer needed him.
- **Editor buffers aren't disk.** Carter's Cursor notes were invisible until Cmd+S — checksum
  against git before concluding "no changes."

## 📂 Files touched · 🌿 git

Project at `~/Projects/memory-management/`. This session (branch `worktree-phase25-manifest`,
8 commits incl. close): `plan/container-consolidation-manifest.md` (new — the deliverable),
`plan/ROADMAP.md` (mode-files decision, git-init item, worktree-promotion TODO),
`decisions.md` (in-place exception header + mode-files entry), `handoffs/handoff-latest.md`,
this file. Outside the repo: prior session's transcript hand-folded into
`~/.claude/projects/-Users-carterking-Projects-memory-management/`;
`~/Claude/session-logs/thinking-patterns.md` + `2026-08-06.md`. **Native memory deliberately not
written from this worktree** (worktree stores orphan on deletion — the exact trap the promotion
TODO covers); the `@import` sentinel results belong in `reference-claude-code-loading-mechanics`
when the execution session runs the test from the project root.
