---
project: memory-management
task: mode-memory-research (worktree branch)
session_ended: 2026-08-06T20:42:57Z
cwd: /Users/carterking/Projects/memory-management
git_branch: worktree-mode-memory-research
git_sha: 9d7d465
shape: gen4-modes
---

# Handoff — memory-management / mode-memory research session

## Next Action
From `~/Projects/memory-management`, merge branch `worktree-mode-memory-research` into `main`
(8 commits, no remote — local merge only).

Then, in order (details in `context.md` next-steps): run
`python3 make/memory-repair/transcript_consolidate.py` (dry-run, then `--execute`) to fold the
closed session's transcript out of the worktree-keyed dir — **fold BEFORE deleting the worktree**
— then begin Phase 2.5: container-store memory consolidation, capturing the process as a runbook
(Carter wants every procedure recorded for the dream/skill pipeline).

## Pointers
- Task memory entry point: `.claude/memory/context.md` (regenerated 2026-08-06; next-steps list is current)
- Decisions log: `.claude/memory/decisions.md` (two entries dated 2026-08-06)
- The design: `plan/mode-memory-design.md` · roadmap: `plan/ROADMAP.md` (new Phase 2.5)
- Experiments: `research/sources/native-memory-keying-and-symlink-experiments.md`
- Procedures: `docs/transcript-housekeeping-runbook.md` · `docs/memory-repair-runbook.md`
- Tools: `make/memory-repair/` (`audit.py`, `transcript_sweep.py`, `transcript_consolidate.py`)
- NOTE until merged: all of the above live on the branch — read them via this worktree's copy at
  `.claude/worktrees/mode-memory-research/…`

## Decisions This Session
- Native memory keys to the **git root** (sentinel-proven) → no mode-memory layer gets built
- Shared topic files = the one cross-store mechanism (canonical copy + symlink + index line); copying is forking
- Sessions open only at `<project>/` or `<project>/<mode>/` (Carter's launch convention)
- Transcript housekeeping is standing maintenance: sweep + consolidate tools, archive never delete
- Four audit.py checks are required before any memory symlink exists (spec in design doc)

## In-Flight Work
- Branch `worktree-mode-memory-research` — 8 commits awaiting local merge; working tree clean
- The closed session's transcript (`22ce04ba….jsonl`) still sits in the worktree-keyed dir
  `~/.claude/projects/-Users-carterking-Projects-memory-management--claude-worktrees-mode-memory-research/`

## Open Questions / Blockers
- Phase 2.5 routing will need Carter's rulings on borderline files (orphan-repair precedent:
  propose full manifest first, move nothing without approval)
- Still untested: folder-level **skills** symlink (memory experiments do not cover the skills loader)
