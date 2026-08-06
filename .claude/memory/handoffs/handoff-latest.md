---
project: memory-management
task: phase25-manifest (worktree branch) → Phase 2.5 execution
session_ended: 2026-08-06 (evening)
cwd: /Users/carterking/Projects/memory-management
git_branch: worktree-phase25-manifest
shape: gen4-modes
---

# Handoff — Phase 2.5: manifest approved, execution is yours

## Next Action (in order)

1. From `~/Projects/memory-management`, **merge `worktree-phase25-manifest` into `main`**
   (no remote — local merge only; `git log main..worktree-phase25-manifest --oneline` shows the
   8 commits coming).
2. **Fold this session's transcript BEFORE deleting the worktree:**
   `python3 make/memory-repair/transcript_consolidate.py` (dry-run, review, then `--execute`) to
   fold the worktree-keyed dir `…-memory-management--claude-worktrees-phase25-manifest` up into
   the project dir. The 1-hour activity guard will skip it right after close — wait it out or
   hand-fold per the runbook's Procedure C. **Fold, then delete the worktree — never the reverse**
   (a dead dir gets archived by sweep, not folded).
3. **Run the `@import` sentinel test** before anything touches `~/.claude/modes/`: (a) a
   `@~/.claude/modes/TEST.md` import line in a mode CLAUDE.md loads its content; (b) what a
   **missing** import target does — loud or silent (silent = E5's camouflage → needs an audit
   check first). ALWAYS.md and the whole mode-files delivery are **contingent on this test**.
   Record the results in `reference-claude-code-loading-mechanics` (native store, from project
   root) — deliberately left unwritten by the worktree session.
4. **Collect Carter's remaining gates** before moving files: Tranche 1 go (53 routes) · 3 unruled
   Tranche 2 files (`plan-pmg-life-app`, `notion-multi-workspace-safety`,
   `model-configuration-guide`) · the 8 ASKs (Tranche 3).
5. **Execute per the manifest's procedure** (`plan/container-consolidation-manifest.md`, bottom):
   audit clean → backups to `~/Claude/_archive/container-stores_<date>/` → destination toplevel
   re-check → route.py to `LEFT 0` → **sectioned indexes per the sorted-MEMORY.md template** →
   fold the 36 mode-principle + 12 Always files into `~/.claude/modes/` files, then delete →
   demote the three promoted rules out of `~/.claude/CLAUDE.md` → fix-in-passing items → audit
   exit 0. **Capture the runbook as it runs** (`docs/`), per Carter's standing rule.
6. After merge: **re-mine this memory dir into mempalace** (wing `memory-management`) — skipped at
   close because the worktree path would have indexed wrong.

## Pointers

- **The deliverable:** `plan/container-consolidation-manifest.md` — Carter reviewed it in full;
  rev 2 (mode files) is his design. All rulings and the tiering table are recorded inline.
- Task memory entry: `.claude/memory/context.md` · decisions: `.claude/memory/decisions.md`
  (2026-08-06 mode-files entry + the in-place-correction exception in the header)
- Roadmap: `plan/ROADMAP.md` (Phase 3 mode-files bullet carries the full tiering spec)
- Runbooks: `docs/transcript-housekeeping-runbook.md` · `docs/memory-repair-runbook.md`
- NOTE until merged: everything above lives on the branch — read via the worktree copy at
  `.claude/worktrees/phase25-manifest/…`

## Decisions This Session (all Carter's)

- Mode principles live **once** at `~/.claude/modes/<MODE>-MODE.md`, `@import`-ed by mode
  CLAUDE.mds — never copied. Routing test: project-specific → MEMORY.md (Project Awareness);
  mode principle → mode file (Situational Awareness).
- **CLAUDE.mds explain and navigate; memory remembers** (container/project/mode tiering — table
  in the manifest).
- ALWAYS.md approved **contingent on the `@import` sentinel test** (incl. broken-import check).
- Rulings: ghostty DELETE · user-* approved · subskill-vs-reference fold-then-delete · the three
  promoted rules leave `~/.claude/CLAUDE.md`.
- Misrecorded decisions are corrected **in place**, never by appended correction.
- Execution happens in a **new session** (this handoff), with everything persisted first.

## Open Questions / Blockers

- The four audit.py checks are still unbuilt — they gate the shared-file symlinks (Tranche 4's
  library remainder), not the mode files.
- ⚠️ Carried two sessions without movement: the correction sweep (root CLAUDE.md table,
  memory-repair runbook, audit.py orphan message, close-session Phase-5 text still claim
  exact-cwd keying) + updating the close-session/new-session skills to the new memory patterns.
  **Add to the close-session skill update (recurring pain, Carter 2026-08-06):** a worktree
  session must end by stepping OUT of the worktree (ExitWorktree, keep — never remove) so Agent
  View can close without blocking on the keep/remove worktree decision. "Keep" is always the
  answer in this workflow: the branch merges later and the transcript folds later.
- Worktree memory promotion review (ROADMAP Phase 2.5) — still open, untouched by design.
