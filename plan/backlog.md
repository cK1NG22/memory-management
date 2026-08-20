# Plan — working through TODO.md

*Drafted 2026-08-20. Sequences the 7 open items in the root `TODO.md` into five sessions:
one decision batch for Carter, then four execution sessions ordered so each unlocks the next.
Rewrite as items close; the durable record of each ruling goes to `../.claude/memory/decisions.md`.*

## Why this order

Three of the seven items are Carter-only rulings, and one ruling (the §4 stop-gate) is the
single thing keeping a worktree alive and a cleanup blocked. So the sequence is: **decide
everything first in one sitting, then execute in dependency order** — quick mechanical wins,
then skill fixes, then the audit tooling, then Phase 3 (the biggest and least blocked-upon).

Dependency chain that forces the order:

- §4 ruling (item 1) → fold `trim-diff.md` into the repo → `skill-budget-execution` worktree
  becomes deletable → worktree housekeeping (item 6) can finish completely.
- Write-conventions decision → unblocks the `dream`/`morning-shift` half of the drift fixes (item 4).
- Four new `audit.py` checks (item 7) → unblocks `/share-topic` (queued in ROADMAP Phase 1).
- Phase 3 Plan B (item 5) → gates removing `# Planning a build` from global CLAUDE.md → Plan A after.

---

## Session 1 — the decision batch (Carter, ~15 min, no code)

One sitting, four rulings. Each gets an entry in `decisions.md` when made.

1. **§4 stop-gate** (TODO item 1). Gate doc:
   `.claude/worktrees/skill-budget-execution/.superpowers/sdd/trim-skills/trim-diff.md`.
   **Recommend: stop.** The <9K listing target is met (8,086 chars), bare-name count fell 16→1,
   the over-budget WARN is gone, and the executing session's own analysis says trimming past the
   top 10 buys nothing measurable.
2. **A/B evidence replacement** (item 2). **Recommend: record as unmeasured.** The one target
   genuinely evicted at baseline went 0%→100% (mechanism confirmed); the other three were never
   evicted, so the aggregate claim was untestable, not disproven. A re-run with per-probe
   eviction verification costs a fixture session and changes no downstream decision — the trim
   already hit its target. Annotate `research/sources/skill-description-drop.md` accordingly.
3. **Worktree deletion list** (item 6). **Recommend: delete all 7** (TODO says six; disk shows
   seven — `todo-system-build` and `todo-system-plan` were unlisted, both clean and merged).
   All 7 branches are merged into main, all trees clean. `skill-budget-execution` becomes
   deletable the moment ruling 1 lands and `trim-diff.md` is folded in (Session 2).
4. **`dream`/`morning-shift` write conventions** (gates half of item 4). Decide the memory-write
   conventions those two skills must bake in, or explicitly defer — deferral just splits item 4
   into a done-now half and a later half.

## Session 2 — mechanical quick wins (~1 focused session)

- **Item 3 — launch-dir convention into `new-session`.** Add to
  `~/.claude/skills/new-session/SKILL.md`: launch at the project root or the mode folder that
  fits the next action (`<project>/` or `<project>/<mode>/`), never deeper. Wording already
  drafted in `ROADMAP.md` ("Still open", ~line 217). Also delete the two stale
  `SKILL.md.bak.20260622-*` files sitting in that skill dir.
- **Fold the gate record** (from ruling 1): copy `trim-diff.md` (and
  `task-5-verification.md`) into `research/sources/` on main, commit, then the worktree holds
  nothing unique.
- **Item 6 execution — worktree housekeeping.** Order per worktree: transcript sweep first
  (`make/memory-repair/transcript_sweep.py`, per `docs/transcript-housekeeping-runbook.md`),
  then `git worktree remove`, then delete the merged `worktree-*` branch. Today only
  `stale-blockers` has a live transcript dir; also sweep the two already-orphaned transcript
  dirs (`…-mode-memory-research`, `…-roadmap-and-orphans`) while in there.
- **Item 2 execution** (from ruling 2): annotate `skill-description-drop.md`, write the
  `decisions.md` entry.

## Session 3 — skill-drift fixes (item 4)

The four unblocked fixes, one commit each, per the 2026-08-07 sweep record
(`ROADMAP.md` ~lines 161–184):

| Target | Fix |
| --- | --- |
| `~/.claude/skills/brain-dump/` | route dumps to the session's git-root store, not hardcoded `~/Projects` |
| `~/.claude/skills/memory-review/` | review the store for the actual cwd; sectioned-index template |
| `~/.claude/agents/memory-janitor.md` | run `audit.py` across all stores, not one hardcoded store |
| `~/.claude/agents/research-deep-dive.md` | route the memory write to the store the research belongs to |

`dream` + `morning-shift` follow only if ruling 4 settled the write conventions; otherwise they
stay on TODO.md as their own line with the decision named as the blocker.

## Session 4 — the four new `audit.py` checks (item 7)

Extend `make/memory-repair/audit.py` (which already has four *other* checks — orphaned stores,
dangling index links, broken @imports, unindexed files) with the four ROADMAP Phase 2.5 checks:
stranded repo-subdir stores, lstat symlink resolution, containment invariant, fork tripwire.
Run it across all stores when done. This unblocks `/share-topic`.

Also in this session: **close the worktree-memory-promotion review.** The 2026-08-10 probe
showed worktree sessions write native memory to the main repo root store, so there is likely
nothing to promote — verify that against one kept worktree's history and record the closure
(or the surprise) in `decisions.md`.

## Session 5 — Phase 3 (item 5, the big one)

Execute `plan/phase3.md` as approved: **Plan B first** — `git init` + mode wiring + probe for
the 9 non-repo projects (`dad`, `hoth`, `loops`, `ai-engineering`, `neon-learning`,
`health-insurance`, `outreach`, `mana-ventures`, `custom-agents`). Only after all 9 probe clean:
remove `# Planning a build` from `~/.claude/CLAUDE.md`. Then **Plan A** (move the 15 mode-home
skills), which carries its own two open ❓ calls for Carter (`resolve-vulns` destination;
docx/pdf/pptx/xlsx → `make/` or stay global) — batch those into Session 1 if convenient, they
don't block anything before Plan A. Pre-check before starting: the proposed mode-rule shadowing
convention (native memory, `project-mode-rule-shadowing`) is still unratified — ratify or
explicitly waive it before stamping mode files at scale.

---

## What gets deleted, and how deletion is verified

Per plan-mode rule: a migration that doesn't delete is an addition.

| Deleted | Verified by |
| --- | --- |
| 7 worktrees + their merged branches | `git worktree list` shows only main; `git branch` shows no `worktree-*` |
| transcript dirs of removed worktrees | swept/archived per runbook before removal; `ls ~/.claude/projects/` shows no orphaned `…-worktrees-*` dirs |
| 2 stale `new-session` `.bak` files | absent from the skill dir |
| `# Planning a build` in `~/.claude/CLAUDE.md` | section gone; recall probe stays neutral (phase3.md's gate) |
| 15 global skill entries (Plan A) | `audit.py` one-place-loading check; skill count drops by 15 |

## Falsifiers

- If after ruling 1 the worktree still holds something unique besides `trim-diff.md` +
  verification, the fold step was wrong — re-inventory before deleting.
- If any of the 9 restamped projects fails its probe, Plan B stops there; the global CLAUDE.md
  section stays until all 9 pass.
- If the promotion review finds real un-promoted worktree memory, Session 4's "likely moot"
  assumption is wrong — it becomes its own work item instead of a closure note.

## TODO.md bookkeeping

Flip each item to `[x] … done <date>` the moment its session completes it — Session 1 flips
nothing by itself (rulings enable work; the flips happen when the work lands), except item 1
and 2 which are pure decisions and flip on the `decisions.md` entry.
