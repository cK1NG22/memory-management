# ECC adoption: 36 decisions

- **ECC** = affaan-m/ecc v2.2.2 (2026-09-15), https://github.com/affaan-m/ecc. Paths are relative
  to that repo unless they start with `~`. The trace clone is gone, so re-clone or read on GitHub.
- **Traced** 2026-09-21 · **Carter answered** 2026-09-22 · **Trimmed** 2026-09-23 after the plugin
  and skill cleanup (`.claude/memory/decisions.md`). Carter's verbatim answers, and rows about
  removed skills, are in `plan/_archive/ecc-decisions_2026-09-23.md`.
- **Updated 2026-09-28** for the 09-24 cleanup: mattpocock-skills and ponytail uninstalled; local
  `api-design`, `database-design`, `new-session` gone. Supabase is the only third-party plugin left.
- **Related:** `plan/skill-budget-ab.md`, `plan/trim-skills.md`, memory `reference-ecc-kit-evaluation`.

## Status

| # | Decision | Carter | Blocked on |
|---|---|---|---|
| 1 | Install as the `ecc@ecc` plugin | Compare with current skills first; will drop plugins that ECC beats | — (table refreshed 09-28) |
| 2 | Copy in a chosen subset with `install.sh --target claude` | Most likely path; goes with item 1 | item 1 |
| 3 | Add about 93k chars to the skill listing | Pending; depends on item 1 | item 1; headroom needs re-measuring |
| 4 | Keep his api-design next to ECC's | **Moot** — his api-design is gone; ECC's is a plain add-or-not under item 2 | — |
| 5 | Add 68 agents | Accept once he knows what they do; **measured +7,179 tokens/session** | — |
| 6 | Add 94 `/ecc:` commands | Asked what replaced them | — |
| 7 | Copy in `rules/common` | Wants the token cost; will read every file | reading the 10 files (probe done: loads) |
| 8 | Agents invoked automatically | OK: they are agents, not skills | — |
| 9 | 80% coverage, TDD on every change | TDD ≠ over-engineering; conformance-suite-first still fits | — |
| 10 | ECC's model table | Would consider it; subagent-heavy work fits it | — |
| 11 | Search order: GitHub → Context7 → Exa → agents | **Accept**; reuse reference files as ideas to distil | — |
| 12 | Conventional commits | **Accept** | — |
| 13 | Immutability, function and file size limits | Investigate; ponytail test skipped (ponytail removed) | reading coding-style.md under item 7 |
| 14 | `includeCoAuthoredBy: false` | No "co-authored by ECC"; "co-authored by Claude Code" is fine | — |
| 15 | `pluginConfigs` options | Asked what it does | — |
| 16 | ECC's settings recommendations | Asked what changes | — |
| 17 | Merge `~/.claude/CLAUDE.md` with ECC's example | **No** — global CLAUDE.md kept as is (09-28) | — |
| 18 | Hook profile | **No hooks** (09-28) | — |
| 19–29 | Individual hooks | **No hooks** (09-28) | — |
| 30 | Instincts | Asked what instincts are | — |
| 31 | Promoted instincts become local skills | Leaning toward promoting by hand | — |
| 32 | unified-memory | Leaning away | — |
| 33 | session-data as the resume mechanism | **Keep close-session** — session-data needs hooks, and hooks are out (09-28) | — |
| 34 | Sync ECC into Codex | **No** (09-28) | — |
| 35 | Catalog MCP servers | Asked what they are | — |
| 36 | `contexts/` shell aliases | Wants a comparison | — |

## Measurements 2026-09-28 (CLI 2.1.284, ECC 2.2.2 @ d3b8a3e)

Method: headless `claude -p --model sonnet`, a fresh repo per variant, ECC files copied into the
project's `.claude/`; total input tokens (input + cache) for "Reply OK." Both runs were identical
for every row. Nothing under `~/.claude` touched. ECC's installer was **not** run (the auto-mode
classifier blocks executing it), so profile contents come from reading
`manifests/install-profiles.json` and `scripts/lib/install-targets/claude-*.js`.

| Added to a project | Tokens/session | Δ vs baseline |
|---|---|---|
| nothing (baseline) | 34,856 | — |
| 68 agents | 42,035 | +7,179 |
| 94 commands | 38,002 | +3,146 |
| 47 `workflow-quality` skills | 37,802 | +2,946 |
| full `rules/` tree (122 files; 111 have `paths:` frontmatter) | 44,654 | +9,798 |

- **`--profile minimal`** = rules-core + agents-core + commands-core + platform-configs +
  workflow-quality, no hooks. rules-core maps the whole `rules/` tree to `.claude/rules/ecc/`
  (no language filter). platform-configs drops `.claude-plugin`, `.codex`, `.cursor`, `.gemini`,
  `mcp-configs`, … into the target root. Sum of the four rows ≈ **+23,000 tokens/session** (not
  measured together).
- Profiles are the **file-copy path**, not the plugin. `--target claude-project` installs into one
  project's `.claude/` instead of `~/.claude/`.
- `--with` / `--without` adjust a profile by module; the unit is a module, not a file.
  `--skills a,b` picks single skills. The bare-language form (`install.sh typescript`) copies
  `rules/common` + one language but can't be combined with `--profile`.

Loading probes (same method, sentinel strings, 2/2 runs each):

| Setup | cwd = project root | cwd = `make/` |
|---|---|---|
| `<project>/.claude/rules/x.md` | loads | loads |
| `<project>/make/.claude/rules/x.md` | **no** | loads |
| `<project>/make/.claude/skills/s/` | **no** | loads |
| `make/.claude/skills/s` → symlink to a library folder | — | loads |
| `.claude/rules/x.md` → symlink to a library file | — | **no** |
| `.claude/rules/dir` → symlink to a library folder | **no** | — |
| `~/.claude/rules/ecc/x.md` (real subfolder) | loads | — |

- Rules **skip symlinks** (file and folder); skills follow them.

---

## Install shape

### 1. Plugin install: your skills compared with ECC's

| Yours | ECC | Fit |
|---|---|---|
| built-in `/code-review`, anthropic-skills deep-research | code-reviewer agent, `deep-research`, `research-ops` | Close; yours are bundled and cost no listing budget |
| (nothing — mattpocock uninstalled 09-24) | `tdd-workflow` + tdd-guide agent | ECC fills a gap |
| (nothing — ponytail uninstalled 09-24) | code-simplifier agent, `refactor-cleaner`, KISS/YAGNI in coding-style.md | ECC fills a gap → item 13 |
| dream, morning/day/night-shift | continuous-learning-v2, loop-operator agent, `autonomous-loops` | Different shape → items 24, 30 |
| capture-feedback | instincts + `/ecc:learn` | → item 30 |
| close-session | `/ecc:save-session`, `/ecc:checkpoint` | → item 33 |
| anthropic-skills mcp-builder, skill-creator; supabase plugin | `mcp-server-patterns`, `/ecc:skill-create`, `postgres-patterns` + `database-migrations` | Yours are bundled; ECC's would add listing cost |
| (nothing — api-design, database-design gone) | `api-design` | Add-or-not under item 2 |
| blocksite, email-tracker, github-digest, weekly-update, transcribe-media, clean-transcript, financials, slide-deck, … | — | Personal workflows; no overlap |
| anthropic-skills (bundled) | — | Don't count toward the listing budget |

- Those plugins are already dropped, and the plugin path (292 skills + 94 commands) still can't fit.
  Only a file-copy subset fits (item 2).

### 2. Copy in a subset with `install.sh --target claude`

How it works, from `scripts/lib/install/`:

- `--skills a,b,c` = install only the named skills. `--profile <p>` = install a set of modules,
  adjusted with `--with` / `--without`. `--dry-run` = print every write without making it.
- IF the `platform-configs` module is included THEN `plugin.json`, `marketplace.json`, `README.md`,
  `AGENTS.md` and `docs/` get written into the `~/.claude/` root. A `--skills` list with no
  modules leaves it out.
- Skills are copied to `~/.claude/skills/<name>/` as local skills, so `skillOverrides` and
  usage-based trimming work on them. They don't work on the plugin path.
- Ledger = `~/.claude/ecc/install-state.json`, which records every file ECC created. Reinstalling
  skips any file not in the ledger. `node scripts/ecc.js list-installed | doctor | repair` works
  from it.
- Upgrade = re-run the installer from a newer checkout. There is no auto-update.
- This is vendoring. ALWAYS.md forbids vendoring because copies freeze; the ledger makes the copy
  upgradeable, which reduces that risk but doesn't make it an exception.

Steps: 1. Finish item 1 → 2. Pick the ECC skills that win → 3. Run `--skills <list> --dry-run` →
4. Confirm nothing is written to the `~/.claude/` root → 5. Install.

### 3. Skill listing budget

| | Chars |
|---|---|
| Listing budget, default model (measured) | ~30,000 |
| Catalog on 2026-08-07 (130 skills) | 35,948 |
| Catalog on 2026-09-23 (69 skills) | 28,523 |
| ECC's 292 skill descriptions, with the per-entry cap applied | ~83,400 |
| ECC's 94 command descriptions | ~10,000 |

- IF the catalog is over budget THEN the extra entries show as bare names, with no warning, AND a bare
  name can't be triggered by a plain-language request.
- The plugin path has no trimming lever: `plugin.json` exposes only `hooks_enabled` and
  `hook_profile`. The item 2 `--skills` list is the only way to trim. The A/B method for checking
  which skills drop out is in `plan/trim-skills.md` and `plan/skill-budget-ab.md`.
- Headroom = 30,000 − 28,523 ≈ 1,500 chars. An ECC skill averages 83,400 / 292 ≈ 285 chars, so
  about 5 ECC skills fit.
- IF the model has 200K context (budget ≈ 8,000 chars) THEN the current catalog is already ≈ 3.5×
  over budget.
- [stale 09-28] 31 plugin skills (mattpocock 25, ponytail 6) and several local skills were removed
  after this count, so headroom is larger than 1,500. Re-measure before sizing a subset.
- 69 = 48 local skills + 32 plugin skills (mattpocock 25, ponytail 6, supabase 1) − the skills
  hidden from the listing. The 40 bundled Anthropic skills don't count. The loader still reads the
  8 skills in `~/.claude/skills/_archived/` as live.

How it was measured: 1. Run a headless `claude -p` from a neutral folder with
`--settings '{"skillListingBudgetFraction":0.0005}'` → 2. The loader prints
`69 skills, 28523 chars > 1500 budget` → 3. Run again at the default budget → no warning, so the
catalog fits.

### 4. api-design: yours compared with ECC's

Files: `~/.claude/skills/api-design/SKILL.md` and ECC's `skills/api-design/SKILL.md`. ECC's
`benchmark` has no local counterpart left to compare.

| | Yours | ECC |
|---|---|---|
| Size | 1.5 KB | 13.2 KB |
| Scope | REST + GraphQL | REST only |
| Shape | Principles, when/when-not, instructions, pointer to resources | 11 sections: resources, HTTP methods and status codes, response format, pagination, filter/sort/search, auth, rate limits, versioning, implementation |
| Frontmatter | `allowed-tools`: Read, Glob, Grep, Bash, Agent | none |

IF you want the full reference text in context when the skill fires THEN ECC's fits. IF you want a
short pointer THEN yours fits.

### 5. 68 agents

Model shown only where it isn't sonnet.

| Group | # | Agents |
|---|---|---|
| Core workflow | 18 | planner (opus), architect (opus), code-reviewer, security-reviewer, tdd-guide, build-error-resolver, e2e-runner, refactor-cleaner, doc-updater (haiku), code-simplifier, code-architect, code-explorer, performance-optimizer, silent-failure-hunter, type-design-analyzer, comment-analyzer (haiku), pr-test-analyzer, docs-lookup (haiku, Context7) |
| Language reviewers | 21 | cpp, csharp, django, fastapi, flutter, fsharp, go, java, kotlin, php, python, react, rust, swift, typescript, vue, harmonyos-app-resolver, database (Postgres), mle, rag-pipeline, healthcare (opus) |
| Build resolvers | 10 | cpp, dart, django, go, java, kotlin, pytorch, react, rust, swift |
| Orchestration and meta | 8 | gan-planner / generator / evaluator (a spec → build → test loop), agent-evaluator (5-axis rubric), harness-optimizer (tunes config against evals), loop-operator, conversation-analyzer (haiku; finds behaviours worth a hook), spec-miner (opus) |
| Domain and business | 11 | chief-of-staff (email/Slack triage), marketing-agent, seo-specialist, a11y-architect, homelab-architect, network-architect, network-config-reviewer, network-troubleshooter, opensource-forker (haiku), opensource-packager (haiku), opensource-sanitizer |

- Most descriptions say "Use PROACTIVELY", which pushes Claude to call them automatically (item 8).
- All 68 appear in the Agent tool's type list every session, in addition to Carter's 7 and the
  built-in agents.

### 6. 94 `/ecc:` commands

- Skills replaced the commands. ECC's own text says commands are "convenient entry points" and
  "the durable logic should live in skills."
- 34 of the 94 hand off to a skill explicitly, for example `/ecc:plan` → `plan-orchestrate` + the
  planner agent, `/ecc:code-review` → the code-reviewer agent, `/ecc:save-session` → session-data
  (item 33).
- The older shims (`/tdd`, `/eval`, `/verify`) sit in `legacy-command-shims/` and don't load unless
  copied in by hand.
- The 94 that do load cost ≈ 10,000 listing chars.

---

## Instructions and settings

### 7. `rules/common` → `~/.claude/rules/ecc/common/`

| File | Bytes | ≈Tokens | Content |
|---|---|---|---|
| agents.md | 2,800 | 700 | Agent roster, "immediate agent usage", running in parallel, delegation contract |
| code-review.md | 3,600 | 900 | When to review, checklist, severity levels, 80% coverage |
| coding-style.md | 3,000 | 750 | Immutability, KISS/DRY/YAGNI, file sizes, error handling, naming |
| development-workflow.md | 2,200 | 550 | Research → plan → TDD → review → commit |
| performance.md | 1,600 | 400 | Model table, context management, extended thinking |
| testing.md | 1,400 | 350 | 80% coverage, three test types, TDD steps, AAA pattern |
| patterns.md | 1,000 | 250 | Skeleton projects, repository pattern, API response envelope |
| security.md | 860 | 215 | Pre-commit checklist, secret handling, incident response |
| git-workflow.md | 840 | 210 | Conventional commits, PR workflow, the `includeCoAuthoredBy` note |
| hooks.md | 770 | 190 | Hook types, caution on auto-accept, TodoWrite advice |
| **Total** | **18,100** | **≈4,500** | |

- Skill = loads when it fires. Rule = loads in every session, in every project.
- The harness reads subfolders of `~/.claude/rules/` (probe 2026-09-28, 2/2 sonnet runs quoted a
  random sentinel from `rules/ecc/probe.md`; control at `rules/` top level also loaded). So the cost
  is ≈ 4,500 tokens per session, every session, every project.
- Probe: 1. Write a marker file to `~/.claude/rules/ecc/test.md` → 2. Run a headless session and
  check whether the marker loads → 3. Delete the file. This is the method from
  `reference-claude-code-loading-mechanics`.
- Each language pack adds 5–8 files; the full tree is 122 files, 286 KB. Copy at most one pack.

### 8. Agents invoked automatically

- Skill = loads into the main context. Agent = runs in its own context and returns a report. So
  this rule costs subagent calls, not main-context tokens.
- IF ECC's trigger "complex feature request → planner" is adopted THEN it conflicts with
  CLAUDE.md's "a direct question gets a direct answer" UNLESS CLAUDE.md says which requests are
  exempt.
- The "Use PROACTIVELY" descriptions (item 5) push the same way even without this rule.

### 9. 80% coverage, three test types, TDD on every change

- Nothing in ECC's hooks enforces 80%. `quality-gate.js` only runs formatters and linters.
  Coverage is checked only when `/ecc:test-coverage` or the tdd-guide agent runs, so the 80% is
  instruction text, not a gate.
- ECC has no idea of conformance suites. The PLAN-MODE rule sits on top of ECC's with no conflict,
  and suite runs count toward whatever coverage number applies.

### 10. Model table

- The tiers match `Model-Configuration-Guide`; the model names are out of date. ECC "Haiku" =
  Haiku 4.5, "Sonnet" = Sonnet 5 or 4.6, "Opus" = Opus 4.8. Fable sits above the table.
- ECC's pins: 58 sonnet, 6 haiku, 4 opus (planner, architect, spec-miner, healthcare-reviewer).

| Role | ECC | Carter's dev pipeline |
|---|---|---|
| Implementation | — | Implementer: opus |
| QA | e2e-runner: sonnet | QA Runner: sonnet |
| Final review | code-reviewer, security-reviewer: sonnet | Merge-Gate Reviewer: opus |

- To change a plugin agent's model, copy its file into `~/.claude/agents/` with a different pin.
  That makes it a fork.
- ECC assumes delegation throughout: rules/agents.md, the 68 agents and the `orch-*` commands.

### 11. Search order: GitHub → Context7 → Exa → agents

- Exa = a neural web-search API (exa.ai). ECC uses it through the opt-in `exa-web-search` MCP
  server (needs a paid `EXA_API_KEY`) and the `exa-search` skill.
- ECC's order is about finding existing code before writing new code. Carter's local-files-first
  rule is about answering from his own notes before searching the web. The two don't collide.
- For the reference-file idea: ECC's `rules-distill` pulls shared principles out of skills into
  rule files, and `search-first` looks for existing work first. Pointed at Carter's reference
  files, these do the distilling he describes.

### 12. Conventional commits

- Format: `<type>(<optional scope>): <description>`, one line, imperative mood, optional body.
- Types: feat, fix, refactor, docs, test, chore, perf, ci.
- Example: "S3: close the §4 stop-gate…" → `chore(plan): close the §4 stop-gate, delete all 8
  worktrees`.
- The bash dispatcher's `commit-quality` check (item 20) nudges this automatically. The attribution
  trailer is a separate question (item 14).

### 13. Coding style compared with ponytail

Ponytail's order of preference: 1. does it need to exist → 2. already in the codebase → 3. stdlib
→ 4. native platform → 5. installed dependency → 6. one line → 7. the least code that works.

| ECC rule | Ponytail | Fit |
|---|---|---|
| KISS, DRY, YAGNI | Same | Compatible |
| Early returns, named constants, split long functions | Same | Compatible |
| Immutability is CRITICAL | Not addressed | Neutral |
| Many small files, typically 200–400 lines | "one line before fifty" | Tension |
| patterns.md: repository pattern, API response envelope | Skip speculative abstraction | Conflict |
| agents.md: planner for complex features | "Does this need to exist?" | Tension over when to plan |

Test: 1. Pick one file → 2. Have ponytail-review and ECC's code-simplifier each review it → 3. Read
where they disagree. IF ponytail is removed (under review; its mode has been off since
2026-08-31) THEN skip this test.

### 14. `includeCoAuthoredBy: false`

- The trailer is Claude Code's own (`Co-Authored-By: Claude … <noreply@anthropic.com>`). ECC never
  names itself in commits.
- IF `settings.json` has neither `includeCoAuthoredBy` nor `attribution` THEN ECC setup writes
  `includeCoAuthoredBy: false` and the trailer switches off. As of 2026-09-23 it has neither.
- IF either key is set explicitly THEN ECC leaves it alone. So to keep the trailer, add
  `"includeCoAuthoredBy": true` before installing.
- `attribution` is the newer key. ECC writes the deprecated one because older Claude Code rejects
  keys it doesn't know.

### 15. `pluginConfigs["ecc@ecc"].options`

- This is Claude Code's store for per-plugin options in `settings.json`. For ECC it holds two values:
  `hooks_enabled` and `hook_profile`.
- At runtime they reach the hooks as `CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED` and
  `CLAUDE_PLUGIN_OPTION_HOOK_PROFILE`. This is the switch behind item 18.
- To change them: re-run `npx ecc-universal setup`, run `/ecc:configure-ecc`, or edit the JSON.

### 16. Settings recommendations

Values read from `settings.json` on 2026-09-23.

| Key | Now | ECC | Effect of accepting |
|---|---|---|---|
| `model` | `opus` | `sonnet` | New main sessions start on Sonnet. ALWAYS.md says the strongest main-session model is a deliberate choice |
| `effortLevel` | `xhigh` | — | none |
| `env.MAX_THINKING_TOKENS` | `10000` | `10000` | none |
| `env.CLAUDE_CODE_SUBAGENT_MODEL` | not set | `haiku` | Affects only agents with no `model:` pin: the built-ins (Explore, general-purpose, Plan, claude-code-guide) and workflow phases with no model. Carter's 7 agents and ECC's 68 are all pinned |
| `ECC_CONTEXT_MONITOR_COST_WARNINGS` | — | `off` for subscription users | Hides API-cost warnings from ECC's context monitor |

### 17. Merge `~/.claude/CLAUDE.md` with `examples/user-CLAUDE.md`

| | Yours | ECC's example |
|---|---|---|
| Size | 30 lines + the ALWAYS.md import | 109 lines |
| Content | — | Philosophy, a rules table (wrong path: missing `/ecc/`), an agents table (wrong location for the plugin path), preferences (no emojis, immutability, file sizes, conventional commits, TDD at 80%, knowledge-capture routing), a Zed section, success metrics |

- Nearly all of ECC's example repeats rules/common. So the merge comes down to which preference
  lines belong in CLAUDE.md and which belong in rules.
- Its knowledge-capture routing already matches the native-versus-project memory routing.
- Order: after items 7–13 are decided.

---

## Hooks, memory, other harnesses

### 18. Hook profile: `standard`, `minimal` or off

- Hook = a script Claude Code runs at an event: before a tool call (PreToolUse), after one
  (PostToolUse), when Claude finishes a turn (Stop), at session start (SessionStart), or before
  compaction (PreCompact).
- IF a hook exits with code 2 THEN the action is blocked and the hook's message goes back to Claude.

What `standard` runs:

| Event | Hook | Does | Blocks? | Item |
|---|---|---|---|---|
| PreToolUse Edit/Write | gateguard-fact-force | Demands investigation before the first edit to a file | Yes | 19 |
| PreToolUse Bash | bash dispatcher | Blocks `--no-verify`, tmux, push reminder, commit check, gateguard | Some | 20 |
| PreToolUse Edit/Write | config-protection | Blocks edits to linter and formatter configs | Yes | 21 |
| PreToolUse Write | doc-file-warning | Warns about TODO/NOTES/DRAFT files | No | 22 |
| PreToolUse any tool | mcp-health-check, observe-runner | Blocks MCP servers marked unhealthy; records each call | MCP only | 23 |
| PreToolUse Edit/Write | suggest-compact | Suggests `/compact` at intervals | No | 29 |
| PreCompact | pre-compact | Saves state before compaction | No | 24 |
| SessionStart | session-start | Injects the last session summary, instincts, learned skills, package manager | No | 28 |
| PostToolUse any tool | dispatcher | Quality gate, console warning, metrics, activity log, observation | Rarely | 23, 27 |
| Stop | session-end | Writes a session summary, sometimes via `claude -p` | No | 24 |
| Stop | format-typecheck, check-console-log | Formats edited files, runs tsc, checks for console.log | Yes on failure | 25 |
| Stop | desktop-notify | macOS notification | No | 26 |
| Stop | cost-tracker, evaluate-session, plan-canvas-pending | Metrics and learning | No | 27 |

| Profile | Runs |
|---|---|
| `standard` | everything in the table |
| `minimal` | the bash dispatcher and a metrics bridge |
| off | nothing; skills and agents stay |

Any profile: `ECC_DISABLED_HOOKS=id,id` turns off individual hooks.

### 19. Fact-forcing gate (`scripts/hooks/gateguard-fact-force.js`)

- Premise: ask an LLM "are you sure?" and it always says yes, so the hook demands facts instead.
- IF Claude edits or writes a file path for the first time this session THEN the hook blocks
  (exit 2) and asks for four things: who imports the file, what public API changes, whether the
  data schemas were checked, and a quote of the user instruction behind the edit. On the retry
  for the same path the edit goes through. Paths are recorded in `~/.gateguard` (keyed per
  session; a session times out after 30 minutes).
- IF a Bash command is destructive (rm, reset, force push, plus a configurable list) THEN it asks
  for the targets, a rollback plan and the instruction quote.
- IF a Bash command is routine THEN it asks for the instruction quote once per session.
- Cost = one blocked call + one investigation pass for each new file, markdown included.
- Settings: `GATEGUARD_EXEMPT_GLOBS` (e.g. `**/*.md`), `GATEGUARD_BASH_ROUTINE_DISABLED`,
  `GATEGUARD_FACT_FORCE_FULL_DENIALS`, `GATEGUARD_DISABLED`, `GATEGUARD_STATE_DIR`.
- It runs on the same matcher as guard-sharp-edges, and either hook can block with exit 2. It
  enforces the "look before you edit" that mattpocock asks for in prose.

### 20. Bash preflight dispatcher

Before each Bash call it starts one node process and runs, in order:
1. `block-no-verify` (refuses `git commit --no-verify`)
2. `auto-tmux-dev` (runs dev servers inside tmux)
3. `tmux-reminder` (for long commands)
4. `git-push-reminder`
5. `commit-quality` (item 12)
6. gateguard's Bash checks (item 19)

After the call: it logs the command and its cost, and posts notices when a PR is created or a
build finishes.

- It runs under every profile, `minimal` included.
- PreToolUse hooks run in parallel and get the original input, so it sees the command before rtk
  rewrites it. It runs alongside secrets-scanner.

### 21. Config protection

- Protected: the configs for eslint, prettier, biome, ruff, shellcheck, stylelint and markdownlint.
- IF the config file is new THEN the write is allowed. IF it modifies an existing config THEN it
  exits 2.
- For a legitimate change, edit it by hand or run with `ECC_DISABLED_HOOKS=pre:config-protection`.

### 22. Doc-file warning

- IF a Write creates NOTES / SCRATCH / DRAFT / WIP / TODO.md (and similar) outside `docs/`,
  `.claude/`, `memory/`, `skills/` or a few other structured folders THEN it prints a warning.
  It never blocks.
- Carter's root `TODO.md` is intentional, so for that file the warning is just repeated noise.
  Everywhere else it catches stray files.
- To turn it off: `ECC_DISABLED_HOOKS=pre:write:doc-file-warning`.

### 23. MCP health check and observation recorder (both on the `.*` matcher)

- **mcp-health-check**: keeps `~/.claude/mcp-health-cache.json`. IF calls to an MCP server fail
  THEN it marks the server unhealthy, blocks further calls to it and tries to reconnect. The one
  known case here (`plugin:data:definite`) disappeared when the data plugin was removed on
  2026-09-23, so its value now depends on MCP failures that haven't happened yet. For non-MCP
  tools it exits immediately, but a node process still starts on every call.
- **observe-runner**: writes each tool call and its outcome to the homunculus observations file.
  It is the input for item 30. IF item 30 is declined THEN this hook is cost with no benefit.

### 24. Session-end summary (with a nested `claude -p`)

| | ECC session-end | Dream shift | close-session |
|---|---|---|---|
| Trigger | Every Stop | launchd, daily at 07:30 | Manual |
| Reads | This session's transcript | The whole day's transcripts | The conversation |
| Writes | `~/.claude/session-data/<date>-<id>-session.md` | Native + project memory; proposals in `~/Claude/dreams/` | Memory files, summary file |
| Method | Mechanical extraction; haiku enrichment every 50 messages or below 20% context | Full model run, ratchet, KPI | Carter in the loop |
| Read by | ECC SessionStart in the same repo (item 28) | Later sessions, via MEMORY.md | Carter |
| Layer | Short-term continuity | Long-term consolidation | Curated |

- ECC's file sections: Session Summary, Tasks, Files Modified, Tools Used, Stats, Notes for Next
  Session, Context to Load.
- It overlaps with new-session handoffs (item 33), not with dream.
- IF the hook runs inside a background job, dream-cron or the night-shift foreman THEN the nested
  `claude -p` has the same shape that hit the 600-second limit in August. Fixes:
  `ECC_HOOKS_ENABLED=false` in those job environments, or a very large `ECC_LLM_SUMMARY_INTERVAL`.

### 25. Stop-time format, typecheck and console-log check

- At Stop, `stop-format-typecheck` formats every JS/TS file edited this session (with Biome or
  Prettier, whichever the project has) and then runs `tsc`.
- IF either one fails THEN it exits 2, and Claude can't stop until the errors are fixed.
- `check-console-log` checks the same files for leftover `console.log`.
- IF the project isn't JS/TS THEN it does nothing.

| | Carter's `auto-format.sh` | ECC |
|---|---|---|
| When | After each edit | Once per turn |
| Typecheck | No | Yes |
| Blocks | Never | On failure |

### 26. Stop-time desktop notification

| | Carter's hook | ECC's hook |
|---|---|---|
| Event | Notification (waiting on Carter: a permission prompt or idle) | Stop (a turn has finished) |
| Means | "waiting" | "done" |

They don't duplicate each other. Both fire only when a turn ends and a prompt follows.

### 27. Cost tracker, session evaluator, plan-canvas

- **cost-tracker**: at Stop it adds up the session's token usage and appends a row to
  `~/.claude/metrics/costs.jsonl`, plus a snapshot. `/ecc:cost-report` reads it. Carter's cost
  audits currently rebuild this data by hand.
- **evaluate-session**: the v1 learning extractor; at Stop it looks through the transcript for
  reusable patterns. The v2 observer (item 30) replaces it, but both run under `standard`.
- **plan-canvas**: a browser UI (`ecc-plan-canvas`) where you mark up a plan and approve it or ask
  for changes. At session start its hooks show open canvases, and before Stop they deliver any
  feedback not yet delivered. It writes to `~/.claude/plan-canvas/`.
- All three write to global state from every session, which raises the one-owner concern in
  `reference-global-state-parallel-sessions`.

### 28. Last-session context injected at SessionStart

What `session-start.js` injects, in order:
1. The latest session summary for this repo (matched by git common dir, capped by
   `ECC_SESSION_START_MAX_CHARS`)
2. Instincts, ranked
3. Learned skills
4. Session aliases
5. The package manager and project type

Today a session opens with only the MEMORY.md index; no SessionStart hook of Carter's runs. With
ECC added:

```
[MEMORY.md index, as now]

[SessionStart] Found 3 recent session(s)
[SessionStart] Selected: ~/.claude/session-data/2026-09-21-03bf80b5-session.md (match: repo)
## Session Summary
### Tasks
- Traced ECC v2.2.2 install paths, hooks, memory writes
### Files Modified
- plan/ecc-decisions.md
### Notes for Next Session
- Carter to answer 36 decisions
[SessionStart] Injecting 2 instinct(s) into session context
- prefer-verified-facts (0.8): quote file:line for every claim
[SessionStart] Package manager: bun (lockfile)
```

- Gain = continuity without a handoff step. Cost = a recall layer injected into every session,
  which the bake-off ruling says needs an explicit decision.
- For a trial, cap it with `ECC_SESSION_START_MAX_CHARS`. To turn it off:
  `ECC_SESSION_START_CONTEXT=off`.

### 29. Compaction suggestions on Edit and Write

- Auto-compaction triggers at a fixed context percentage, wherever the task happens to be,
  sometimes in the middle of an edit.
- `suggest-compact` counts tool calls (first suggestion at 50, then every 25) and watches
  transcript size (the threshold is 160k tokens on a 200k window). At those points it prints
  "consider `/compact` now".
- Effect: Claude can run close-session and compact at a phase boundary, before auto-compaction
  hits. With `autoCompactEnabled: true` both stay on; the hook only changes when compaction
  happens.

### 30. Instincts

- Instinct = a small learned rule with a confidence score, pulled automatically from observed
  sessions. Fields: `id`, `trigger`, `confidence`, `domain`, `source`, `scope`, then Action and
  Evidence sections (e.g. "Observed 5 instances…").
- Pipeline: 1. The observe hooks (item 23) record each session →
  2. Observations go to `~/.local/share/ecc-homunculus/projects/<hash>/` → 3. Instinct files are
  created per project with confidence 0.3 (tentative) to 0.9 (near certain) → 4. At SessionStart
  they are injected, ranked by confidence (item 28) → 5. Review: `/ecc:instinct-status`; cluster
  into skills, commands or agents: `/ecc:evolve`; promote: `/ecc:promote`.
- IF the same instinct id appears in 2+ projects AND its average confidence is ≥ 0.8 THEN
  `/ecc:promote` can move it from project scope to global.

| | capture-feedback | Dream | Instincts |
|---|---|---|---|
| Who decides | Carter confirms | Nightly model run | Automatic, statistical |
| Output | One rule per file, with Why and How | Memory consolidation | Confidence-scored guesses |
| Upside | — | — | Catches patterns Carter never stated |
| Risk | — | — | Unverified state, injected automatically: what ALWAYS.md forbids in memory |

[not verified] Whether extraction uses heuristics or a model.

### 31. Promoted instincts become local skills

- Promotion is already manual. Only observation and instinct creation are automatic, and both
  happen outside `~/.claude`.
- The decision left: IF a promoted instinct is written to `~/.claude/skills/learned/` THEN it
  becomes a listed skill and counts toward the item 3 budget. ELSE you fold it by hand into an
  existing skill or feedback file.

### 32. unified-memory

- unified-memory = one memory store shared by Claude, Codex, Cursor and OpenCode:
  `<git root>/.ecc/memory/{project,team}` + `~/.ecc/memory/`, with an optional MCP server
  (`ecc-memory-vault`).
- IF Codex needs the same context when it reviews Claude's output THEN it earns its place. ELSE it
  duplicates `.claude/memory/` and adds a third store, which this project's two-store thesis and
  the one-current-file-per-thing rule warn against.

### 33. session-data as the resume mechanism

| | ECC session-data | new-session + close-session |
|---|---|---|
| Trigger | Automatic at every Stop | Manual, one deliberate step each |
| Where | `~/.claude/session-data/` (global) | `.claude/memory/handoffs/` in the task (new-session); memory files (close-session) |
| Keyed by | Git common dir, newest first | Task folder, a named handoff |
| Reload | Automatic at SessionStart | Paste the handoff prompt |
| Content | Mechanical: tasks, files, tools, stats; haiku enrichment now and then | Curated |
| Kept for | `ECC_SESSION_RETENTION_DAYS` | Until deleted |
| Fits | Continuity across many short sessions | Deliberate handoffs between tracked sessions |

- IF you choose ECC THEN new-session's handoff file goes. close-session's memory updates are a
  different job and stay.
- IF you choose yours THEN set `ECC_DISABLED_HOOKS=stop:session-end,session:start`, or use a
  profile without those hooks.

### 34. Sync ECC into Codex

| Path | How | Effect |
|---|---|---|
| Native | `codex plugin marketplace add affaan-m/ECC` → `codex plugin add ecc@ecc` | No file merging; Codex decides hook trust |
| Legacy | `scripts/sync-ecc-to-codex.sh` | Backs up first, then: merges an ECC block into `~/.codex/AGENTS.md` between markers, adds to `config.toml` without overwriting (the only MCP it adds is `chrome-devtools`), copies prompts and agents, installs global git hooks |

- `~/.codex` already registers marketplaces, so the native path matches how it's set up now.
- Neither path runs as a side effect of the Claude install.

### 35. Catalog MCP servers (33, all opt-in; the plugin registers none)

| Group | Servers |
|---|---|
| Memory | memory, omega-memory, memxus, longhand (indexes `~/.claude` session history), ecc-memory-vault (item 32) |
| Search and research | exa-web-search (paid key), parallel-search, firecrawl (paid key), context7 (Carter uses the `ctx7` CLI instead) |
| Dev platforms | github (token), vercel, railway, cloudflare docs/builds/bindings/observability, supabase (Carter has the plugin, under review, 0 uses), clickhouse |
| Browser | playwright, browserbase (paid), browser-use (paid) |
| Tracking | jira, confluence |
| Media | fal-ai (paid), magic (UI components) |
| Meta and infra | nexus (cost proxy), token-optimizer, devfleet (parallel worktree agents), filesystem, sequential-thinking, evalview (agent regression tests), codescene, laraplugins, ito-compute (unpublished) |

- Browser roles (ruled 2026-09-23): agent-browser for general tasks, Chrome DevTools for debugging
  (no MCP set up yet; it's in `TODO.md`), Playwright for end-to-end tests, Claude in Chrome as the
  backup. ECC's playwright server fits the end-to-end role. The Codex sync (item 34) adds
  `chrome-devtools`, which fills the debugging gap on the Codex side only.
- ECC's own guidance: 20–30 servers in config, under 10 enabled, under 80 tools active. Carter's
  enabled set is already large: google_workspace, agentmail, granola, reactbits, plus the
  claude.ai connectors.

### 36. `contexts/` shell aliases compared with modes

| | ECC contexts | Carter's modes |
|---|---|---|
| What | 3 files, 400–600 bytes each: dev, research, review | 3 folders: research, plan, make, each with its own CLAUDE.md and skills |
| How it loads | `claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"` through a shell alias | CLAUDE.md files load by walking up from the cwd (verified in `reference-claude-code-loading-mechanics`) |
| How you switch | Start a new process | `cd` into the mode folder |
| Effect | Replaces the system prompt for that process (`--append-system-prompt` adds to it instead; check the CLI docs for current behaviour) | Adds to the default prompt |
| Where it ships | Git checkout only, not the npm package | Single source in `~/.claude/modes/` |
| Content | Behaviour bullets, tool preferences | Principles, conventions, the skills each mode uses |

A context sets the tone for one launch; a mode sets what loads. They don't overlap, and nothing in
ECC depends on contexts.
