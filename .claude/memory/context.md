# Context — memory-management

**Last updated:** 2026-08-08 (session 5 — both execution plans run; the trim landed; §4 gate open)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**The skill-listing budget bug is fixed on disk.** Session 5 ran both approved plans in `make/`
mode, subagent-driven (fresh implementer → task review → fix loop → final whole-work review).

- **`plan/skill-budget-ab.md` — run, verdict FALSIFIED, gate adjudicated PROCEED.** The 25pp
  restoration delta missed the pre-registered ≥60pp bar for a reason unrelated to the hypothesis:
  3 of 4 probe targets were never evicted at baseline, making the aggregate bar arithmetically
  unreachable. The one genuinely-evicted target swung 0/5 → 5/5. Reasoning is in the SDD ledger,
  not buried. Results appended to `research/sources/skill-description-drop.md`.
- **`plan/trim-skills.md` — executed through §4.** Non-gstack listing catalog **18,440 → 8,086
  chars** (goal <9K). Bare-name probe **`114,16` → `128,1`** ×3 identical; the single remaining
  bare name is `sources-cited`, bare by design. The over-budget WARN is **gone entirely**. 12
  skills flipped to `disable-model-invocation: true` (all probed ABSENT); decoy control clean.
  Riders shipped: `opusplan` → `fable-plan`; `capture-feedback` rerouted to Gen-4 destinations.
- **Final whole-work review: CLEAN.** All change classes spot-verified against the pre-edit tar
  `~/Claude/_archive/skill-trim_2026-08-08.tar.gz`; verification arithmetic independently
  recomputed exact; every deferred minor triaged RIDE.

**`/doctor` ran after** and its cleanup was applied per Carter ("keep React Bits, clean up
everything else"): 3 MCP servers disabled for this project, `modern-web-guidance@googlechrome`
off, duplicated Worktrees bullet removed from the global `CLAUDE.md`.

## ⏭️ Next steps / open

1. **⛔ Carter's §4 stop-gate ruling** — `trim-diff.md` (verbatim old/new + char counts for all 11
   trims) lives in the kept worktree at
   `.claude/worktrees/skill-budget-execution/.superpowers/sdd/trim-skills/`. Standing
   recommendation: **stop at the top 10** — the <9K target is met, further trimming buys nothing.
2. **Merge `worktree-skill-budget-execution`** (commit `25f962a`, unmerged) and fold its
   transcript before the worktree is ever deleted. The workspace is deliberately kept: the skill
   edits landed outside the repo and have **no git record** — that workspace *is* the record.
3. **Update `plan/ROADMAP.md` line 187** — the "Trim skill frontmatter to the gstack shape" item
   is now done. *Not edited this session:* `make/` mode forbids writing to `../plan/`. Needs a
   `plan/` session or Carter's hand.
4. **Fold the pending revisions into `close-session` + `new-session` skills** — worktree-exit
   phase, git-root store keying, **and two newly-found staleness bugs**: Phase 3.7 still routes
   durable feedback to the retired `~/.claude/task-types/` scheme, and the mempalace phase
   contradicts the standing `feedback-no-mempalace` memory (MCP now disabled).
5. ⚠️ **Stale since 2026-08-06 (~5 sessions, no movement):** the correction sweep — exact-cwd
   wording in the root `CLAUDE.md` table, the memory-repair runbook, the `audit.py` orphan
   message. The `capture-feedback` half of this item was cleared as a trim rider; the rest sat.
6. **Phase 3 Plan B** — restamp the projects (git init the 9 non-repos + wire mode
   CLAUDE.mds/symlinks, probe each), then remove `# Planning a build` from the global CLAUDE.md.
   **Plan A** — move the 15 mode-home skills (after B), then re-measure the floor (free).
7. Carried: worktree memory promotion review · four `audit.py` checks (gate `/share-topic`) ·
   optional pruning of 4 zero-use inline plugins · optional removal of the claude.ai Gmail +
   Calendar connectors (`google_workspace` covers both).

## 🧠 Recent decisions

See `decisions.md` (entry 2026-08-08 "Both execution plans run"). Load-bearing:

- **A falsified verdict can still be a PROCEED** when the failure is a *precondition* failure, not
  a mechanism failure — but the reasoning gets written down, never quietly waved through.
- **The parallel-session contamination alarm was rejected on evidence, not paused on caution** —
  the A/B had banked and committed all 10 probes before the first flip landed.
- **Permission laundering refused:** a denial in one agent is never authorization for another.
  `rm -r ~/.claude/skills/opusplan` went to Carter as a manual step.

## 💡 What we learned

- **An eviction experiment must verify its targets are actually evicted at baseline.** Otherwise
  the arm measures nothing and reports failure — which is exactly what happened here.
- **Probe readings carry timestamp evidence.** ABSENT vs NAME-ONLY vs described distinguishes
  *which* mutation had landed when a session read the catalog. Deliberately leaving
  probe-distinguishable states is what let a false conflict alarm be disproven from data.
- **Worktrees isolate the repo, not the machine.** `~/.claude/skills/`, `settings.json`, and
  `skill-usage.json` are shared mutable state across every parallel session. Sequencing
  (measurement completes before mutation starts) and single ownership are the only protections.
- **Edit the generated file *and* its template.** The `learn` skill's `.tmpl` source would have
  silently reverted the flip on the next regen — this project's signature failure class.
- **`/usr/bin/diff -u` for frontmatter reviews** — the default diff tool renders YAML
  folded-block (`>`) changes as whole-file rewrites, which reads as "the agent rewrote everything."
- **A skill that reroutes other people's writes can be stale about its own.** Running
  `close-session` surfaced that its Phase 3.7 still writes to the very Gen-3 folder scheme this
  session removed from `capture-feedback`.

## 📂 Files touched · 🌿 git

Repo: one commit `25f962a` on branch **`worktree-skill-budget-execution`** (unmerged) —
`research/sources/skill-description-drop.md` (A/B results). Worktree **kept** on disk; SDD
workspace under `.superpowers/sdd/{skill-budget-ab,trim-skills}/` holds the ledgers, briefs,
reports, `trim-diff.md`, and `task-5-verification.md`. This close-session wrote `decisions.md` +
this file directly on `main`.

Outside the repo (no git record — the workspace is the record): pre-edit tar
`~/Claude/_archive/skill-trim_2026-08-08.tar.gz` (97 files, `tar czhf` to dereference symlinks) ·
11 trimmed + 12 flipped SKILL.md files under `~/.claude/skills/` and `~/.agents/skills/` ·
`~/.claude/skills/fable-plan/` (new; `opusplan/` deleted by Carter) · `~/.claude/settings.json`
(`skillOverrides: {"sources-cited": "name-only"}`, plugin disable) · `~/.claude.json` (per-project
MCP disables) · `~/.claude/CLAUDE.md` (dedup). Native store:
`reference-global-state-parallel-sessions.md` (new) + MEMORY.md pointer. A/B fixture
`~/Sandbox/skill-budget-ab-fixture/` cleaned up.
