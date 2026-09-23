# Context — memory-management

**Last updated:** 2026-09-23 (gstack-removal note only; the rest of this file is as of 2026-08-10,
session 7 close — stale blockers cleared; store keying probe-verified)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**2026-09-23 — gstack is gone.** Carter had the usage measured (1 of 54 skills used, `browse`
only) and had the whole kit ripped out: clone, `~/.gstack`, 55 skill dirs, settings permissions,
25 per-project state folders. Global skills **106 → 50**. Every `gstack` reference below and in
`plan/` is now historical. Record: `decisions.md` 2026-09-23; native memory
`project-gstack-removed.md`; three follow-ups in `TODO.md`.

**The repo is consolidated. `main` holds everything; no branch is unmerged.** Four parallel worktree
branches plus one set of uncommitted `make/`-session writes had accumulated across sessions 4–6.
All are on `main`, with `decisions.md` reconciled to **22 entries** — the union across three
writers, four of which existed in only one copy.

**Store keying is now probe-verified, not inferred — and it is the session's most reusable result.**
*Transcripts key to the launch cwd; native memory keys to the **main repo root**, even from inside a
worktree.* Two independent probes: the `make/` session's transcript sits in
`…-memory-management-make` while its own memory writes landed in the repo-root store; and a
`claude -p` launched inside `.claude/worktrees/stale-blockers` reported the **main repo's** store as
its memory directory, leaving a worktree store dir with a transcript and no `memory/`. Resolve the
key with `git rev-parse --path-format=absolute --git-common-dir` minus `/.git` — **not**
`--show-toplevel`, which returns the worktree. Consequences: mode folders and worktrees cannot
fragment native memory, background-job writes are visible to the main session, and **deleting a
worktree does not orphan native memory** (the roadmap's guard to the contrary is withdrawn).

**The skill-listing budget bug is fixed on disk, and the trim is gate-blocked, not unfinished.**
Two sessions had written conflicting accounts and both were partly wrong. Verified 2026-08-10:
**11** skills carry `disable-model-invocation: true` (session 5's "12" was one high); the
`capture-feedback` Gen-4 rider **shipped** (session 6's "unapplied" was wrong); 104 skills in
`~/.claude/skills/` (+3 under `~/.agents/skills/`); `fable-plan` present, `opusplan` gone. 83
model-invoked non-gstack skills carry **13,248 description chars, 24 still over 200** — held by the
plan's own §4 stop-gate awaiting Carter's ruling, **not** forgotten work. Session 5's execution
numbers stand: catalog 18,440 → 8,086 chars, probe `114,16` → `128,1` ×3, over-budget WARN gone.

**The A/B verdict: FALSIFIED on the metric, mechanism intact.** Baseline 75%, subtraction 100%,
delta 25pp vs a 60pp bar — but only 1 of 4 targets was evicted at baseline, so the bar was
arithmetically unreachable. A **precondition failure, not a mechanism failure**; the one real target
swung 0/5 → 5/5. The *aggregate* claim is unmeasured, not disproven.
Results: `research/sources/skill-description-drop.md`, on `main`.

**The correction sweep and the skill de-staling are done** (both open since 2026-08-06, ~6
sessions). Root `CLAUDE.md`, `docs/memory-repair-runbook.md`, and `audit.py` all state repo-root
keying; `audit.py` re-runs clean (38 stores, 0 orphans). `close-session` gained **Phase 8** (exit
worktree with `keep`), lost the mempalace phase and the hardcoded `-Users-carterking-Projects`
Phase-1 scan, and routes durable norms to Gen-4 scopes. `new-session` lost its retired `history.md`
reference and gained the worktree case per Carter's design (handoff written **and committed on the
branch**).

## ⏭️ Next steps / open

Moved to the root `TODO.md` (2026-08-19) — the per-project TO-DO file is the live list now
(convention: `plan/todos.md`). This section is a pointer, not a list.

## 🧠 Recent decisions

See `decisions.md` (entries 2026-08-07 → 2026-08-10). Load-bearing:

- **Probe before writing a claim into multiple files.** A lucky inference and a verified fact look
  identical on disk — this project's founding failure mode.
- **Append-only files merge as a set union, not latest-wins** — `decisions.md` and `context.md`
  needed opposite conflict resolutions in the same merge, decided by each file's contract.
- **A falsified verdict can still be a PROCEED** when the failure is a *precondition* failure — but
  the reasoning gets written down, never quietly waved through.
- **Invocation split (Carter): zero-bare rejected.** Model-invoked skills earn descriptions;
  user-invoked skills go absent; name-only is for skill-to-skill reach.
- **Duplicated skills resolve to the managed plugin copy** (Carter's ruling, `tdd` case).

## 💡 What we learned

- **Absence of a thing is not evidence of the rule that would explain it.** "Worktrees are safe" was
  inferred from missing `memory/` folders in worktree store dirs; those sessions had simply never
  written native memory. Right answer, wrong evidence — until probed.
- **Project memory and native memory move in opposite directions from a worktree.** Project memory
  follows the *branch* and must be committed there; native memory ignores the worktree entirely. A
  skill that conflates them gets one of the two wrong.
- **A file's merge strategy comes from its contract, not from git.** Append-only → union;
  regenerated snapshot → discard both sides and rewrite.
- **Two confident write-ups of the same work can both be wrong.** Reconcile against the artifact,
  never against the more recent prose.
- **"Unfinished" and "gate-blocked" look identical in a status file and mean opposite things.**
  Write the *reason* work stopped, or the next session re-opens settled questions.
- **A skill's staleness is invisible from inside it.** Running `close-session` is what exposed its
  hardcoded one-store Phase-1 scan, as it did the mempalace and task-types bugs two sessions back.
- **The evicted set moves with the model, not just with usage** — a "which skills are bare" answer
  is only valid for the model that produced it.
- **Converting a resolved warning beats deleting it** — a dated "Resolved" note distinguishes
  "handled" from "never existed," and the permission classifier agrees.

## 📂 Files touched · 🌿 git

`main` contains every branch. Session 7 merged, in order: `7f25bdd` (session 5's orphaned `make/`
writes, committed first so conflict resolution couldn't eat them), then
`worktree-skill-budget-execution` → `worktree-todo-capture-reference` →
`worktree-close-session-plugin-dedup` → `worktree-stale-blockers` (`6c7b0eb`).
`worktree-phase3-plan` was already at main.

Session 7 repo edits (branch `worktree-stale-blockers`): `CLAUDE.md` (keying table, mode-
fragmentation rationale, probe results) · `docs/memory-repair-runbook.md` ·
`make/memory-repair/audit.py` (orphan message) · `plan/ROADMAP.md` (trim status corrected to
gate-open; correction sweep checked off; close/new-session item marked partial; **the false worktree
guard withdrawn**; `git init` item's premise confirmed) · `decisions.md` (+2 entries, 22 total) ·
this file.

Outside the repo, no git record: `~/.claude/skills/close-session/SKILL.md` (Phase 8; Gen-4 routing;
mempalace removed; repo-root keying; Phase-1 scan de-hardcoded) ·
`~/.claude/skills/new-session/SKILL.md` (`history.md` removed; worktree case per Carter's design) ·
native `reference-store-keying-mechanics.md` (probe results + resolution command).
From session 5, still outside git: `~/Claude/_archive/skill-trim_2026-08-08.tar.gz`, the
trimmed/flipped SKILL.md files, `~/.claude/settings.json`, `~/.claude.json`.
