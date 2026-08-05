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
- [x] **Resolve every orphaned memory store** — 165 topic files across 16 stores keyed to directories
      that no longer exist. **139 routed** to live stores, **17 moved out of the memory system**
      entirely (Locker's build plans were never memories), **9 deleted**. **Cleanup is now finished:**
      22 live stores, 308 topic files, 0 dangling links, every store resolving to a real directory.
- [x] **Write the repair down so it never has to be re-derived** — `docs/memory-repair-runbook.md`
      (the 8-step procedure + the judgment rules + the shell gotchas) and `make/memory-repair/`
      (`audit.py`, `dump.py`, `route.py`, `mkindex.py`). **`audit.py` is the durable half:** no args,
      exit 1 when dirty, run it before and after moving any folder.

---

## Phase 1 — Build the skills this work identified

- [ ] **`/move-project`** — relocate a project *and* everything path-coupled to it: the cwd-keyed
      native store, symlinks in both directions, ~23 config references, worktrees holding absolute
      paths. **A `--check` audit mode is the more valuable half** — it would have caught the June
      damage before it compounded. Spec: `[[project-move-project-skill-idea]]`.
      **Half of this already exists:** `docs/memory-repair-runbook.md` is the written procedure, and
      `make/memory-repair/audit.py` is `--check` for the memory half (runs with no args, exit 1 when
      dirty). What `/move-project` adds is *doing the move* and covering symlinks + config references.
- [ ] **`/context-dashboard`** — show the makeup of the context window given current memory settings:
      what `MEMORY.md` costs, what the global skill catalog costs, what the CLAUDE.md chain costs,
      what each mode adds. *Why:* every decision in this project has been argued from estimates. Real
      per-session token data is already in every session `.jsonl` — `cache_creation_input_tokens` and
      `cache_read_input_tokens`. **This is also what un-suspends the circular "not worth it" argument.**
- [ ] **`/mine-conversation`** — have agents read this conversation (and future long ones) and extract
      thoughts, patterns, and possibilities that got dropped. *Why:* this session produced far more
      than survived into the docs; the losses were silent, which is the recurring failure here.
- [x] **Retire `history.md` + the `auto_log_history.py` Stop hook.** Done 2026-08-05. The Stop hook
      is unwired from `~/.claude/settings.json` and archived (with its test) to
      `~/.claude/hooks/_archive/`; `close-session` no longer appends it; `new-session` Phase 4 is
      tombstoned; **`memory_migrate.py` — a fourth writer the original count missed — no longer
      scaffolds or seeds it.** Existing `history.md` files are inert; leave them. Takes effect for
      hooks at the next session start.

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
- [ ] **Build the mode `CLAUDE.md` templates** — one canonical `research/`, `plan/`, and `make/`
      instruction file, stored once and used by the new-project skill at scaffold time. The three in
      *this* project are the first drafts and the only copies that exist. **Decide the update model
      before writing them:** a copied template drifts per project and can never be fixed centrally;
      a symlinked or `@import`-ed one stays live but means editing it changes every project at once.
      Ties directly into the Phase 2 promotion question — the template *is* the top rung of that ladder.
- [ ] **Auto-symlink each mode's skills into `<project>/<mode>/.claude/skills/`** at scaffold time,
      so entering a mode loads that mode's tools and nothing else. This is the mechanism the whole
      mode structure was approved for — without it modes carry instructions but no tooling, and the
      global catalog still loads everywhere regardless. Depends on the relocation step above: the
      skills must live outside `~/.claude/skills/` before there is anything to link.
      **Symlinks are the known-fragile part** — 7 died silently in the June reorg — so this needs a
      resolve-check, and `/move-project --check` is where that check belongs.

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
