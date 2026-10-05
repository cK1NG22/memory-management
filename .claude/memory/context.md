# Context — memory-management (updated 2026-10-04)

## 🎯 Goal / KPI

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**2026-10-04 — mode principles became rule files (merged to `main` by PR #2 the same day).** Each
project now holds real copies in `<mode>/.claude/rules/`, sourced from `make/modes/library/`; the
symlink + `@import` wiring is gone from this repo. `make/modes/modes.py` stamps, sorts and checks;
`/modes` is the skill. `audit.py` reported clean on main after the merge. Open follow-ups are in
`TODO.md`. How-to: `docs/mode-files-runbook.md`.

**2026-10-04, later — the mode loop is designed, not built.** Carter ruled the shape (full entry
in `decisions.md`): the built-in auto-memory captures feedback → a dreamer harvests the native
stores → one source file per mode that nothing auto-loads → copied into every project's mode
rules on each source edit. `capture-feedback` is to be retired. The plugin becomes a "middleman":
a non-loading folder that holds other plugins, with skills that sort their pieces into mode
folders and one that moves globally installed plugins into it.

*Built on the branch so far:* stamp, check, list, place, the `/modes` skill, the audit check, this
repo restamped. *Built and now contradicted by the rulings:* `check`/`stamp` report a differing
copy and wait — they should overwrite it; the library sits in `make/modes/library/`, a home Carter
has not ruled on. *Not built:* the copy-on-edit trigger, the list of stamped projects, the
dreamer, the tracking record, the plugin-mover skill, the plugin packaging.

*Proposed by the session for the tracking record, not ruled:* native stores are not git repos, so
"commits since the last run" does not apply to them — the signal is file change. Keep one record
(path → content hash → state) written by the dreamer. Before any model call a script walks the
stores' `feedback` files: unknown path = new feedback; known path with a changed hash = the
built-in writer updated an existing memory, which is how repeat feedback inside one project shows
up (it edits the old file instead of adding one). Nothing new or changed → no agent runs. The
mode comes from `originSessionId` → the launch folder recorded in `~/.claude/history.jsonl`
(43 of 43 IDs found; transcripts gave only 6). Carter agreed to the script gate.

**The map of the whole setup is `plan/mode-loop-map.md`** — two products (middleman, mode loop),
the loop step by step, each line tagged ruled / measured / proposed / open.
`plan/middleman-map.md` is the middleman's own process: install → setup → compliance → scaffold →
the split (whole plugin = switch it on in that folder's settings; part = copy pieces). Later rulings the
same day: deliver both ways (`enabledPlugins` per mode folder and copied pieces); the user picks
the middleman folder's home; memory is a setting (off / propose / apply); promote at 2 or 3
recurrences; the dreamer drops redundant feedback, may mine Carter's prompts, and harvests only
projects with mode folders (two today).

**2026-10-04, after the merge — the "slice" idea, probed, not ruled.** `enabledPlugins` is on/off
per plugin id; the manifest decides the pieces. A local marketplace can hold small plugins
("slices") that list only chosen pieces and link into a held copy of the upstream plugin; each is
switched on per mode folder. Probes on a throwaway marketplace: listed pieces only, links into the
held copy load, hooks follow the slice, edits carry through, registering writes two global
entries and removing restores them. Drawn in `plan/middleman-map.md` section 5; results and what
is still unmeasured in `decisions.md`.

**2026-09-29 — ECC went live as a library.** The fork `ck22coding/ECC` is cloned at `ecc/`
(gitignored, own repo). First build: eightfaces (Scott Murff's repo, local-only via
`.git/info/exclude`) got the developer profile minus hooks — 68 agents, 94 commands, 117 skills
as symlinks; rules wait on the stack. Probed: symlinked agents and commands load. Carter: symlinks
are optional, and plugin-path commands get fixed in the fork. How-to: `docs/ecc-runbook.md`.

**ECC adoption has a shape (2026-09-29): the "library" model, from Carter's own fork
`ck22coding/ECC`.** No plugin, no install profile. The fork is cut to Claude-only core in two merged
PRs (1,884 + 765 files dropped; 1,348 remain): skills, commands, agents, rules, hooks, plus the
`scripts/`, `config/`, `workflows/`, `manifests/` they depend on. Projects will get hand-picked
pieces at scaffold time. Records: `decisions.md` 2026-09-28 and 2026-09-29; `plan/ecc-decisions.md`
rows 1–3; native `reference-ecc-kit-evaluation.md`.

**The 09-28 probes set the scaffold rules:** skills follow symlinks (can track the fork), rules
skip symlinks (must be real copies); a mode folder's `.claude/` loads only when the session starts
there; `~/.claude/rules/` subfolders load everywhere. ECC's minimal profile ≈ +23k tokens/session.

**Git:** both 2026-09-29 ECC branches merged into `main` and pushed to `ck22coding/memory-management`.

## ⏭️ Next steps / open

The root `TODO.md` is the live list. ECC-next:
- Fix the 26 commands and ~14 skills that call plugin paths, in the fork.
- eightfaces: cut to the confirmed stack 2026-09-29 (see decisions.md). Open: `common/testing.md`, symlink vs copy, measure the skill-listing budget.
- Carter decides: `docs/`, `scripts/` trim, `examples/`, `.mcp.json` in the fork.
- Remaining ECC rows (5–16, 30–32, 35–36) still carry Carter's open questions.

⚠️ **Stale:** the four items added 2026-08-19 (A/B evidence, skill-drift fixes, Phase 3 Plan B,
carried `audit.py` checks) — six weeks without movement; the S4 fixture blocker since 2026-08-21.

## 🧠 Recent decisions

See `decisions.md`. Load-bearing:
- **ECC = hand-picked library from the fork**, not plugin or profile (2026-09-29).
- **No ECC hooks; close-session stays the resume mechanism; no Codex sync; global CLAUDE.md kept** (2026-09-28).
- **Drop groups merged with merge commits**, so each can be reverted alone.
- **Count usage from three sources, never one** (2026-09-23).
- **Browser roles:** agent-browser / Chrome DevTools / Playwright / Claude in Chrome.

## 💡 What we learned

- **Rules and skills load differently through symlinks.** A library can keep skills live
  (symlink) but rules freeze at copy time — so rules need a deliberate re-copy step.
- **"Minimal profile" was not minimal.** Reading the manifests showed the whole rules tree, 68
  agents and 94 commands; measure the real install, not the label.
- **Hooks are the one core type that isn't self-contained** — keeping hooks means keeping
  `scripts/hooks`, `scripts/lib` and `package.json`.
- **Deleting from a fork raises the price of every upstream sync** (modify/delete conflicts);
  folders upstream rarely touches are cheap to drop, busy ones are not.
- **A deleted file can still load you**: ECC's own `.claude/` and `CLAUDE.md` would have loaded
  into any session opened in the library folder.

## 📂 Files touched · 🌿 git

**This repo:** `plan/ecc-decisions.md`, `plan/ecc-hiw.md`, `.claude/memory/{decisions,context}.md`,
`TODO.md`. Merged + pushed through `571e653`; this close is on branch
`worktree-close-session-ecc-library`.

**Outside this repo:** fork `ck22coding/ECC` (PRs #1 `b2d2ede4`, #2 `a0e8a663`); native store
`reference-claude-code-loading-mechanics.md`, `reference-ecc-kit-evaluation.md`, `MEMORY.md`;
`~/Claude/session-logs/thinking-patterns.md`.
