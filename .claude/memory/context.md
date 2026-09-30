# Context — memory-management (updated 2026-09-29)

## 🎯 Goal / KPI

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

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
