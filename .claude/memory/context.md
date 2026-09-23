# Context — memory-management

**Last updated:** 2026-09-22 (bg session close — the setup was packaged as a public repo)

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**The setup now exists as a product: `~/Projects/mode-memory` → `ck22coding/mode-memory`,
private until Carter reviews and flips it.** Built 2026-09-21/22 in a background session, modeled
on `affaan-m/ecc`'s framing but 33 files: generalized `modes/*.md`, `install.sh`,
`new-project.sh`, a generic `tools/audit.py`, rewritten `close-session` + `new-session`, a plugin
manifest, five docs distilled from this repo's `docs/`, an SVG hero (light + dark), and a
hermetic test suite (27/27). Two commits, both pushed. Dry-runs against this machine are no-ops.
Native note: `project-mode-memory-repo.md`. Nothing in this repo changed except this file,
`decisions.md`, and `TODO.md`, on branch `worktree-close-session-mode-memory` (unmerged).

**Consequence to hold onto: the mode files now have two copies by design.** `~/.claude/modes/`
is personal and live; `mode-memory/modes/` is generic and shipped. The installer never overwrites
a differing file, so a principle added here ships only if also edited there. The personal
`make/memory-repair/audit.py` and the product's `tools/audit.py` likewise differ now (the product
one takes paths as arguments and has no `CONTAINERS`).

**Before this session (S3, 2026-08-21):** the §4 stop-gate is **closed** — model-invoked listing
8,580 chars across 31 skills, under the 9,000 target; four invocation flips applied
(`connect-chrome` and `open-gstack-browser` turned out to be one symlinked file, so both flipped).
All 8 worktrees and their merged branches deleted; transcripts folded per runbook. **S4 is
blocked:** `~/Sandbox/skill-budget-ab-fixture` no longer exists; rebuild from the recipe in
`research/sources/skill-description-drop.md` or Carter re-rules.

**Still true and load-bearing:** store keying is probe-verified — transcripts key to the launch
cwd, native memory to the **main repo root** even inside a worktree (resolve with
`git rev-parse --path-format=absolute --git-common-dir` minus `/.git`). Mode folders and
worktrees cannot fragment native memory. Full record: `reference-store-keying-mechanics`.

## ⏭️ Next steps / open

The root `TODO.md` is the live list. Four items were added 2026-09-22 (review + flip public,
skill install path, mode-file sync rule).

⚠️ **Stale:** the four items added 2026-08-19 (A/B evidence decision, skill-drift fixes, Phase 3
Plan B, carried `audit.py` checks) have had no movement in a month, and the S4 fixture blocker
from 2026-08-21 is unresolved.

## 🧠 Recent decisions

See `decisions.md` (latest entry 2026-09-22). Load-bearing from this session:

- **A separate repo for the product; this one stays the private lab.**
- **Private first; Carter flips public.** Publishing is outward-facing and unreviewed.
- **Mirror ECC's three layers (install once, stamp per project, run per session), not its size.**
- **Two copies of the mode files, on purpose, with a written rule for when they sync.**
- **`new-project.sh` warns about non-repo targets rather than running `git init`** — re-keying
  is silent and the user must choose before the first session.

## 💡 What we learned

- **Porting a personal tool to a generic one is a test of the tool.** `audit.py`'s hardcoded
  container list only became visible as a defect when a stranger's machine was the target;
  taking paths as arguments is simply the better design and the personal copy should follow.
- **Two copies by design need a sync rule written down the day they are created**, or the drift
  is discovered the way every earlier migration here was: months later, silently.
- **Render generated images before shipping them.** The first hero had a label clipped off the
  right edge; headless Chrome caught it in one screenshot.
- **The ECC comparison held both ways.** Its product framing (hero, philosophy line, count table,
  installer, profiles) transferred cleanly; its scale did not need to, and `reference-ecc-kit-
  evaluation` already recorded why its plugin path is untrimmable here.
- Earlier lessons still stand: absence is not evidence; probe before writing a claim into
  multiple files; append-only merges as a union; "unfinished" and "gate-blocked" need the reason
  written down; a skill's staleness is invisible from inside it.

## 📂 Files touched · 🌿 git

**This repo, branch `worktree-close-session-mode-memory` (unmerged; no remote):** `TODO.md`
(+4 lines) · `.claude/memory/decisions.md` (+1 entry) · this file. `main` is at `5604793` (S3),
clean, one worktree (this one).

**Outside this repo:** `~/Projects/mode-memory/` — new git repo, commits `089818e` (0.1.0) and
`b0675c4` (hero), both on `origin/main` at `github.com/ck22coding/mode-memory` (PRIVATE). Native
store: `project-mode-memory-repo.md` + `MEMORY.md` index line. `~/Claude/session-logs/2026-09-22.md`.
No skills were added to `~/.claude/skills/` (tests used a throwaway `HOME`).
