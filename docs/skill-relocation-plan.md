# Skill relocation plan

**Date:** 2026-08-04 · Analysis by a dedicated agent over all 102 real `SKILL.md` files, cross-checked
against real usage counts in `~/.claude/skill-usage.json`. Lead-verified findings marked ✅.

**Why:** skills in `~/.claude/skills/` load into **every session, everywhere**. Skills in a
`.claude/skills/` folder inside a project load **only at or below that folder**. So relocating a
skill out of global costs nothing where it's needed and saves everywhere it isn't.

---

## ⚠️ Fix this first — it has nothing to do with modes

**Seven skills are silently dead.** ✅ They're symlinks pointing at project folders that moved
during the 2026-06-30 reorg. Claude doesn't warn you; they simply stopped existing. Usage history
shows several were in active use before going dark (`411-refine` 12×, `skill-spec-validator` 3×).

Three of four targets are recoverable — the folders moved, they weren't deleted: ✅

| Broken symlink(s) | Old target | Now lives at |
|---|---|---|
| `411-case`, `411-deck`, `411-refine`, `411-reresearch`, `411-research` | `~/Projects/strat-411-skills` | **`~/School/strat-411-skills`** |
| `discovery-call-prep` | `~/Projects/optimal-claude-skills` | **`~/Optimal/optimal-claude-skills`** |
| `skill-compliance`, `skill-factory`, `skill-spec-validator`, `skill-to-spec` | `~/Projects/skill-factory` | **`~/Claude/skill-factory`** |
| `acme-board-memo` | `~/Projects/acme-claude-skills` | **gone — not on disk anywhere** |
| `qa-design-review` | `gstack/qa-design-review` | broken relative link |

Re-point the symlinks and you get those skills back. **You currently believe you have them.**

**Also dead weight:** ✅ `financials`, `slide-deck`, `supply-chain-scan` are empty folders with no
`SKILL.md` at all. Delete. (`_archived/` is correctly parked and not loading — fine as-is.)

**Duplicates:** `browse` / `_gstack-command` / `gstack` carry word-for-word identical descriptions,
as do `connect-chrome` / `open-gstack-browser`. Keep one of each pair.

---

## The size of the prize

| | |
|---|---|
| Native catalog description text | **~25,000–45,000 bytes** depending on how much frontmatter counts |
| Enabled plugin bundles (superpowers 14, ponytail 6, modern-web-guidance 2) | ~6,300 bytes |
| **Loaded every session, regardless of what you're doing** | **roughly 6,000–11,000 tokens** |

*Honest note on the range:* two independent counts disagreed — 24,875 vs 45,354 bytes — because it's
unclear how much frontmatter beyond `description:` actually reaches the catalog. **The percentage
saved is robust even though the absolute number isn't:** the plan below cuts the native catalog by
**~71%**, whatever the true denominator.

---

## STAY GLOBAL — 28 skills

The rule applied: a skill that stays global costs every session forever, but one wrongly demoted is
missing exactly when you reach for it — and you may not remember it exists to reach for. Anything
reflexive, safety-related, or session-lifecycle stays regardless of cost.

- **Session lifecycle:** `close-session` (98 uses), `new-session` (59), `context-save`, `context-restore`
- **Meta / orchestration:** `brain-dump`, `capture-feedback`, `memory-review`, `dream`, `decide`,
  `opusplan`, `day-shift`, `night-shift`, `morning-shift`, `new-project`, `restructure-project`,
  `claude-audit`, `learn`, `locker`
- **Safety:** `careful`, `guard`, `freeze`, `unfreeze`
- **Universal tools:** `browse` (75 uses — your CLAUDE.md hardcodes it as the *only* browsing path,
  so it cannot be mode-gated), `connect-chrome`, `setup-browser-cookies`, `gstack-upgrade`, `codex` (27)

## RESEARCH — gathering

`transcribe-media` · `clean-transcript` · `notion-transcript` · `daily-standup` · `connect-vault` ·
`sources-cited` · `scrape` · `github-digest` · `email-tracker` · `youtube-slide-transcript` ·
`office-hours` *(low confidence — vague description)*

## PLAN — deciding

`spec` · `doc-coauthoring` · `database-design` · `api-design` · `architecture-review` ·
`design-consultation` · `kpi-setter` · `autoplan` · `plan-ceo-review` · `plan-design-review` ·
`plan-devex-review` · `plan-eng-review` · `plan-tune` · `scout-stack` *(bridges research→plan)*

## MAKE — building

`tdd` · `investigate` · `dung` · `mcp-builder` · `skill-creator` · `skillify` · `autoresearch` ·
`ui-ux-pro-max` · `design-html` · `design-review` · `design-shotgun` · `benchmark` ·
`benchmark-models` · `canary` · `health` · `devex-review` · `retro` · `review` · `qa` · `qa-only` ·
`ship` · `land-and-deploy` · `landing-report` · `setup-deploy` · `vercel-deploy-claimable` ·
`document-release` · `document-generate` · `resolve-vulns` · `cso` · `pair-agent` · `setup-gbrain` ·
`sync-gbrain`

## PROJECT-SPECIFIC — one real home, not a mode

- `find-your-level`, `check-understanding` → `~/Projects/ai-engineering/`
- `source-leads` → Optimal AI lead-gen only
- `workout-bot` → its own automation folder; not a coding project at all
- `ios-clean`, `ios-design-review`, `ios-fix`, `ios-qa`, `ios-sync` → **`~/Projects/balkanski/`** ✅
  Identified after the analysis: it's the only project on disk with a native `ios/` directory, and
  it's an Expo + React Native app. These five belong in `balkanski/make/.claude/skills/` — the
  clearest project-specific cluster in the whole catalog, and worth ~5 skills' description text
  removed from every unrelated session.

---

## Your call — the one placement that shouldn't be decided for you

**File-type skills:** `xlsx` (945 bytes — the largest description in the catalog), `docx` (787),
`pptx` (696), `pdf` (437), `make-pdf`. Together **~2,900 bytes, over 10% of the native total.**

They don't belong to an activity, they belong to a *file type*. A PDF turns up mid-research (reading
a source) as often as mid-plan (writing a spec) or mid-make (exporting data). They were provisionally
put in **PLAN** because your decks and memos skew that way — but this one is genuinely yours to
decide, and the cost of getting it wrong is reaching for `xlsx` in the wrong mode and not finding it.

Smaller forced calls, flagged: `design-shotgun` → make (plan/make border), `cso` → make.

---

## Plugins — a separate, riskier lever. Do not do this the same day.

Plugins toggle as whole bundles via `enabledPlugins` in `settings.json`, not per-folder. It is
**unverified** whether a project-level setting can locally re-enable a globally-disabled plugin —
and the P1 finding (loading is additive, never subtractive) suggests it may not work like folder
relocation does. Test in isolation.

- **superpowers — keep global.** `brainstorming` (53 uses) is the second-most-used skill you have
  after `close-session` and `browse`. Exactly the reflexive carve-out.
- **modern-web-guidance — disable.** **Zero recorded uses, ever.** 1,827 bytes buying nothing.
- **ponytail — leave alone for now.** Its always-on behavior comes from a `settings.json` *hook*,
  not the plugin channel, so disabling the plugin may not do what you expect. Separate investigation.

---

## Suggested order

1. **Re-point the seven dead symlinks.** Independent of everything else, recovers skills you think
   you have, minutes of work.
2. **Delete the three empty folders and the duplicate browse/chrome entries.**
3. **Disable `modern-web-guidance`.** Zero uses.
4. **Re-measure the session floor** — this is the number the whole design review hinged on, and it
   was computed against the un-pruned catalog.
5. **Then** relocate by mode, starting with one project, and only if step 4 shows the floor actually
   moved.
