# Plan — working through TODO.md

*Rewritten 2026-08-21 after the grilling session that settled every open ruling. The decision
batch is done; this is now a pure execution sequence. S1 records the rulings in
`../.claude/memory/decisions.md` — until then, this file is the only record of them.*

## Rulings (Carter, 2026-08-21)

1. **§4 stop-gate:** trimming stops, but the gate closes only after a final classification pass —
   every non-gstack local skill re-confirmed as model-invoked or user-invoked, evidence-based
   (invocation counts), reviewed by Carter in a markdown table.
2. **A/B evidence:** re-run the test — after the classification flips land, same fixture
   (`~/Sandbox/skill-budget-ab-fixture`) and success bar (baseline ≤20%, subtraction ≥80%,
   delta ≥60pp), with targets selected by probing the untouched baseline at run time and
   keeping only verified-evicted skills; ≥4 valid targets required.
3. **Worktrees:** delete all 8 (the 7 merged ones + `todo-plan` once its branch is merged).
   Transcript sweep before each removal. Merging `worktree-todo-plan` is Carter's command,
   not a background job's.
4. **Write conventions:** the shared memory-write reference is written first; dream's writer,
   morning-shift's apply step (scripted, no more freehand), and the four drift fixes all become
   thin wrappers over it. Shifts-repo item 4.4 stays gated until the reference exists.
5. **Executors:** mechanical sessions run as background jobs Carter reviews; `audit.py` work is a
   night card; Phase 3 runs foreground/day-shift-planned.
6. **Mode-rule shadowing convention: ratified.** A mode file may add an obligation but never a
   sentence readable as a complete statement of a global rule. Governs all Phase-3 stamping.
7. **Skill placement:** `resolve-vulns` and `docx`/`pdf`/`pptx`/`xlsx` stay global. Plan A moves
   11 skills, not 15.

## Session sequence

### S1 — rulings + quick wins (background job)
- Record all rulings above in `decisions.md` (one dated entry); flip the `project-mode-rule-shadowing`
  memory from proposed → ratified.
- `new-session` launch-dir convention: add to `~/.claude/skills/new-session/SKILL.md` — launch at
  the project root or the mode folder fitting the next action, never deeper (wording drafted in
  `ROADMAP.md` "Still open"). Delete the two `SKILL.md.bak.20260622-*` files.
- Build the classification table → hand to Carter. Scope: the ~60 non-gstack local skills
  (48 KEEP + 12 flipped). Columns: skill · current state · one-line description · invocation
  count (from the skill-usage tracker + transcript `tool_use`-block counting — never plain grep,
  which inflates ~100x; note each count's window) · flip/keep recommendation. Commit the table
  to the repo as the §4 gate-closure artifact.

### S2 — Carter, async
- Mark the classification table.
- Run `git -C ~/Projects/memory-management merge worktree-todo-plan`.

### S3 — close the gate, clean the worktrees (background job)
- Apply the marked flips (`disable-model-invocation` frontmatter / settings).
- Re-verify the model-invoked listing is still <9K; if flips pushed it back over, stop and surface —
  do not silently accept.
- Close the §4 gate in `decisions.md`; fold `trim-diff.md` + `task-5-verification.md` into
  `research/sources/`.
- Worktree cleanup: per worktree — transcript sweep (`make/memory-repair/transcript_sweep.py`,
  per `docs/transcript-housekeeping-runbook.md`), `git worktree remove`, delete the merged
  branch. Also sweep the two already-orphaned transcript dirs (`…-mode-memory-research`,
  `…-roadmap-and-orphans`).

### S4 — A/B re-run (night card)
Per ruling 2. Runs only after S3's flips land (stable catalog). If <4 targets verify as evicted
at probe time, record "insufficient eviction to test" — that is a valid result, not a failure
to work around.

### S5 — memory-write reference + drift fixes (background job)
- Write the shared memory-write reference (ROADMAP Phase 1 item): routing test, git-root keying,
  frontmatter shape (`metadata.type:`, provenance fields), mandatory `MEMORY.md` index line,
  sectioned-index template, no-unverified-state rule.
- Then the four drift fixes as thin wrappers over it, one commit each:
  `brain-dump` (git-root store routing) · `memory-review` (actual-cwd store + sectioned index) ·
  `memory-janitor` agent (audit all stores) · `research-deep-dive` agent (route the write).
- `dream`: conform the writer's output shape to the reference. `morning-shift`: script the
  approve-apply step against the same writer. 4.4 stays gated until both conform.
- Light follow-up: repoint `close-session`/`new-session` guide text to the reference.

### S6 — audit.py four checks (night card)
- Extend `make/memory-repair/audit.py` with: stranded repo-subdir stores · lstat symlink
  resolution · containment invariant · fork tripwire. Run across all stores. Unblocks `/share-topic`.
- Close the worktree-memory-promotion review: verify against one kept worktree's history that
  the 2026-08-10 keying probe means nothing needs promoting; record closure (or the surprise)
  in `decisions.md`.

### S7 — Phase 3 (foreground / day-shift-planned)
- Plan B: `git init` + mode wiring + probe for the 9 non-repo projects, stamping mode files
  under the ratified shadowing convention. Only after all 9 probe clean: remove
  `# Planning a build` from `~/.claude/CLAUDE.md`.
- Plan A: move the 11 mode-home skills (15 minus the 4 file-type skills staying global);
  `resolve-vulns` stays global. Verify one-place loading via `audit.py`.

## What gets deleted, and how deletion is verified

| Deleted | Verified by |
| --- | --- |
| 8 worktrees + their merged branches | `git worktree list` shows only main; no `worktree-*` branches |
| transcript dirs of removed worktrees + 2 already-orphaned dirs | swept/archived per runbook; no orphaned `…-worktrees-*` dirs in `~/.claude/projects/` |
| 2 stale `new-session` `.bak` files | absent from the skill dir |
| `# Planning a build` in `~/.claude/CLAUDE.md` | section gone; recall probe stays neutral (phase3.md's gate) |
| 11 global skill entries (Plan A) | `audit.py` one-place-loading check; skill count drops by 11 |
| morning-shift's freehand apply instruction | replaced by the scripted path in SKILL.md step 2a |

## Falsifiers

- S3: flips push the listing back over 9K → stop and surface; the classification pass overrode
  the trim, and Carter re-rules.
- S4: <4 targets evicted at probe time → "insufficient eviction to test" is the recorded result.
- S5: dream's settled ADR format conflicts with the shared reference in a way wrappers can't
  bridge → surface the conflict; do not fork silently.
- S6: promotion review finds real un-promoted worktree memory → it becomes its own work item.
- S7: any of the 9 projects fails its probe → Plan B stops there; the global section stays.

## TODO.md bookkeeping

| TODO item | Flips `[x]` when |
| --- | --- |
| 1 — §4 stop-gate | S3 closes the gate |
| 2 — A/B evidence | S4's result is recorded (either outcome) |
| 3 — launch-dir convention | S1 |
| 4 — skill-drift fixes | S5 |
| 5 — Phase 3 | S7 |
| 6 — worktree housekeeping | S3 |
| 7 — promotion review + audit checks | S6 |
