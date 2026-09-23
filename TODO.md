# TODO — memory-management

- [x] Carter: rule on the §4 stop-gate for the skill-description trim — gate doc `trim-diff.md` in worktree `skill-budget-execution`; executing session recommends stop (<9K target met) — added 2026-08-19, done 2026-08-21
- [ ] Decide what replaces the falsified A/B as evidence for the aggregate claim: re-run with targets verified evicted at probe time, or record it as unmeasured (results: `research/sources/skill-description-drop.md`) — added 2026-08-19
- [x] Write the launch-dir convention into `new-session`: launch at the project root or mode folder, never deeper — added 2026-08-19, done 2026-08-21
- [ ] Remaining skill-drift fixes from the 2026-08-07 sweep: `brain-dump` store routing, `memory-review`, `memory-janitor`, `research-deep-dive`, `dream` + `morning-shift` — added 2026-08-19
- [ ] Phase 3 Plan B: restamp the 9 non-repo projects (git init + mode wiring, probe each), then remove "# Planning a build" from global CLAUDE.md; Plan A (move 15 mode-home skills) after — added 2026-08-19
- [x] Carter: worktree housekeeping — six merged worktrees on disk; keep `skill-budget-execution`, fold transcripts before deleting any — added 2026-08-19, done 2026-08-21
- [ ] Carried: worktree memory promotion review; four `audit.py` checks (gates `/share-topic`) — added 2026-08-19
- [x] Package the mode-based memory setup as a shareable repo, modeled on affaan-m/ecc's product framing (`~/Projects/mode-memory` → `ck22coding/mode-memory`, private, 2 commits, 27/27 tests) — added 2026-09-22, done 2026-09-22
- [ ] Carter: review mode-memory's generalized `modes/*.md` (esp. the "Working with me" placeholder in ALWAYS.md) and the two rewritten skills, then flip `ck22coding/mode-memory` public — added 2026-09-22
- [ ] Decide how mode-memory ships its skills: plugin manifest only, `install.sh --skills` copy only, or keep both with the README's "pick one" — added 2026-09-22
- [ ] Sync rule for the two mode-file copies: a principle added to `~/.claude/modes/` only ships if also edited in `mode-memory/modes/` — decide whether that stays manual or gets a diff check in `audit.py` — added 2026-09-22
