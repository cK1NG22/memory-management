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
- [ ] **`/capture-reference`** — sibling of `capture-feedback`: capture a pointer to an external
      resource (URL, dashboard, doc, tool note) as a `reference-<slug>.md`. The skill owns two
      things: the **file format** (frontmatter with `name`, a one-line `description` that recall
      matches on, `type: reference`) and the **save location** — the native store keyed to the
      current project, *plus* the index line in that store's `MEMORY.md`, since a reference file
      without its index line never autoloads. For a reference that matters to more than one store,
      use the shared-topic-file mechanism (canonical copy + symlink + an index line in each store —
      `mode-memory-design.md`), so it shows up with the other references and tooling notes
      everywhere it applies.
- [ ] **`/context-dashboard`** — show the makeup of the context window given current memory settings:
      what `MEMORY.md` costs, what the global skill catalog costs, what the CLAUDE.md chain costs,
      what each mode adds. *Why:* every decision in this project has been argued from estimates. Real
      per-session token data is already in every session `.jsonl` — `cache_creation_input_tokens` and
      `cache_read_input_tokens`. **This is also what un-suspends the circular "not worth it" argument.**
- [ ] **`/mine-conversation`** — have agents read this conversation (and future long ones) and extract
      thoughts, patterns, and possibilities that got dropped. *Why:* this session produced far more
      than survived into the docs; the losses were silent, which is the recurring failure here.
- [ ] **Shared memory-write reference** (added 2026-08-07, from the skill drift sweep) — one
      canonical file holding the write rules every memory writer follows: the routing test,
      git-root keying, the frontmatter shape, the **mandatory** `MEMORY.md` index line, the
      sectioned-index template, no-unverified-state. Every writer becomes a thin wrapper that
      reads it: `close-session`, `brain-dump`, `capture-feedback`, `/capture-reference` (above),
      `dream`/`morning-shift` (proposal + apply), the `research-deep-dive` agent. *Why:* the sweep
      found the copies have already forked — `capture-feedback` writes top-level `type:` where
      close-session's guide says `metadata.type:`. Copies drift, references can't fork — the mode-
      files mechanism applied to skills. Also turns Phase 2's "change all four writers together"
      into a one-file edit.
- [ ] **`/share-topic`** (added 2026-08-07) — mechanize the shared-topic-file procedure from
      `mode-memory-design.md`: one `ln -s` + one index line per consuming store; removal = links
      first, canonical last; `audit.py` before/after. **Blocked on the four audit.py checks**
      (Phase 2.5). First customer, already queued: link
      `reference-claude-code-loading-mechanics.md` from the `~/Projects` store into this repo's
      store.
- [ ] **Skill-dependency map + retired-token tripwire + the cross-skill change protocol** (added
      2026-08-07). The map is **derived, never hand-drawn** — a hand-maintained map is one more
      copy that drifts. A small script greps `~/.claude/skills/*/SKILL.md` +
      `~/.claude/agents/*.md` for load-bearing tokens (memory paths, formats, skill-to-skill
      references) and emits who-depends-on-what — automating the 2026-08-07 sweep so it can rerun
      any time. `audit.py` gains a **retired-token list** (`history.md`, `mempalace`, the old hub
      path, `task-types/`, exact-cwd keying wording): any skill or agent still carrying a retired
      convention fails the audit loudly instead of drifting silently. **The protocol for any
      change that touches a shared convention:** (1) name the convention changing, (2) generate
      the map to list dependents, (3) change every dependent in one change set — a convention
      change that doesn't update all its dependents is a fork, not a change, (4) add the old
      token to the retired list so stragglers surface. Protocol text lives beside the shared
      write reference. `claude-audit` gains a memory section that runs `audit.py` (incl. the
      imports check) so "audit my setup" covers memory wiring.
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
      transcript items folded to project level per the session-launch convention (sessions open at
      `<container>/`, `<project>/`, or `<project>/<mode>/` — never deeper). Standing tools: `make/memory-repair/`
      `transcript_sweep.py` + `transcript_consolidate.py`; procedure:
      `docs/transcript-housekeeping-runbook.md`.
- [x] **Consolidate the container stores** — **done 2026-08-06** (all four tranches; 65 moves,
      3 deletes, 12 new stores, audit exit 0 at 37 stores / 264 topics). Per-file record + ASK
      rulings + lessons: the manifest's "Execution record" section. Original scope:
      (`~/Projects` 135 topics, `~/Optimal`, `~/Sandbox`,
      `~/Sandbox/builds`, `~/Vault`, `~/Research`) — a **placement** migration: container stores
      stay live under the launch convention, but one store loads per session, so project-specific
      facts filed at container level never load in the project sessions that need them. Full
      per-file proposal: `container-consolidation-manifest.md` (54 mechanical routes, 91 global
      files stay as `~/Projects`' reference library). Use the memory-repair runbook flow
      (dump/route/mkindex, explicit manifests, `LEFT 0`); **capture the process** for the dream
      ladder. Awaiting Carter's rulings.
- [ ] **Review how worktree memory gets promoted** (Carter, 2026-08-06). Two layers, only one
      understood: (a) *project* memory (`.claude/memory/`) edited in a worktree is git-tracked and
      merges back with the branch — the current handoff pattern, working but dependent on sessions
      committing; (b) the *native* store of a worktree session — each worktree is its own git
      toplevel, so it keys its own ephemeral store, and anything saved there is silently orphaned
      when the worktree is deleted. No promotion path exists; the mode-memory design deliberately
      deferred it ("revisit only if a worktree session ever saves a memory worth keeping").
      Worktree sessions are now routine (background jobs, night shifts), so decide: promote on
      merge? forbid native saves in worktrees? a sweep tool? Fold into the transcript-housekeeping
      cadence?
- [ ] **Build the four `audit.py` checks** from `mode-memory-design.md` (stranded repo-subdir
      stores, lstat-level symlink resolution, containment invariant, fork tripwire) — required
      before any memory symlink is created.
- [ ] **Correction sweep for git-root keying wording** — still stating exact-cwd keying: the root
      `CLAUDE.md` two-system table, `docs/memory-repair-runbook.md`, `audit.py`'s orphan message,
      and the close-session skill's Phase-5 native-memory text.
- [ ] **Update `close-session` + `new-session` skills to the new memory patterns** (Carter,
      2026-08-06). close-session Phase 5: replace "keyed to the exact working directory / does not
      walk up" with git-root keying + the one-store-per-session rule; route native facts to the
      repo-root store. new-session: codify the worktree case (handoff written and committed on the
      branch) and set the launch dir per the session-launch convention — **project root or the
      mode folder that fits the next action** (`<project>/` or `<project>/<mode>/`), never a
      deeper path — and drop any exact-cwd assumptions. Both live in `~/.claude/skills/` — outside this repo, so it's a hand edit, not
      part of a branch merge.
- [ ] **Skill drift fixes — 2026-08-07 sweep** (all hand edits in `~/.claude/skills/` +
      `~/.claude/agents/`; do together with, or right after, the close-session/new-session item
      above — ideally as thin wrappers over the shared memory-write reference, Phase 1).
      **close-session** additionally: drop the mempalace phase (ruled dead), the hardcoded
      `-Users-carterking-Projects` Phase-1 scan, and the task-type feedback step; add the
      **worktree guard** — in a worktree, write project memory + handoff only, never the native
      store (worktree stores orphan on deletion), and end with ExitWorktree "keep."
      **brain-dump**: route to the session's git-root store instead of the hardcoded `~/Projects`
      store (today every in-project dump misfiles into the library), canonical frontmatter, index
      line mandatory. **capture-feedback**: rule-shaped feedback routes to `ALWAYS.md` /
      `<MODE>-MODE.md` per the tiering (CLAUDE.mds explain and navigate; memory remembers);
      align frontmatter; drop the Gen 3 task-type bootstrap. **memory-review**: review the store
      for the cwd — 37 stores exist, it knows one — and the sectioned-index template.
      **memory-janitor agent**: run `audit.py` across all stores instead of hardcoding one.
      **research-deep-dive agent**: route the memory write to the store the research belongs to.
      **dream + morning-shift**: bake the write conventions into proposal + apply **before
      roadmap 4.4 flips writes on**. **opusplan**: plans save to `plan/` (present-tense home),
      never "the memory directory" — fix when it moves to the plan mode home (phase3.md).
      Clean, no action: day/night-shift, save-summary, file-versioning, skill-creator, learn
      (separate gstack system by design).

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
      Plan and full inventory: `phase3.md`.
- [ ] **Trim skill frontmatter to the gstack shape** (Carter, 2026-08-07). The 53 gstack skills
      cost only ~1.1K tokens because each `description:` is one terse line (~20 tokens); the ~43
      non-gstack global skills carry the rest of the catalog (~120+ tokens each — long
      trigger-phrase lists are the bulk). Review each against the gstack shape. Trim fat, not
      signal: the description is what makes a skill fire, so keep the trigger phrases that earn
      their keep. Same lever as relocation, no files move. **This is the fix for a live
      triggering bug** (root-caused 2026-08-07, `research/sources/skill-description-drop.md`):
      the skills listing has a **budget** (~1% of context window) and least-used skills
      silently lose their descriptions when it overflows — measured live 2026-08-07:
      35,948 chars vs a 30,000 budget on the default model (only ~8K for 200K-context
      models), so ~16 skills are name-only per session (`sources-cited`, `tdd`,
      `sync-gbrain`, `ponytail:*`, …) and cannot natural-language trigger. The budget is
      aggregate: every verbose description evicts someone else's. Meters: `/doctor` before and
      after; `/skills` shows per-skill state. Optional second lever:
      `skillListingBudgetFraction` in settings (costs context in every session).
- [ ] **Re-measure the floor** after pruning. **Baseline captured 2026-08-05 (before relocating):
      44K–55K tokens at session start across eight recent sessions**, from the `.jsonl` token data.
      The post-relocation number comes free from the next normal session start.
- [ ] **Restructure all project folders to the mode shape.** Sequence deliberately: fix → prune →
      measure → *then* migrate. Gen 3 tasks map to modes where they fit and stay put where they don't.
- [ ] **Rewrite `restructure-project` + `new-project` to Gen 4 before the stamping starts** (added
      2026-08-07). `restructure-project` still scaffolds `history.md` (retired 2026-08-05) and the
      full Gen 3 COS shape (PROJECT.md/TASK.md/task-types); `new-project` assumes the same
      container shape. Rewrite `restructure-project` in place as the Gen 4 mode stamper (mode
      CLAUDE.mds + symlinks + `git init` + the store-keying pre-flight — the runbook's step 5), or
      park it until then. Leaving it live while Phase 3 rolls out scaffolds the previous
      generation in parallel — the exact "three generations coexisted" failure this roadmap's
      standing principles name.
- [ ] **`git init` every project folder as part of the mode migration** (Carter, 2026-08-06). A
      non-repo project fragments native memory: every mode-folder launch keys its own store
      (exact-cwd keying), so `plan/` and `make/` sessions each get a separate empty store — the
      June accident, re-run per project. A repo converges every inside-the-project session onto one
      root store. **Containers must stay non-repos** — a repo at `~/Projects` would swallow every
      non-repo project under it into one store. Pre-flight per project: check for existing stores
      keyed to its *subfolders* — creating a repo above such a store strands it retroactively
      (audit check #1's inverse). `attio-network-database` verified safe 2026-08-06 (it is its own
      repo). Note `git init` does **not** protect against folder moves — the store keys to the
      encoded absolute root path either way; `audit.py` before/after any move stays mandatory.
      Currently non-repo (from the manifest's destination check): dad, hoth, loops, ai-engineering,
      neon-learning, health-insurance, outreach, mana-ventures, custom-agents.
- [x] **Build the mode files + mode `CLAUDE.md` templates** — **done 2026-08-06** for the files
      + this project's wiring (sentinel test overturned the home-path import; delivery is an
      in-project symlink + `@import`, see `docs/mode-files-runbook.md`; stamping the other
      projects rides the restructure item above). Original decision: **DECIDED (Carter,
      2026-08-06): single-source, referenced.** Mode principles live once at
      `~/.claude/modes/RESEARCH-MODE.md` / `PLAN-MODE.md` / `MAKE-MODE.md` (same home as the
      per-mode skills below — a mode's instructions and tooling side by side). Each project's mode
      `CLAUDE.md` stays a thin faux system prompt (which mode + directions) plus one
      `@~/.claude/modes/<MODE>-MODE.md` import — editing the mode file changes every project at
      once, which is the point. `ALWAYS.md` (every-mode rules, imported from `~/.claude/CLAUDE.md`)
      **approved (Carter, 2026-08-06), contingent on the `@import` sentinel test** — which must
      also check what a *missing* import target does (silent or loud; silent = E5 in new
      clothing → needs an audit check). Content seeds: the 36 mode-principle memories fold in per the
      manifest's Tranche 4 (then delete); this project's three mode CLAUDE.mds are the first
      drafts. **Sentinel-test the home-path `@import` first** (cheap pre-flight).
      **CLAUDE.md-vs-memory tiering (Carter, 2026-08-06): CLAUDE.mds explain and navigate; memory
      remembers.** Container CLAUDE.md: what the container is + the project folders below ·
      Project: what the project is + how to navigate its modes · Mode: the directions.
      Container memory: what explains the container + future project ideas · Project memory:
      that project's progress and decisions · Mode sections of project memory: that mode's work
      in that project + a pointer to the mode file, with general lessons **promoted up** into the
      mode file (routing test: project-specific → MEMORY.md; mode principle → `<MODE>-MODE.md`).
- [ ] **Auto-symlink each mode's skills into `<project>/<mode>/.claude/skills/`** at scaffold time,
      so entering a mode loads that mode's tools and nothing else. This is the mechanism the whole
      mode structure was approved for — without it modes carry instructions but no tooling, and the
      global catalog still loads everywhere regardless. Depends on the relocation step above: the
      skills must live outside `~/.claude/skills/` before there is anything to link.
      **Shape decided 2026-08-05:** one **folder-level** symlink per mode per project
      (`<mode>/.claude/skills → ~/.claude/modes/<mode>/skills`), per-skill links only inside the
      mode home — so adding a skill to a mode reaches every project without rescaffolding.
      **Sentinel-tested ✓ 2026-08-07:** a symlinked parent `skills/` folder loads fully (names,
      descriptions, natural triggering) — `research/sources/skill-description-drop.md`.
      **Symlinks are the known-fragile part** — 12 died silently in the June reorg — so this needs a
      resolve-check plus a load-twice check (one loading location per skill), and
      `/move-project --check` is where both belong. Per-mode assignments: `phase3.md`.

## Phase 3.5 — Automations

- [ ] **Create the automations project** (Carter's idea, endorsed 2026-08-05) — one workspace for
      the cron jobs, with `WorkingDirectory` pinned in each plist so the cron-locked skills can
      leave global too. Dream stays with memory-management (its rules are memory policy — the
      colocate principle). Details: `phase3.md`.
- [ ] **Shifts under the mode structure** — Carter's direction: execution lands in the relevant
      project's `make/`, possibly `make/shift-work/`; the foreman stays cross-project. Resolve
      when the mode rollout reaches the projects the shifts touch.

## Open questions — Carter's call

1. **Why did Gen 2 → Gen 3 happen?** Undocumented anywhere on disk; only Carter knows. Still the best
   evidence for whether Gen 4 is worth it.
2. **File-type skills** (`xlsx`/`docx`/`pptx`/`pdf`, >10% of the catalog) key off *file type*, not
   activity. Placement under a mode structure is genuinely ambiguous.
3. ~~`reference-notion-multi-workspace-safety.md`~~ — deleted 2026-08-06 (Tranche 2).

---

## Standing principles for this roadmap

- **A migration that doesn't delete is an addition.** Three generations coexisted because each
  migration was safe, partial, and unfinished, and none signalled that it had stopped.
- **Silence is the failure mode.** Every bug found here reported success and did nothing.
- **Test principles in isolation, then illustrate with real projects — never the reverse.**
