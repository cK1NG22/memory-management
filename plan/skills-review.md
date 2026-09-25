# Skills review — 2026-09-24

Mark each row: put `x` in **Keep** or **Delete**. Leave a note if it's a maybe.

Source: `~/.claude/skills/`, `~/.claude/plugins/installed_plugins.json`, and the skill listing loaded
this session. (The `/skills` screen itself printed nothing to capture.)

## Local skills — `~/.claude/skills/` (auto-invoke on)

Claude can load these on its own when the description matches.

| Keep | Delete | Skill | What it does |
|---|---|---|---|
| [ ] | [ ] | api-design | Design/review REST or GraphQL APIs |
| [ ] | [ ] | blocksite | Block/unblock a site via /etc/hosts daemon |
| [ ] | [ ] | capture-feedback | Save a correction/rule as durable feedback |
| [ ] | [ ] | clean-transcript | Strip filler from meeting transcripts |
| [ ] | [ ] | database-design | Schema design, normalization, indexing |
| [ ] | [ ] | day-shift | Sprint plans + tonight's task cards |
| [ ] | [ ] | doc-coauthoring | Structured doc co-writing workflow |
| [ ] | [ ] | docx | Word documents |
| [ ] | [ ] | dream | Consolidate memory from the day's transcripts |
| [ ] | [ ] | email-tracker | Newsletter + Claude blog triage → Slack |
| [ ] | [ ] | fill-notes | ACC 241 — lesson notes from videos (stage 2) |
| [ ] | [ ] | find-docs | Current library docs (context7) |
| [ ] | [ ] | github-digest | GitHub trending digest → Slack |
| [ ] | [ ] | mcp-builder | Build MCP servers |
| [ ] | [ ] | morning-shift | Review overnight runs, merge or reject |
| [ ] | [ ] | night-shift | Launch the overnight queue |
| [ ] | [ ] | pdf | PDF files |
| [ ] | [ ] | pptx | PowerPoint files |
| [ ] | [ ] | skill-creator | Create/edit/eval skills |
| [ ] | [ ] | supplement | ACC 241 — reading notes into KCO.md (stage 4) |
| [ ] | [ ] | transcribe-media | Local video/audio transcription |
| [ ] | [ ] | ui-ux-pro-max | UI/UX design and review |
| [ ] | [ ] | write-doc | ACC 241 — KCO.md into Google Doc (stage 5) |
| [ ] | [ ] | xlsx | Spreadsheets |

## Local skills — slash-command only (`disable-model-invocation: true`)

These never auto-load; they only run when you type `/<name>`.

| Keep | Delete | Skill | What it does |
|---|---|---|---|
| [ ] | [ ] | architecture-review | Review architecture: scalability, resilience, security |
| [ ] | [ ] | close-session | End-of-session progress + memory update |
| [ ] | [ ] | equationify | Rewrite a study file into rules/tables/sequences |
| [ ] | [ ] | memory-review | Walk through and trim memory files |
| [ ] | [ ] | new-project | Scaffold CLAUDE.md, ADR templates for a project |
| [ ] | [ ] | new-session | Hand off to a fresh session in Agent View |
| [ ] | [ ] | resolve-vulns | Fix supply-chain vulns from the daily scan |
| [ ] | [ ] | restructure-project | Reshape a folder into the COS container shape |
| [ ] | [ ] | todos | (no description in SKILL.md) |
| [ ] | [ ] | youtube-slide-transcript | Slide-aware transcript of a talk video |

## Plugins

Delete here = uninstall the whole plugin (plugin skills can't be trimmed one by one).

| Keep | Delete | Plugin | Status | Skills |
|---|---|---|---|---|
| [ ] | [ ] | mattpocock-skills | enabled | diagnosing-bugs, tdd, prototype, research, domain-modeling, codebase-design, code-review, resolving-merge-conflicts, wizard, grilling, writing-for-agents |
| [ ] | [ ] | ponytail | enabled | ponytail, ponytail-audit, ponytail-debt, ponytail-gain, ponytail-help, ponytail-review |
| [ ] | [ ] | supabase | enabled | supabase |
| [ ] | [ ] | modern-web-guidance (googlechrome) | installed, **disabled** | — |
| [ ] | [ ] | vercel | installed, **disabled** | — |

## Not removable from here (for reference)

- **Built into Claude Code:** dataviz, artifact-design, artifact-diagramming, artifact-capabilities,
  update-config, keybindings-help, code-review, simplify, fewer-permission-prompts, loop, schedule,
  claude-api, workflow-authoring, claude-in-chrome, run, init, security-review.
- **claude.ai account skills (`anthropic-skills:`):** built-in-browser, chrome-browser, computer-use,
  deep-research, docs, docx, import-memory, mcp-builder, morning, pdf, pptx, skill-creator,
  slack-gif-creator, xlsx — managed in claude.ai settings, not on disk.

## Duplicates to check while marking

- `docx`, `pdf`, `pptx`, `xlsx`, `mcp-builder`, `skill-creator` exist both locally and as
  `anthropic-skills:`. Per [[feedback-prefer-managed-plugin-skills]], the managed copy usually wins.
