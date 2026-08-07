# Context — memory-management

**Last updated:** 2026-08-07 (skill-drift-sweep session; same day, another session approved Phase 3
plans + ran the skills-symlink sentinel — see `decisions.md`, two 2026-08-07 entry groups)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**Phase 2.5 is complete, Phase 3 is approved and pre-flighted — and the skills themselves are now
the known-drifted layer.**

- **Phase 3 plans approved (`plan/phase3.md`, renamed from `skill-relocation-plan.md`):** sentinel
  test → Plan B (restamp every project) → Plan A (move the last 15 mode-home skills) → re-measure.
  Two ❓ still open: the file-type four's destination, `resolve-vulns`. The skills-symlink sentinel
  verdict is **SPLIT** (commits `5ea0f92`, `b7e4993`): skill *names* load through folder-level +
  two-hop symlinks, but natural-language triggering rides on *descriptions* — check those commits /
  decisions.md before assuming symlinked skills fire by phrase.
- **Skill drift sweep done (2026-08-07, three read-only agents + spot-checks):** ten skills/agents
  drift from the current memory model. Worst: `close-session`, `brain-dump`, `capture-feedback`,
  `memory-review`, `restructure-project`, plus the `memory-janitor` and `research-deep-dive`
  agents. Root cause: conventions encoded by copy while the model changed underneath (git-root
  keying + consolidation, mode files, mempalace death). Full punch list is ON the roadmap
  (Phase 1 / 2.5 / 3 additions).
- **Maintenance architecture decided** (`decisions.md` 2026-08-07): single-source memory-write
  reference · **derived** dependency map · retired-token tripwire in `audit.py` · the 4-step
  cross-skill change protocol.

## ⏭️ Next steps / open

Full list in `plan/ROADMAP.md`. Suggested order:

1. **Build the shared memory-write reference first** — it turns every skill rewrite into a thin
   wrapper instead of six parallel hand-edits.
2. **Execute the drift punch list** (Phase 2.5 item; hand edits in `~/.claude/skills/` +
   `~/.claude/agents/`, outside this repo) together with the close-session/new-session update.
   ⚠️ **Stale: that update has been open since 2026-08-06, now 4+ sessions** — close-session
   still runs a mempalace phase Carter ruled dead and still claims exact-cwd keying.
3. **dream + morning-shift write conventions before roadmap 4.4 flips memory writes on.**
4. **Phase 3 execution per `phase3.md`** (Plan B restamp → Plan A moves), minding the sentinel
   SPLIT caveat; rewrite `restructure-project`/`new-project` to Gen 4 *before* stamping starts.
5. Carried: the four `audit.py` checks · correction sweep (exact-cwd wording) · worktree memory
   promotion review · dependency-map script + retired-token tripwire (new) · floor re-measure.

## 🧠 Recent decisions

See `decisions.md` (two 2026-08-07 entry groups). Load-bearing:

- **Skill conventions go single-source, referenced** — the mode-files mechanism applied to the
  memory writers; the frontmatter fork (`type:` vs `metadata.type:`) proved copies already drift.
- **Dependency maps are derived, never hand-drawn** — a hand-maintained map is one more copy.
- **Cross-skill convention changes follow the 4-step protocol** (name the convention → generate
  the map → one change set covering all dependents → retire the old token).
- **Phase 3 approved as written; sentinel verdict SPLIT** (names load via symlinks, description
  triggering doesn't ride along).

## 💡 What we learned

- **The skills are the untracked dependents of the memory model.** Every model change so far
  fanned out into skills nobody updated; the drift was found by sweep, not by tripwire. The
  retired-token list converts this one-off sweep into a standing audit check.
- **Five change classes fan out across skills:** where memory lives · file formats · retiring an
  artifact · project shape · session lifecycle rules. Scaffolders are the most-missed dependent —
  `restructure-project` still builds the previous generation.
- **The sweep pattern worked:** three read-only agents extracting quotes with line numbers,
  judgment kept in the main session, load-bearing claims spot-verified before reporting.
- **The bg-isolation guard applies to memory files too:** a background session cannot write
  `.claude/memory/` in the shared checkout — close-session writes ride a worktree branch and
  merge, which is the worktree-memory-promotion pattern working as designed (project memory is
  git-tracked; native-store writes from worktrees stay forbidden).

## 📂 Files touched · 🌿 git

Project at `~/Projects/memory-management/`. This session (branch
`worktree-todo-capture-reference`, fast-forwarded to main `d1203f3` then extended):
`plan/ROADMAP.md` (+67 lines: `/capture-reference` + five sweep to-dos — merged to main mid-
session), `decisions.md` (2026-08-07 sweep entry), this file. Outside the repo:
`~/Claude/session-logs/thinking-patterns.md` + `2026-08-07.md` (session 2 append). Worktrees on
disk: `todo-capture-reference` (this close's memory writes — merge then delete when ready),
`phase3-plan` (fully merged) — **fold transcripts per the runbook before deleting either.** No
remote. Native store deliberately not written from the worktree.
