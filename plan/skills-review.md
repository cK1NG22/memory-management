# Skills review — 2026-09-24

The 80 skills from `/skills`, in the same order. Put `x` in **Keep** or **Delete**; add a note for maybes.

- **Source** — `claude.ai sync` (account skills), `plugin`, or `local` (`~/.claude/skills/`).
- **Status** — `user-only` = only runs when typed as `/<name>`, never auto-loads.
  `locked by plugin` = can't be removed alone; deleting it means uninstalling the whole plugin.
- **~tok** — listing cost. claude.ai and plugin values are from the `/skills` screen where visible;
  the rest are estimated (description length ÷ 4).

## Name clashes (from the `/skills` footer)

Your local `docx`, `mcp-builder`, `pdf`, `pptx`, `skill-creator`, `xlsx` take the slash command, so
typing `/docx` etc. runs **yours**, not Anthropic's. To use Anthropic's, delete (or rename) the local
one. `/deep-research` is also taken by another command — source not found on disk.

## claude.ai sync

Delete these in claude.ai → Settings → Capabilities, not on disk.

| Keep | Delete | Skill | Status | ~tok |
|---|---|---|---|---|
| [ ] | [ ] | anthropic-skills:deep-research | | 200 |
| [ ] | [ ] | anthropic-skills:docx | clashes with local docx | 320 |
| [ ] | [ ] | anthropic-skills:mcp-builder | clashes with local mcp-builder | 100 |
| [ ] | [ ] | anthropic-skills:pdf | clashes with local pdf | 150 |
| [ ] | [ ] | anthropic-skills:pptx | clashes with local pptx | 330 |
| [ ] | [ ] | anthropic-skills:skill-creator | clashes with local skill-creator | 120 |
| [ ] | [ ] | anthropic-skills:xlsx | clashes with local xlsx | 320 |
| [ ] | [ ] | built-in-browser | | 280 |
| [ ] | [ ] | chrome-browser | | 260 |
| [ ] | [ ] | computer-use | | 320 |
| [ ] | [ ] | docs | | 330 |
| [ ] | [ ] | import-memory | | 60 |
| [ ] | [ ] | morning | | 120 |
| [ ] | [ ] | slack-gif-creator | | 90 |

## Plugin: mattpocock-skills (25)

Whole plugin is one decision. Mark individual rows anyway if it helps you decide.

| Keep | Delete | Skill | Status | ~tok |
|---|---|---|---|---|
| [ ] | [ ] | ask-matt | user-only | 40 |
| [ ] | [ ] | code-review | locked by plugin | 150 |
| [ ] | [ ] | codebase-design | locked by plugin | 100 |
| [ ] | [ ] | diagnosing-bugs | locked by plugin | 60 |
| [ ] | [ ] | domain-modeling | locked by plugin | 80 |
| [ ] | [ ] | grill-me | user-only | 30 |
| [ ] | [ ] | grill-with-docs | user-only | 50 |
| [ ] | [ ] | grilling | locked by plugin | 60 |
| [ ] | [ ] | handoff | user-only | 40 |
| [ ] | [ ] | implement | user-only | 30 |
| [ ] | [ ] | improve-codebase-architecture | user-only | 60 |
| [ ] | [ ] | prototype | locked by plugin | 70 |
| [ ] | [ ] | research | locked by plugin | 90 |
| [ ] | [ ] | resolving-merge-conflicts | locked by plugin | 40 |
| [ ] | [ ] | setup-matt-pocock-skills | user-only | 80 |
| [ ] | [ ] | tdd | locked by plugin | 60 |
| [ ] | [ ] | teach | user-only | ~40 |
| [ ] | [ ] | to-questionnaire | user-only | ~40 |
| [ ] | [ ] | to-spec | user-only | ~50 |
| [ ] | [ ] | to-tickets | user-only | ~75 |
| [ ] | [ ] | triage | user-only | ~50 |
| [ ] | [ ] | wait-what | user-only | ~30 |
| [ ] | [ ] | wayfinder | user-only | ~65 |
| [ ] | [ ] | wizard | locked by plugin | ~85 |
| [ ] | [ ] | writing-for-agents | locked by plugin | ~35 |

## Plugin: ponytail (6)

| Keep | Delete | Skill | Status | ~tok |
|---|---|---|---|---|
| [ ] | [ ] | ponytail | locked by plugin | ~230 |
| [ ] | [ ] | ponytail-audit | locked by plugin | ~110 |
| [ ] | [ ] | ponytail-debt | locked by plugin | ~105 |
| [ ] | [ ] | ponytail-gain | locked by plugin | ~85 |
| [ ] | [ ] | ponytail-help | locked by plugin | ~60 |
| [ ] | [ ] | ponytail-review | locked by plugin | ~125 |

## Plugin: supabase (1)

| Keep | Delete | Skill | Status | ~tok |
|---|---|---|---|---|
| [ ] | [ ] | supabase | locked by plugin | ~145 |

## Local — `~/.claude/skills/` (34)

Each one can be deleted on its own.

| Keep | Delete | Skill | Status | ~tok |
|---|---|---|---|---|
| [ ] | [ ] | api-design | | ~40 |
| [ ] | [ ] | architecture-review | user-only | ~45 |
| [ ] | [ ] | blocksite | | ~85 |
| [ ] | [ ] | capture-feedback | | ~50 |
| [ ] | [ ] | clean-transcript | | ~45 |
| [ ] | [ ] | close-session | user-only | ~75 |
| [ ] | [ ] | database-design | | ~90 |
| [ ] | [ ] | day-shift | | ~70 |
| [ ] | [ ] | doc-coauthoring | | ~105 |
| [ ] | [ ] | docx | clashes with anthropic-skills:docx | ~60 |
| [ ] | [ ] | dream | | ~70 |
| [ ] | [ ] | email-tracker | | ~85 |
| [ ] | [ ] | equationify | user-only | ~35 |
| [ ] | [ ] | fill-notes | | ~60 |
| [ ] | [ ] | find-docs | | ~225 |
| [ ] | [ ] | github-digest | | ~50 |
| [ ] | [ ] | mcp-builder | clashes with anthropic-skills:mcp-builder | ~70 |
| [ ] | [ ] | memory-review | user-only | ~55 |
| [ ] | [ ] | morning-shift | | ~75 |
| [ ] | [ ] | new-project | user-only | ~140 |
| [ ] | [ ] | new-session | user-only | ~155 |
| [ ] | [ ] | night-shift | | ~90 |
| [ ] | [ ] | pdf | clashes with anthropic-skills:pdf | ~35 |
| [ ] | [ ] | pptx | clashes with anthropic-skills:pptx | ~55 |
| [ ] | [ ] | resolve-vulns | user-only | ~100 |
| [ ] | [ ] | restructure-project | user-only | ~155 |
| [ ] | [ ] | skill-creator | clashes with anthropic-skills:skill-creator | ~80 |
| [ ] | [ ] | supplement | | ~80 |
| [ ] | [ ] | todos | user-only, no description | 0 |
| [ ] | [ ] | transcribe-media | | ~65 |
| [ ] | [ ] | ui-ux-pro-max | | ~50 |
| [ ] | [ ] | write-doc | | ~65 |
| [ ] | [ ] | xlsx | clashes with anthropic-skills:xlsx | ~65 |
| [ ] | [ ] | youtube-slide-transcript | user-only | ~155 |

## Not in `/skills` (for reference)

- **Installed but disabled plugins:** modern-web-guidance (2 skills), vercel (~40 skills). Uninstall
  with `/plugin` if you don't want them on disk.
- **mattpocock folders the plugin doesn't register** (10): claude-handoff, loop-me,
  setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape, git-guardrails-claude-code,
  migrate-to-shoehorn, scaffold-exercises, setup-pre-commit. They never load.
- **Built into Claude Code** (dataviz, artifact-*, loop, schedule, code-review, simplify, etc.) —
  not listed by `/skills`, not removable.
