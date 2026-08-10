# Context — memory-management

**Last updated:** 2026-08-10 (session 6, bg — A/B verdict folded in: FALSIFIED on the metric,
mechanism intact; trim confirmed executed; collision correction)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**Phase 3 is approved, its gate is passed, and its first two execution items are done.** Carter
approved `plan/phase3.md` — Plan A: move the last 15 skills to mode homes; Plan B: restamp every
project to the mode shape; order: sentinel test → B → A → re-measure.

**The root cause (2026-08-07):** the skills listing has a **budget** (~1% of the model's context
window). When the catalog overflows it, the least-used skills silently lose their `description:`
and can no longer natural-language trigger — names always load, descriptions are rationed. Symlinks
were never the problem. Full reference: `research/sources/skill-description-drop.md`.

**The A/B ran 2026-08-08 and came back FALSIFIED — on the metric, not the mechanism.** Baseline
75%, subtraction 100%, delta 25pp against a 60pp bar. Only 1 of 4 targets
(`youtube-slide-transcript`) was actually evicted going in; for that one the restoration was a
clean 0% → 100% on all 5 probes. The other three had drifted back into budget on their own since
the 08-07 pass — the plan's own falsifier clause firing as written. **What stays unconfirmed is the
aggregate claim** (does trimming fix the multi-skill problem), not the mechanism. Per the plan: do
not justify further trim/relocation work on this result alone. Second measurement, sonnet probe
model: 119 skills + 4 plugins = 31,362 chars vs an **8,000-char budget** → 23,362 deficit. Combined
with the 08-07 figure (35,948 vs 30,000, default model), the lesson is that **the evicted set moves
with the model**, not just with usage drift.

**The trim executed and is partly done.** 11 skills now carry `disable-model-invocation: true`
(`autoresearch`, `claude-audit`, `close-session`, `fable-plan`, `kpi-setter`, `memory-review`,
`new-project`, `new-session`, `resolve-vulns`, `restructure-project`, `youtube-slide-transcript`).
The `opusplan` → `fable-plan` rename rider landed. Global is **101 skills**. Not yet done: the ~19
model-invoked descriptions still awaiting their 80–200-char trim, and the `capture-feedback`
content rider.

**The trim/A-B collision flagged on 08-08 never actually landed.** Timestamps settle it: A/B results
committed 12:47, trim flips 12:58, `tdd` archive 13:45. Every probe ran on a clean catalog. The
warning was right to send — the two plans genuinely share `~/.claude/` state, which worktrees cannot
isolate — but the ordering held by luck, not design.

**Tooling (08-08):** `mattpocock-skills@mattpocock` installed as a plugin (25 skills incl.
`writing-for-agents`, ~1,620 tok always-on; managed like gstack, outside Plan A). Dedup sweep found
one live exact-name duplicate — local `tdd`, archived to `~/Claude/_archive/tdd-skill_2026-08-08`
per Carter's managed-over-local ruling.

## ⏭️ Next steps / open

1. ⚠️ **Four unmerged worktree branches are stacked up** — `worktree-skill-budget-execution` (the
   A/B results, the only copy), `worktree-close-session-plugin-dedup` (sessions 5–6),
   `worktree-todo-capture-reference`, `worktree-phase3-plan`. Merging them is Carter's call; the
   A/B research file exists nowhere else.
2. **Finish the trim:** the ~19 model-invoked descriptions → 80–200 chars, plus the
   `capture-feedback` Gen 4 memory-routing rider. `/doctor` before/after is the authoritative meter.
3. **Decide what replaces the falsified A/B as evidence for the aggregate claim** — the honest
   options are a re-run with targets verified evicted *at probe time*, or accepting the mechanism
   as proven and treating the aggregate as unmeasured. Do not silently drop it.
4. **Plan B — restamp the projects** (git init the 9 non-repos + wire mode CLAUDE.mds/symlinks,
   probe each; runbook step 5), then remove `# Planning a build` from the global CLAUDE.md.
5. **Plan A — move the 15 mode-home skills** (after B), then re-measure the floor (free).
6. ⚠️ **Stale since 2026-08-06 (~6 sessions, no movement):** the correction sweep (exact-cwd
   wording in root CLAUDE.md table, memory-repair runbook, audit.py orphan message) + the
   close-session/new-session **skill-content** updates (worktree exit step, git-root keying).
   Session 6 note: close-session again hand-skipped its dead mempalace phase and its stale
   "PENDING UPDATE" banner. Third consecutive session paying this tax.
7. Carried: worktree memory promotion review · four audit.py checks (gate `/share-topic`) ·
   floor re-measure.

## 🧠 Recent decisions

See `decisions.md` (entries 2026-08-07 → 2026-08-10). Load-bearing:

- **A/B FALSIFIED on the metric, mechanism intact** — one real eviction swung 0% → 100%; three
  targets weren't evicted going in. The aggregate claim is unmeasured, not disproven.
- **Invocation split (Carter): zero-bare rejected.** Model-invoked skills earn descriptions;
  user-invoked skills go absent via `disable-model-invocation`; name-only is for skill-to-skill
  reach. close/new-session → user-invoked; cron/shift family → model-invoked.
- **Duplicated skills resolve to the managed plugin copy** (Carter's ruling, `tdd` case).
- **Phase 3 approved as written** — sentinel → B → A; the two ❓ calls (file-type four,
  resolve-vulns) stay open.

## 💡 What we learned

- **A metric can falsify while the mechanism holds.** The A/B's success bar was aggregate across
  four targets; three of them weren't exhibiting the effect. Verify the effect is *present* before
  measuring how well you can remove it.
- **The evicted set moves with the model, not just with usage.** Budget is a fraction of the
  model's context window — 30,000 chars on one, 8,000 on another. A "which skills are bare" answer
  is only valid for the model that produced it.
- **The description budget is aggregate — a commons.** Every verbose description evicts some other
  skill's triggering. gstack's terseness is what keeps the catalog alive.
- **Probabilistic failures get blamed on the model.** The evicted set varies per session, so broken
  triggering read as "model mood" for months. Deterministic bugs get found.
- **Forensics: compare against the result timestamp, not the write timestamp.** The 08-08 collision
  looked fatal from file mtimes alone; the A/B's commit time showed it had already finished.
- **Usage telemetry decides visibility** (`~/.claude/skill-usage.json` ranks eviction) — new skills
  start last in line exactly when discovery matters most.
- **A description is a context pointer** (writing-for-agents): pay for it only where the agent must
  discover the skill; where the human is the index, spend cognitive load instead.

## 📂 Files touched · 🌿 git

`main` is at `cae0e21` (session 4's close). **Nothing from sessions 5–6 is merged.**

Session 6 (branch `worktree-close-session-plugin-dedup`, commits `5310499`, `f471c5d`, + this
close): `plan/ROADMAP.md` (A/B verdict item added; trim status corrected to "executed") ·
`decisions.md` (4 entries) · this file. Native store: no new files this session.

Session 5 (same branch): `decisions.md` · `context.md` · mattpocock plugin installed (user
settings) · local `tdd` → `~/Claude/_archive/tdd-skill_2026-08-08` · native store
`reference-writing-for-agents.md` updated + `feedback-prefer-managed-plugin-skills.md` new.

Elsewhere, unmerged: `worktree-skill-budget-execution` (`25f962a`) holds the A/B results in
`research/sources/skill-description-drop.md` — **the only copy** ·
`worktree-todo-capture-reference` (`46f7cc4`) · `worktree-phase3-plan` (at main).
Outside the repo: baseline tar `~/Claude/_archive/skill-trim_2026-08-07.tar.gz`; A/B fixture at
`~/Sandbox/skill-budget-ab-fixture/`.
