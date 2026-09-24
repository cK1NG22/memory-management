# Context — memory-management (updated 2026-09-23)

*Built on the 2026-09-22 close, which lives on the unmerged branch `worktree-close-session-mode-memory`.
This version folds that content in, so taking this file resolves that branch's `context.md` conflict.*

## 🎯 Goal / KPI

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**2026-09-23 was a pruning day.** gstack is gone (54 skills; only `browse` was ever used), Arc is
gone, and the browser roles are ruled (agent-browser general, Chrome DevTools debugging, Playwright
E2E, Claude in Chrome backup). A measured usage count then drove a plugin and skill cleanup:
superpowers, company-preview, market-jumpstart and mana uninstalled; data/product-management
disabled locally; the local skills cut to 36 through Carter's per-skill comments on the
"Skill Ledger" review page (`~/Claude/skill-review-2026-09-23/`). Records: `decisions.md` 2026-09-23
(three entries); native `project-gstack-removed.md` and `project-plugin-cleanup.md`.

**The setup also exists as a product (2026-09-22):** `~/Projects/products/mode-memory` →
`ck22coding/mode-memory`, private until Carter flips it. The mode files now have two copies by
design (`~/.claude/modes/` personal and live; `mode-memory/modes/` generic and shipped), and the
public ALWAYS.md has already drifted (TODO).

**Still true and load-bearing:** transcripts key to the launch cwd; native memory keys to the
**main repo root** even inside a worktree (`git rev-parse --path-format=absolute --git-common-dir`
minus `/.git`). S3's §4 stop-gate is closed; **S4 is blocked** on the missing
`~/Sandbox/skill-budget-ab-fixture`.

## ⏭️ Next steps / open

The root `TODO.md` is the live list (17 open). Carter-owned:
- Rule on ponytail, mattpocock, supabase. (data/product-management removed in claude.ai 2026-09-23.)
- Review and flip `mode-memory` public.

⚠️ **Stale:** the four items added 2026-08-19 (A/B evidence, skill-drift fixes, Phase 3 Plan B,
carried `audit.py` checks) have not moved in over a month; the S4 fixture blocker has been open
since 2026-08-21.

## 🧠 Recent decisions

See `decisions.md`. Load-bearing:
- **Count usage from three sources, never one.** The hook log misses typed commands, transcripts
  are purged, `pluginUsage` counts hook fires.
- **Old builds live on GitHub or in `~/Projects/Archive/`, never in `~/.claude/skills/`**, so they
  cannot be called.
- **decide and file-versioning are always-loaded rules now**; decide is scoped so its "never launch"
  binds only a decide pass.
- **Browser roles:** agent-browser / Chrome DevTools / Playwright / Claude in Chrome.
- **mode-memory ships private first; Carter flips public.**

## 💡 What we learned

- **A usage counter can measure the wrong thing.** Ponytail's 8,036 were hook fires; its skill ran
  13 times. Split "skill called" from "hook fired" in any audit.
- **Moving an instruction changes its meaning.** Text written for an invoked skill becomes a global
  order once it sits in always-loaded rules; recheck scope on every skill↔rule↔reference move.
- **Delete by dependency, not by folder.** scout-stack was referenced from CLAUDE.md itself;
  deleting the folder alone would have left an always-on rule pointing at nothing.
- **Folder dates lie after a reorganization** (20 skill folders share 2026-03-16);
  `~/.claude/history.jsonl` kept the real install commands.
- **Test hooks on a scratch `HOME` before wiring them**: a jq syntax error would have silently
  dropped every typed command.
- Earlier lessons still stand: absence is not evidence; probe before writing a claim into
  multiple files; two copies by design need a written sync rule the day they are created.

## 📂 Files touched · 🌿 git

**This repo:** `TODO.md`, `.claude/memory/decisions.md`, this file, `plan/ecc-decisions.md`.
The 09-22 and 09-23 close branches are both merged into `main` (no remote).

**Outside this repo:** `~/.claude/settings.json` (hooks), `~/.claude/hooks/track-skill-usage.sh`,
`~/.claude/rules/{decide,file-versioning}.md`, `~/.claude/modes/{ALWAYS,PLAN-MODE}.md`,
`~/.claude/CLAUDE.md`, `~/.claude/skills/` (46 → 36), plugin registry; `strat-411-skills` PR #1
merged; native store `project-plugin-cleanup.md`; review files in `~/Claude/skill-review-2026-09-23/`;
Trash holds every removed skill, hook, plugin cache, Arc and Chromium 1234.
