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
- [x] **"Mode memory" explored and resolved — 2026-08-06.** Native memory is keyed to the **git
      root** on Claude Code 2.1.223 (sentinel-tested), so the modes of a repo project already share
      one store; no mode-memory layer gets built. The one adopted mechanism is the **shared topic
      file** (canonical copy + file symlink + per-store index line). Design and required `audit.py`
      checks: `mode-memory-design.md`; experiments:
      `../research/sources/native-memory-keying-and-symlink-experiments.md`.
- [ ] **Explore promotion out of native memory**, which currently has only one destination. Candidates:
      → a **skill** · → the **mode `CLAUDE.md` template**, where
      `plan/CLAUDE.md` is the *same file across every project*. *Why this matters:* a rule in the mode
      template applies everywhere that mode is used at zero recall cost, which is strictly better than
      a memory file that must be matched and loaded. **Open question: what earns promotion to a
      template versus staying a per-project memory?**
- [ ] Decide the **memory policy** — what earns a place in a memory file at all. Mechanics are settled;
      the judgment is not. Then change `close-session`, `new-session`, `dream`, and the history hook
      **together** — all four write the same files.

## Phase 2.5 — Memory consolidation & correction sweep (added 2026-08-06)

- [x] **Transcript housekeeping** — done 2026-08-06. 46 dead-path dirs (294 MB) archived, 83 deep
      transcript items folded to project level per the new session-launch convention (sessions open
      only at `<project>/` or `<project>/<mode>/`). Standing tools: `make/memory-repair/`
      `transcript_sweep.py` + `transcript_consolidate.py`; procedure:
      `docs/transcript-housekeeping-runbook.md`.
- [ ] **Consolidate the container stores** (`~/Projects` 135 topics, `~/Sandbox`, `~/Clients/…`,
      home, `/`) into project-level stores — under the session-launch convention these stores
      rarely load, so their ~200 memories are going dormant. Use the memory-repair runbook flow
      (dump/route/mkindex, explicit manifests, `LEFT 0`); **capture the process** for the dream
      ladder. Planned with Carter for the next session.
- [ ] **Build the four `audit.py` checks** from `mode-memory-design.md` (stranded repo-subdir
      stores, lstat-level symlink resolution, containment invariant, fork tripwire) — required
      before any memory symlink is created.
- [ ] **Correction sweep for git-root keying wording** — still stating exact-cwd keying: the root
      `CLAUDE.md` two-system table, `docs/memory-repair-runbook.md`, `audit.py`'s orphan message,
      and the close-session skill's Phase-5 native-memory text.

## Phase 3 — Restructure the projects

- [x] **Fix the dead skill symlinks** from the June reorg. Done 2026-08-05. The live count was **12,
      not 7** — the tally had drifted since it was taken. 11 re-pointed to their post-reorg homes
      (`~/School/strat-411-skills/`, `~/Optimal/optimal-claude-skills/` + its `skill-factory/`,
      `~/Claude/skill-factory/`); 1 removed (`qa-design-review` — its target no longer exists
      anywhere on disk; the gstack repo dropped it upstream). Verified: zero dead links remain.
- [ ] **Relocate skills out of global** — measured 2026-08-05: **113 skills at ~7.8K tokens** per
      session (the ~130/~11K figure was an estimate; this is from the files). **Tranche 1 done:**
      the 11 project-scoped symlinks moved to `~/School/.claude/skills/` and
      `~/Optimal/.claude/skills/` — global is now 102 skills, ~1,440 tokens lighter everywhere.
      Remaining tranches are Carter's call (physical moves + the gstack question).
      Plan and full inventory: `skill-relocation-plan.md`.
- [ ] **Re-measure the floor** after pruning. **Baseline captured 2026-08-05 (before relocating):
      44K–55K tokens at session start across eight recent sessions**, from the `.jsonl` token data.
      The post-relocation number comes free from the next normal session start.
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
      **Shape decided 2026-08-05:** one **folder-level** symlink per mode per project
      (`<mode>/.claude/skills → ~/.claude/modes/<mode>/skills`), per-skill links only inside the
      mode home — so adding a skill to a mode reaches every project without rescaffolding.
      **Sentinel-test first:** a symlinked parent `skills/` folder loading is unverified.
      **Symlinks are the known-fragile part** — 12 died silently in the June reorg — so this needs a
      resolve-check plus a load-twice check (one loading location per skill), and
      `/move-project --check` is where both belong. Per-mode assignments: `skill-relocation-plan.md`.

## Phase 3.5 — Automations

- [ ] **Create the automations project** (Carter's idea, endorsed 2026-08-05) — one workspace for
      the cron jobs, with `WorkingDirectory` pinned in each plist so the cron-locked skills can
      leave global too. Dream stays with memory-management (its rules are memory policy — the
      colocate principle). Details: `skill-relocation-plan.md`.
- [ ] **Shifts under the mode structure** — Carter's direction: execution lands in the relevant
      project's `make/`, possibly `make/shift-work/`; the foreman stays cross-project. Resolve
      when the mode rollout reaches the projects the shifts touch.

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
