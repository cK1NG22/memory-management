# Context — memory-management

**Last updated:** 2026-08-08 (session 4 — Phase 3 approved; skill-budget root cause; both execution plans ready)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**Phase 3 is APPROVED and its gate is passed.** Carter approved `plan/phase3.md` (renamed from
`skill-relocation-plan.md`) — Plan A: move the last 15 skills to mode homes; Plan B: restamp every
project to the mode shape; order: sentinel test → B → A → re-measure.

**The sentinel test detoured into the session's big find.** Names loaded through skill symlinks but
descriptions didn't — four research agents (docs / GitHub / community / **binary forensics**) plus
fixture experiments root-caused it: **the skills listing has a budget** (~1% of the model's context
window; least-used skills silently lose descriptions; a name-only skill can't natural-language
trigger). Symlinks were never the problem — the two-hop mode chain loads fully; the gate closed as
PASSED. Full reference: `research/sources/skill-description-drop.md`. Live numbers: 130 skills,
35,948 chars vs 30,000 budget on the default model (~8K budget for 200K-context models); ~16
skills bare per session, set varies by session and model.

**Two execution-ready plans await Carter's `make/` session** (both reviewed, on main):

- `plan/skill-budget-ab.md` — A/B confirming "smaller catalog → descriptions return"
  (subtraction arm via project-scoped `skillOverrides`; 5 decoy-controlled probes/arm; ≥60pp
  restoration delta; <$1). **Run this first.**
- `plan/trim-skills.md` — the trim pass, reshaped by Carter's **invocation split** ruling (from
  mattpocock/skills `writing-for-agents`): **zero bare names was the wrong goal.** 12 skills FLIP
  to user-invoked via `disable-model-invocation: true` (probe-verified ABSENT; incl.
  close-session + new-session per Carter), `sources-cited` goes deliberate name-only (411-case
  reaches it by exact name), ~19 stay model-invoked and trim to 80–200 chars, cron/shift family
  ruled model-invoked. Baselines banked: 47 non-gstack skills / 18,440 chars; probe 114
  described / 16 bare; backup tar in `~/Claude/_archive/`. Riders: `opusplan` → `fable-plan`
  (rename + invoke Fable), `capture-feedback` content update to Gen 4 memory routing.

**A parallel session added ROADMAP items** (2026-08-07/08, not this session's work): the
`/capture-reference` skill, the shared memory-write reference, `/share-topic`, and the
skill-dependency map + retired-token tripwire + change protocol.

## ⏭️ Next steps / open

1. **Carter opens a `make/` session:** run the A/B (`plan/skill-budget-ab.md`), then the trim pass
   (`plan/trim-skills.md` — flips + trims + riders, stop after top 10 for his diff review).
   `/doctor` before/after is the authoritative meter.
2. **Plan B — restamp the projects** (git init the 9 non-repos + wire mode CLAUDE.mds/symlinks,
   probe each; runbook step 5), then remove `# Planning a build` from the global CLAUDE.md.
3. **Plan A — move the 15 mode-home skills** (after B), then re-measure the floor (free).
4. ⚠️ **Stale since 2026-08-06 (~4 sessions, no movement):** the correction sweep (exact-cwd
   wording in root CLAUDE.md table, memory-repair runbook, audit.py orphan message) + the
   close-session/new-session **skill-content** updates (worktree exit step, git-root keying).
   Partially overtaken: capture-feedback update is now a trim-pass rider.
5. Carried: worktree memory promotion review · four audit.py checks (gate `/share-topic`) ·
   floor re-measure.

## 🧠 Recent decisions

See `decisions.md` (entries 2026-08-07 → 2026-08-08). Load-bearing:

- **Phase 3 approved as written** — sentinel → B → A; the two ❓ calls (file-type four,
  resolve-vulns) stay open.
- **Skill-listing budget root-caused; gate closed PASSED** — trim is the fix for a live
  triggering bug, not a token optimization; budget raise is the deliberate second lever.
- **Invocation split (Carter): zero-bare rejected.** Model-invoked skills earn descriptions;
  user-invoked skills go absent via `disable-model-invocation`; name-only is for skill-to-skill
  reach. close/new-session → user-invoked; cron/shift family → model-invoked.

## 💡 What we learned

- **The description budget is aggregate — a commons.** Every verbose description evicts some
  other skill's triggering. gstack's terseness is what keeps the catalog alive.
- **Probabilistic failures get blamed on the model.** The evicted set varies per session/model,
  so broken triggering read as "model mood" for months. Deterministic bugs get found.
- **Names load unconditionally; descriptions are rationed.** A sentinel test that probes names
  proves the wrong half — triggering lives in the description.
- **Usage telemetry decides visibility** (`~/.claude/skill-usage.json` ranks eviction) — new
  skills start last in line exactly when discovery matters most.
- **Probe by skill name, not description phrase**; and `disable-model-invocation: true` renders
  a skill ABSENT from the listing while `/name` keeps working.
- **A description is a context pointer** (writing-for-agents): pay for it only where the agent
  must discover the skill; where the human is the index, spend cognitive load instead.

## 📂 Files touched · 🌿 git

All merged to `main` (worktree `phase3-plan` on branch `worktree-phase3-plan`, kept on disk;
merges interleaved cleanly with a parallel session's ROADMAP commits). This session:
`plan/phase3.md` (new, renamed) · `plan/skill-budget-ab.md` (new) · `plan/trim-skills.md` (new) ·
`research/sources/skill-description-drop.md` (new) · `plan/ROADMAP.md` (trim item, sentinel line)
· `decisions.md` (4 entries) · this file. Native store:
`reference-claude-code-loading-mechanics.md` extended with the budget + skills-symlink results.
Outside the repo: baseline tar `~/Claude/_archive/skill-trim_2026-08-07.tar.gz`; A/B fixture spec
targets `~/Sandbox/skill-budget-ab-fixture/` (not yet created).
