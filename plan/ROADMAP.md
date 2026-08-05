# Roadmap — memory-management

**Status:** foundations done; the system is coherent for the first time. Everything below is net-new
work, not cleanup.

---

## ✅ Done — 2026-08-04

- [x] Establish how Claude Code actually loads and enforces things (empirically, not from docs)
- [x] Review the mode design — 4-seat Fable team + Opus packet auditor, two rounds
- [x] Resolve all 13 of Carter's annotations on the verdict
- [x] Write `docs/memory-systems-history.md` — the single surviving record of Gens 1–4
- [x] Neutralize the legacy hub — repoint 5 writers, relocate 2 operational logs, rehome 2 hubs
- [x] Harvest all 167 legacy-hub files; store reduced to a tombstone
- [x] Stand up this project in the Gen 4 mode structure *(it is the trial as well as the subject)*

---

## Phase 1 — Build the skills this work identified

- [ ] **`/move-project`** — relocate a project *and* everything path-coupled to it: the cwd-keyed
      native store, symlinks in both directions, ~23 config references, worktrees holding absolute
      paths. **A `--check` audit mode is the more valuable half** — it would have caught the June
      damage before it compounded. Spec: `[[project-move-project-skill-idea]]`.
- [ ] **`/context-dashboard`** — show the makeup of the context window given current memory settings:
      what `MEMORY.md` costs, what the global skill catalog costs, what the CLAUDE.md chain costs,
      what each mode adds. *Why:* every decision in this project has been argued from estimates. Real
      per-session token data is already in every session `.jsonl` — `cache_creation_input_tokens` and
      `cache_read_input_tokens`. **This is also what un-suspends the circular "not worth it" argument.**
- [ ] **`/mine-conversation`** — have agents read this conversation (and future long ones) and extract
      thoughts, patterns, and possibilities that got dropped. *Why:* this session produced far more
      than survived into the docs; the losses were silent, which is the recurring failure here.
- [ ] Retire `history.md` + disable the `auto_log_history.py` Stop hook *(decided, not yet executed —
      `close-session` still writes it)*.

## Phase 2 — The promotion ladder

- [ ] **`decisions.md` → skill**, farmed by `dream`. Bar: ≥3 occurrences across ≥2 projects; propose,
      never auto-create.
- [ ] **Explore promotion out of native memory**, which currently has only one destination. Candidates:
      → a **skill** · → a **"mode memory"** type · → the **mode `CLAUDE.md` template**, where
      `plan/CLAUDE.md` is the *same file across every project*. *Why this matters:* a rule in the mode
      template applies everywhere that mode is used at zero recall cost, which is strictly better than
      a memory file that must be matched and loaded. **Open question: what earns promotion to a
      template versus staying a per-project memory?**
- [ ] Decide the **memory policy** — what earns a place in a memory file at all. Mechanics are settled;
      the judgment is not. Then change `close-session`, `new-session`, `dream`, and the history hook
      **together** — all four write the same files.

## Phase 3 — Restructure the projects

- [ ] **Fix the 7 dead skill symlinks** from the June reorg. Silent failures; 3 of 4 targets
      recoverable in `~/School/`, `~/Optimal/`, `~/Claude/`. **Prerequisite for any honest measurement.**
- [ ] **Relocate skills out of global** — ~130 load into every session at ~11K tokens. The largest
      controllable context cost found, and the one thing modes are genuinely good for.
      Plan: `skill-relocation-plan.md`.
- [ ] **Re-measure the floor** after pruning. *This is the step that settles the suspended argument —
      do not relocate before measuring, or the baseline is destroyed.*
- [ ] **Restructure all project folders to the mode shape.** Sequence deliberately: fix → prune →
      measure → *then* migrate. Gen 3 tasks map to modes where they fit and stay put where they don't.
- [ ] **Templatize the modes** so every project gets the same `plan/CLAUDE.md`, `research/CLAUDE.md`,
      `make/CLAUDE.md`. Ties into the Phase 2 promotion question.

## Open questions — Carter's call

1. **Why did Gen 2 → Gen 3 happen?** Undocumented anywhere on disk; only Carter knows. Still the best
   evidence for whether Gen 4 is worth it.
2. **File-type skills** (`xlsx`/`docx`/`pptx`/`pdf`, >10% of the catalog) key off *file type*, not
   activity. Placement under a mode structure is genuinely ambiguous.
3. **`reference-notion-multi-workspace-safety.md`** is now unreferenced — delete when ready.

---

## Standing principles for this roadmap

- **A migration that doesn't delete is an addition.** Three generations coexisted because each
  migration was safe, partial, and unfinished, and none signalled that it had stopped.
- **Silence is the failure mode.** Every bug found here reported success and did nothing.
- **Test principles in isolation, then illustrate with real projects — never the reverse.**
