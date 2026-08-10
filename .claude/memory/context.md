# Context — memory-management

**Last updated:** 2026-08-10 (session 7, bg — stale blockers cleared: all branches merged,
correction sweep shipped, close/new-session de-staled)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**The repo is consolidated. `main` holds everything; no branch is unmerged.** Four parallel
worktree branches plus one set of uncommitted `make/`-session writes had accumulated over sessions
4–6. All are now on `main`, with `decisions.md` reconciled to **20 entries** — the union across
three writers, four of which existed in only one copy.

**The skill-listing budget bug is fixed on disk, and the trim is gate-blocked, not unfinished.**
This was the single biggest misconception in the memory: two sessions wrote conflicting accounts,
and both were partly wrong. Verified on disk 2026-08-10:

- **11** skills carry `disable-model-invocation: true` (session 5's "12" was one high).
- The `capture-feedback` Gen-4 rider **shipped** (session 6's "unapplied" was wrong).
- 104 skills in `~/.claude/skills/` (+3 under `~/.agents/skills/`); `fable-plan` present,
  `opusplan` gone; `skillOverrides: {"sources-cited": "name-only"}` set.
- 83 model-invoked non-gstack skills carry **13,248 description chars, 24 still over 200**.

Session 5's execution numbers stand: catalog **18,440 → 8,086 chars** (goal <9K), bare-name probe
`114,16` → `128,1` ×3, over-budget WARN gone, one bare name (`sources-cited`) by design. **The
remaining 24 long descriptions are held by the plan's own §4 stop-gate, awaiting Carter's ruling —
not forgotten work.** The executing session's standing recommendation is to stop there.

**The A/B verdict: FALSIFIED on the metric, mechanism intact.** Baseline 75%, subtraction 100%,
delta 25pp against a 60pp bar. Only 1 of 4 targets (`youtube-slide-transcript`) was actually
evicted at baseline; for that one, restoration was a clean 0/5 → 5/5. The bar was arithmetically
unreachable — a **precondition failure, not a mechanism failure**. What stays unconfirmed is the
*aggregate* claim, not the mechanism. Results: `research/sources/skill-description-drop.md`, now
on `main`.

**Keying is now stated correctly everywhere.** Verified on disk: *transcripts* key to the exact
cwd, *native memory* keys to the **git root**. `~/.claude/projects/` holds a directory per working
directory (`…-make`, `…-research`, one per worktree) but **only the git-root directory has a
`memory/` folder**. So mode folders and worktrees cannot fragment native memory — the opposite of
what the root `CLAUDE.md` claimed for months. A repo *move* still strands a store.

**The trim/A-B collision flagged on 08-08 never landed.** Two independent lines of evidence agree:
commit timestamps (A/B results 12:47, flips 12:58, `tdd` archive 13:45) and the probe readings
themselves (an evicted skill reads NAME-ONLY, a flipped one reads ABSENT). The warning was right to
send — the plans genuinely share `~/.claude/` state, which worktrees cannot isolate — but the
ordering held by luck, not design.

## ⏭️ Next steps / open

1. **⛔ Carter's §4 stop-gate ruling on the trim** — the one real decision outstanding.
   `trim-diff.md` (verbatim old/new + char counts for all 11 trims) is the gate document, in the
   kept worktree at `.claude/worktrees/skill-budget-execution/.superpowers/sdd/trim-skills/`.
   Recommendation from the executing session: **stop** — the <9K target is met.
2. **Decide what replaces the falsified A/B as evidence for the aggregate claim.** Honest options:
   re-run with targets verified evicted *at probe time*, or accept the mechanism as proven and
   record the aggregate as unmeasured. Do not silently drop it.
3. **Phase 3 Plan B — restamp the projects** (git init the 9 non-repos + wire mode
   CLAUDE.mds/symlinks, probe each; runbook step 5), then remove `# Planning a build` from the
   global CLAUDE.md.
4. **Phase 3 Plan A — move the 15 mode-home skills** (after B), then re-measure the floor (free).
5. **Worktree housekeeping (Carter's call).** Five worktrees remain on disk, all now merged:
   `skill-budget-execution` (**keep** — its SDD workspace is the only record of skill edits made
   outside the repo), `close-session-plugin-dedup`, `todo-capture-reference`, `phase3-plan`,
   `stale-blockers`. Fold transcripts before deleting any of them.
6. Carried: worktree memory promotion review · four `audit.py` checks (gate `/share-topic`) ·
   optional pruning of 4 zero-use inline plugins · optional removal of the claude.ai Gmail +
   Calendar connectors (`google_workspace` covers both).

*Cleared this session:* the four-unmerged-branches warning, the correction sweep (open since
2026-08-06), and the close-session/new-session staleness items.

## 🧠 Recent decisions

See `decisions.md` (entries 2026-08-07 → 2026-08-10). Load-bearing:

- **Append-only files merge as a set union, not latest-wins** — `decisions.md` and `context.md`
  needed opposite conflict resolutions in the same merge, decided by each file's contract.
- **A falsified verdict can still be a PROCEED** when the failure is a *precondition* failure —
  but the reasoning gets written down, never quietly waved through.
- **Invocation split (Carter): zero-bare rejected.** Model-invoked skills earn descriptions;
  user-invoked skills go absent via `disable-model-invocation`; name-only is for skill-to-skill
  reach. close/new-session → user-invoked; cron/shift family → model-invoked.
- **Duplicated skills resolve to the managed plugin copy** (Carter's ruling, `tdd` case).
- **Permission laundering refused:** a denial in one agent is never authorization for another.

## 💡 What we learned

- **A file's merge strategy comes from its contract, not from git.** Append-only → union;
  regenerated snapshot → discard both sides and rewrite. Taking git's default on an append-only
  log deletes history silently.
- **Two confident write-ups of the same work can both be wrong.** Session 5 and session 6
  disagreed on flip count and rider status; only disk settled it. Reconcile against the artifact,
  never against the more recent prose.
- **"Unfinished" and "gate-blocked" look identical in a status file and mean opposite things.**
  The trim read as abandoned for two sessions when it had deliberately stopped at its own gate.
  Write the *reason* work stopped, or the next session re-opens settled questions.
- **A metric can falsify while the mechanism holds.** Verify the effect is *present* in every
  target before measuring how well you can remove it.
- **The evicted set moves with the model, not just with usage.** 30,000-char budget on one model,
  8,000 on another — a "which skills are bare" answer is only valid for the model that produced it.
- **Forensics: compare against the result timestamp, not the write timestamp.**
- **A skill that reroutes other people's writes can be stale about its own** — running
  `close-session` is what surfaced that it still wrote to the Gen-3 scheme it had removed elsewhere.
- **Converting a resolved warning beats deleting it.** A dated "Resolved" note lets a future reader
  tell "handled" from "never existed" — and the permission classifier agrees.

## 📂 Files touched · 🌿 git

`main` now contains every branch. Session 7 merged, in order: `7f25bdd` (session 5's orphaned
`make/` writes, committed first so conflict resolution couldn't eat them), then
`worktree-skill-budget-execution` → `worktree-todo-capture-reference` →
`worktree-close-session-plugin-dedup`. `worktree-phase3-plan` was already at main.

Session 7 edits (branch `worktree-stale-blockers`): `CLAUDE.md` (keying table + mode-fragmentation
rationale) · `docs/memory-repair-runbook.md` (mechanism section) · `make/memory-repair/audit.py`
(orphan message) · `plan/ROADMAP.md` (trim status corrected to gate-open, with disk verification) ·
`decisions.md` (+1 entry, 21 total) · this file.

Outside the repo, no git record: `~/.claude/skills/close-session/SKILL.md` (banner → Phase 8;
Phase 3.7 Gen-4 routing; mempalace phase removed; native keying) ·
`~/.claude/skills/new-session/SKILL.md` (`history.md` reference removed; worktree guard added).
Still outside git from session 5: pre-edit tar `~/Claude/_archive/skill-trim_2026-08-08.tar.gz`,
the trimmed/flipped SKILL.md files, `~/.claude/settings.json`, `~/.claude.json`.
