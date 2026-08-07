# Context — memory-management

**Last updated:** 2026-08-06 (session 3, part 2 — Tranches 1–3 executed; Phase 2.5 consolidation COMPLETE)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**Phase 2.5 is COMPLETE — all four tranches executed, audit exit 0 (37 stores / 264 topics).**
Carter's "tranch 1-3 approved" landed the same night as the mode-files delivery: 65 moves, 3
deletes, 12 new project stores, `~/Optimal`/`~/Vault`/`~/Research` emptied to explanatory stubs,
`~/Projects` rewritten as the dual-role library (59 files: user + norms + parked/holds +
references). ASK rulings, fix-in-passing, and the run's three lessons (space-encoding, merged
index lines, stay-set assertion) are in the manifest's "Execution record" section and
`decisions.md`. Pre-move backup: `~/Claude/_archive/container-stores_2026-08-06-pre-tranche123/`.

**Tranche 4's mode-files delivery is EXECUTED.** The `@import` sentinel test overturned the
approved mechanism — home-path imports silently never load (containment is lexical, pre-symlink)
— and Carter re-approved delivery via in-project symlinks, matching the mode-skills shape. The
four files live at `~/.claude/modes/` (ALWAYS, RESEARCH-MODE, PLAN-MODE, MAKE-MODE); ALWAYS.md is
imported directly by `~/.claude/CLAUDE.md` (user level is containment-exempt); this project's
three mode CLAUDE.mds import via symlink, probe-verified; the 48 folded topics are deleted
(backup: `~/Claude/_archive/container-stores_2026-08-06/`); `audit.py` gained a broken-imports
check with a negative test. Procedure: `docs/mode-files-runbook.md`. Tranches 1–3 still await
Carter's gates. Mempalace is dead (Carter: never uses it) — strike it from workflows.

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

1. ~~Merge · transcript fold · sentinel test · mode-files delivery~~ **done 2026-08-06 (session
   3).** The fold was vacuous — EnterWorktree mid-session doesn't re-key transcripts.
2. ~~Gates + Tranches 1–3 execution~~ **done 2026-08-06 (session 3, part 2)** on Carter's blanket
   approval — ASK rulings are listed in the manifest's execution record for reversal if any reads
   wrong.
3. **Phase 3 carries:** stamping mode CLAUDE.mds + symlinks in every project (the runbook's step
   5), then removing `# Planning a build` from the global CLAUDE.md (marked with a comment).
5. Carried forward: the four audit.py checks (shared-file symlinks gate — the imports check is
   built, the four store-level ones are not) · correction sweep + close-session/new-session skill
   updates (⚠️ three sessions old now) · worktree memory promotion review · skills-symlink
   sentinel · floor re-measure.

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
- **Import containment is lexical and pre-symlink** — the one untested assumption in an approved
  design was the one that failed. The contingency test earned its place; keep making approvals
  contingent on the load-bearing mechanic.
- **A tripwire isn't built until it has failed on purpose.** The audit imports check shipped with
  a negative test that fabricates both failure modes.
- **Probe the encoding before keying a store to an unusual path.** The CLI turns spaces into
  dashes too (`~/Standard Works` → `-Users-carterking-Standard-Works`); naive `/`→`-` encoding
  builds stores the CLI never reads. One haiku probe settles it.
- **Merged index lines are couplings.** They save per-session tokens in a library store, but the
  moment two co-linked files route to different destinations, every reused copy dangles. Reuse a
  curated line only when all its links travel together.

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
