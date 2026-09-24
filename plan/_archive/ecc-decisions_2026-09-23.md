# ECC adoption: 36 accept/deny decisions

Source: https://github.com/affaan-m/ecc (v2.2.2, 2026-09-15). Traced 2026-09-21 against a clone and
the live `~/.claude`. Carter's answers recorded 2026-09-22. Responses under each pair. Updated 2026-09-23 for the
plugin and skill cleanup (`.claude/memory/decisions.md`, 2026-09-23).

**Changed since the answers (2026-09-23):**

- **Removed:** the superpowers plugin; all of gstack (browse, benchmark, context-save/restore);
  Arc; local skills save-summary, fable-plan, scout-stack (its suite table is now in
  `~/.claude/modes/PLAN-MODE.md`), and the `project-root-warning` SessionStart hook. dung was
  archived to `~/Projects/Archive/old-skills/`.
- **Moved:** decide and file-versioning are now always-loaded rules in `~/.claude/rules/`, not
  skills.
- **Removed in claude.ai:** data and product-management. Verified 2026-09-23: the sync manifest
  lists no plugins and marks both folders stale.
- **Listing re-measured:** 69 skills, 28,523 chars against the 30,000 budget (item 3).
- **Still installed, under Carter's review:** mattpocock-skills, ponytail, supabase.
- **Browser roles ruled:** agent-browser for general tasks, Chrome DevTools for debugging (no MCP
  configured yet), Playwright for end-to-end tests, Claude in Chrome as backup.

Items 1, 3, 4, 13, 23, 24, 28, 33 and 35 are updated below. Carter's answers are unchanged.

Related: `plan/skill-budget-ab.md`, `plan/trim-skills.md` (the listing-budget work this decision
lands on top of), memory `reference-ecc-kit-evaluation`.

Every path below is relative to the ECC repo unless it starts with `~`. The clone used for this
trace lives in a job tmp dir and will be deleted; read files at the GitHub URL or re-clone.

---

## Install shape

### 1. Install ECC as the `ecc@ecc` plugin

**Carter:** I would like to compare my existing skills and plugins with ECC. I would be willing to
abandon certain plugins as needed in preference of ECC.

**Response.** Mapping of what you run today to what ECC ships, by plugin. "Gap" means ECC has no
equivalent; "different tool" means same job, different mechanism.

| Yours | ECC equivalent | Note |
|---|---|---|
| **superpowers** (uninstalled 2026-09-23) brainstorming | `intent-driven-development`, `council` | Partial. ECC has no "explore intent before building" skill; council is a 4-voice decision aid |
| superpowers writing-plans, executing-plans | `plan-orchestrate`, `/ecc:plan`, `/ecc:plan-prd`, planner agent (opus) | Close match |
| superpowers subagent-driven-development, dispatching-parallel-agents | `team-agent-orchestration`, `orch-*` commands, rules/common/agents.md | ECC is heavier: work items, Kanban, merge gates |
| superpowers TDD | `tdd-workflow` + tdd-guide agent | Close match, ECC adds the 80% number |
| superpowers systematic-debugging | build-error-resolver agents (10 languages), `silent-failure-hunter` | Gap for general debugging method |
| superpowers verification-before-completion | `verification-loop`, `delivery-gate` (Stop hook) | ECC enforces mechanically |
| superpowers requesting/receiving-code-review | code-reviewer agent, rules/common/code-review.md, `santa-method` | Close |
| superpowers finishing-a-development-branch, using-git-worktrees | `git-workflow`, `/ecc:pr`, `scripts/worktree-lifecycle.js`, `dmux-workflows` | Close |
| superpowers writing-skills | `skill-scout`, `skill-stocktake`, `skill-comply`, `/ecc:skill-create` | ECC adds "search before creating" and a compliance visualizer |
| **mattpocock** (under review) tdd, code-review, research | `tdd-workflow`, code-reviewer, `research-ops`, `deep-research` | Close |
| mattpocock diagnosing-bugs, prototype, wizard, grilling, writing-for-agents | none | Gaps. writing-for-agents is your adopted authoring standard |
| mattpocock domain-modeling, codebase-design | `contract-first`, `hexagonal-architecture`, architect agent | Different framing |
| **ponytail** (6 skills, under review; mode off since 2026-08-31) | `code-simplifier` agent, `refactor-cleaner`, KISS/YAGNI in coding-style.md | See item 13 for the conflict |
| **gstack** (removed 2026-09-23) browse, qa, qa-only | `browser-qa`, `e2e-testing`, e2e-runner agent | Browse is now agent-browser; ECC uses Playwright or Vercel Agent Browser, which matches the Playwright end-to-end role |
| gstack benchmark | `benchmark` | See item 4 |
| gstack canary | `canary-watch` | Close |
| gstack ship, land-and-deploy | `/ecc:pr`, `git-workflow`, `deployment-patterns` | ECC has no version-bump/CHANGELOG step |
| gstack review, cso | code-reviewer, security-reviewer, `security-review`, `security-bounty-hunter` | Close |
| gstack plan-ceo/design/eng/devex-review, autoplan | `council`, `plan-canvas` | Different shape: ECC's canvas is a browser annotation UI |
| gstack spec | `intent-driven-development`, `blueprint` | Close |
| gstack careful, guard, freeze | `safety-guard`, `gateguard`, config-protection hook | ECC's are hooks, gstack's are session modes |
| gstack context-save/restore | `/ecc:save-session`, `/ecc:resume-session` | See item 33 |
| gstack health, retro, investigate, office-hours, diagram, make-pdf | `context-budget`, `config-gc`, `production-audit` for health; rest are gaps | |
| gstack design-* | `frontend-design-direction`, `design-system`, `make-interfaces-feel-better` | Different tool |
| gstack ios-* | swift-reviewer, swift-build-resolver, `swiftui-patterns`, `ios-icon-gen` | Partial |
| gstack setup-gbrain, sync-gbrain | `unified-memory` | Different system, see item 32 |
| **yours** dream, morning/day/night-shift | continuous-learning-v2, loop-operator agent, `autonomous-loops` | Different shape, see items 24 and 30 |
| yours capture-feedback, learn | instincts + `/ecc:learn` | See item 30 |
| yours new-session, close-session (save-summary trashed 2026-09-23) | `/ecc:save-session`, `/ecc:checkpoint` | See item 33 |
| yours decide (now a rule in `~/.claude/rules/`) | `council` | Close; a rule is always loaded, so it costs no listing entry |
| ~~scout-stack~~ (trashed; table in PLAN-MODE.md) | `search-first`, `skill-scout` | No longer a skill to compare |
| ~~dung~~ (archived) | `scripts/orchestrate-worktrees.js`, `parallel-execution-optimizer` | No longer installed |
| ~~fable-plan~~ (trashed) | planner agent (opus) | No longer installed |
| yours database-design, api-design, mcp-builder, skill-creator | `postgres-patterns` + `database-migrations`, `api-design`, `mcp-server-patterns`, `/ecc:skill-create` | See item 4 for api-design |
| yours blocksite, email-tracker, github-digest, fill-notes, supplement, write-doc, transcribe-media, clean-transcript | none | Personal workflows, no overlap. file-versioning is now a rule |
| anthropic-skills (bundled) | n/a | Exempt from the listing budget, no overlap concern |

The budget arithmetic when abandoning plugins: superpowers (13) is already gone. mattpocock (11)
and ponytail (6) are the 17 plugin entries left. ECC is 292 plus 94. Dropping every plugin you have
does not offset the plugin path. It only offsets a file-copy subset (item 2).

### 2. Vendor a trimmed subset via `install.sh --target claude`

**Carter:** This is the most likely case, complimentary to the comparison across different plugins
that I use.

**Response.** Mechanics, verified in `scripts/lib/install/`:

- `--skills a,b,c` installs only named skills. `--profile <p>` installs a module set;
  `--with`/`--without` adjust it. `--dry-run` prints every write before touching disk. Use it
  first: the `platform-configs` module is what drops `plugin.json`, `marketplace.json`,
  `README.md`, `AGENTS.md`, and `docs/` into `~/.claude/` root, so a `--skills` list without
  modules avoids that.
- Skills land flat at `~/.claude/skills/<name>/`. They are local skills, so `skillOverrides` and
  usage-priority trimming work on them, unlike the plugin path.
- `~/.claude/ecc/install-state.json` records every file ECC created. Reinstall skips anything not
  in that ledger. `node scripts/ecc.js list-installed | doctor | repair` operate on it. Upgrade is
  re-running the installer from a newer checkout; there is no auto-update on this path.
- This is vendoring. The ALWAYS.md rule against vendoring exists because copies freeze. ECC's
  ledger makes the copy upgradeable, which is the mitigation, not an exception.

Sequence: finish item 1's comparison, pick the ECC skills that win, install exactly those with
`--skills` and `--dry-run` first.

### 3. Absorb roughly 93,000 characters into the skill listing

**Carter:** Subject to review, will be based on results of number 1 as well.

**Response.** The numbers, for the review:

| | Chars |
|---|---|
| Listing budget on this machine (measured, default model) | ~30,000 |
| Your catalog on 2026-08-07 (130 skills) | 35,948 |
| Your catalog on 2026-09-23, after the cleanup (69 skills) | 28,523 |
| ECC 292 skill descriptions, per-entry cap applied | ~83,400 |
| ECC 94 command descriptions | ~10,000 |

Overflow renders as bare names, silently, and bare names cannot natural-language trigger. The
plugin path has no lever: `plugin.json` exposes only `hooks_enabled` and `hook_profile`. Item 2's
`--skills` list is the only trimming mechanism. `plan/trim-skills.md` and `plan/skill-budget-ab.md`
already hold the A/B method for checking which skills fall out.

How the 2026-09-23 figure was measured: a headless `claude -p` run from a neutral folder with
`--settings '{"skillListingBudgetFraction":0.0005}'`, which forces the loader to print its own
over-budget line (`69 skills, 28523 chars > 1500 budget`). A second run at the default budget
printed no warning, so the catalog fits. The 69 are the 48 local skills plus 32 plugin skills
(mattpocock 25, ponytail 6, supabase 1), less the ones hidden from the listing. The 40 bundled
Anthropic skills are exempt. The 48 local skills include 8 in `~/.claude/skills/_archived/`, which
the loader still reads as live.

Arithmetic for sizing an ECC subset: about 1,500 chars of headroom at the default budget. ECC's
skills average about 285 chars each (83,400 / 292), so roughly 5 fit before something else loses
its description. At a 200K-context model's budget (about 8,000 chars) the catalog is already
about 3.5 times over.

### 4. Keep your `api-design` and `benchmark` next to ECC's

**Carter:** Need to compare which version I prefer, need to see them side by side.

**Update 2026-09-23:** gstack is gone, so the benchmark comparison is ECC's or none. Only
api-design is still a live side-by-side.

**Response.** Side by side. Full files: `skills/api-design/SKILL.md` and `skills/benchmark/SKILL.md`
on GitHub; yours at `~/.claude/skills/api-design/SKILL.md` and
`~/.claude/skills/gstack/benchmark/SKILL.md`.

| | Yours | ECC |
|---|---|---|
| **api-design** size | 1.5 KB | 13.2 KB |
| Scope | REST and GraphQL | REST only |
| Shape | Principles, when/when-not, instructions, a Resources pointer | 11 sections: resource design, HTTP methods and status codes, response format, pagination, filtering/sorting/search, auth, rate limiting, versioning, implementation patterns |
| Frontmatter | `allowed-tools` restricts to Read, Glob, Grep, Bash, Agent | None |
| **benchmark** size | 36.4 KB (gstack) | 2.4 KB |
| Mechanism | gstack browse daemon, page-speed regression, preamble, artifacts sync, voice, completion protocol | Generic: measure baselines, detect regressions before/after PRs, compare stack alternatives; "How It Works" and "Integration" sections |
| Coupling | Requires gstack's daemon and conventions | Standalone |

Reading: yours are thin pointers and gstack's is a full tool; ECC's api-design is a reference
document and its benchmark is a method sketch. Which you prefer depends on whether you want the
reference text in context when the skill fires (ECC) or a short pointer to it (yours).

### 5. Add 68 agents with ECC's own model pins

**Carter:** Willing to accept, just need to understand what the agents do.

**Response.** Grouped. Model in parentheses when not sonnet.

- **Core workflow (18):** planner (opus), architect (opus), code-reviewer, security-reviewer,
  tdd-guide, build-error-resolver, e2e-runner, refactor-cleaner, doc-updater (haiku),
  code-simplifier, code-architect, code-explorer, performance-optimizer, silent-failure-hunter,
  type-design-analyzer, comment-analyzer (haiku), pr-test-analyzer, docs-lookup (haiku, Context7).
- **Language reviewers (21):** cpp, csharp, django, fastapi, flutter, fsharp, go, java, kotlin,
  php, python, react, rust, swift, typescript, vue, harmonyos-app-resolver, database (Postgres),
  mle, rag-pipeline, healthcare (opus).
- **Build resolvers (10):** cpp, dart, django, go, java, kotlin, pytorch, react, rust, swift.
- **Orchestration and meta (8):** gan-planner, gan-generator, gan-evaluator (a spec-build-test
  loop), agent-evaluator (5-axis rubric), harness-optimizer (eval-driven config tuning),
  loop-operator, conversation-analyzer (haiku, finds behaviors worth a hook), spec-miner (opus).
- **Domain and business (11):** chief-of-staff (email/Slack triage), marketing-agent,
  seo-specialist, a11y-architect, homelab-architect, network-architect,
  network-config-reviewer, network-troubleshooter, opensource-forker (haiku),
  opensource-packager (haiku), opensource-sanitizer.

Two things to know. Most descriptions say "Use PROACTIVELY", which is the auto-invoke pressure
from item 8. And all 68 appear in the Agent tool's type list every session, on top of your 7 and
the built-ins.

### 6. Add 94 slash-command shims under `/ecc:`

**Carter:** If these are legacy, what has replaced them?

**Response.** Skills replaced them. ECC's own text: commands are "convenient entry points while
ECC moves to a skills-first surface" and "the durable logic should live in skills." 34 of the 94
explicitly delegate to a skill. Examples: `/ecc:plan` → `plan-orchestrate` and the planner agent;
`/ecc:tdd` (in `legacy-command-shims/`, not loaded by default) → `tdd-workflow`;
`/ecc:code-review` → the code-reviewer agent; `/ecc:save-session` → session-data (item 33).
The older shims (`/tdd`, `/eval`, `/verify`) sit in `legacy-command-shims/` and are not loaded
unless copied in by hand. The 94 that are loaded still cost about 10,000 listing characters.

---

## Instructions and settings

### 7. Copy `rules/common` into `~/.claude/rules/ecc/common/`

**Carter:** Need to understand this from a token and performance perspective, need to read all of
the files.

**Response.** The ten files, at https://github.com/affaan-m/ecc/tree/main/rules/common:

| File | Bytes | ≈Tokens | Content |
|---|---|---|---|
| agents.md | 2,800 | 700 | Agent roster, "immediate agent usage", parallel execution, delegation completion contract |
| code-review.md | 3,600 | 900 | Review triggers, checklist, severity levels, 80% coverage line |
| coding-style.md | 3,000 | 750 | Immutability, KISS/DRY/YAGNI, file sizes, error handling, naming |
| development-workflow.md | 2,200 | 550 | Research-first, plan, TDD, review, commit sequence |
| performance.md | 1,600 | 400 | Model selection table, context management, extended thinking |
| testing.md | 1,400 | 350 | 80% coverage, three test types, TDD steps, AAA pattern |
| patterns.md | 1,000 | 250 | Skeleton projects, repository pattern, API response envelope |
| security.md | 860 | 215 | Pre-commit checklist, secret management, response protocol |
| git-workflow.md | 840 | 210 | Conventional commit format, PR workflow, the `includeCoAuthoredBy` note |
| hooks.md | 770 | 190 | Hook types, auto-accept caution, TodoWrite advice |
| **Total** | **18,100** | **≈4,500** | |

Performance model: rules are not skills. A skill loads when it fires; a rule loads every session
in every project. So the cost is ≈4,500 tokens per session, constant, if the harness recurses
into `rules/ecc/`. That recursion is unverified on this machine. Test it the way
`reference-claude-code-loading-mechanics` did: a sentinel file at `~/.claude/rules/ecc/test.md`,
a headless probe, delete. Language packs add 5 to 8 files each (the full tree is 122 files,
286 KB); you would copy one at most.

### 8. Agent-first auto-invocation

**Carter:** I am okay with this because they are agents, not skills (I believe that superpowers
was calling skills).

**Response.** The distinction holds and matters for cost: a skill loads into the main context; an
agent runs in its own context and returns a report. So ECC's rule costs subagent calls, not main-
context tokens. Two residual points. First, ECC's triggers include "complex feature requests →
planner", which fires on the request itself, so your CLAUDE.md line "a direct question gets a
direct answer" would need to say which requests it exempts, or the two rules argue. Second, item 5's
"Use PROACTIVELY" descriptions apply the same pressure from the agent side even without the rule.

### 9. 80% coverage, three test types, TDD on every change

**Carter:** TDD is not overengineering, over engineering is complex code when simple code reliably
performs the function. I still think that conformance-suite-first can work with this.

**Response.** Agreed on the definition; the earlier framing was mine, not yours. Facts for the
layering: nothing in ECC's hook runtime enforces 80%. `quality-gate.js` is a formatter and linter
pass, and coverage is only checked when `/ecc:test-coverage` or the tdd-guide agent runs. So the
number is instruction text, not a gate. Conformance suites have no ECC concept; your PLAN-MODE rule
sits on top without contradiction, and suite runs count toward whatever coverage number applies.

### 10. ECC's model table

**Carter:** I would be willing to consider this table. I think that it is generally correct, and I
believe that this form of development that ECC is setup for is subagent heavy, therefore these model
allocations make sense.

**Response.** The tiering logic matches your Model-Configuration-Guide; the names are stale.
Mapped: ECC "Haiku" = Haiku 4.5, "Sonnet" = Sonnet 5 or 4.6, "Opus" = Opus 4.8, with Fable above
the table. ECC's pins: 58 sonnet, 6 haiku, 4 opus (planner, architect, spec-miner,
healthcare-reviewer). Compared to your dev-pipeline: Implementer opus, QA Runner sonnet,
Merge-Gate Reviewer opus. ECC's code-reviewer and security-reviewer are sonnet, one tier below
your Merge-Gate. Overriding a plugin agent's model means copying its file into `~/.claude/agents/`
with a different pin, which is a fork. Subagent-heavy is correct: rules/agents.md, 68 agents, and
the `orch-*` commands all assume delegation.

### 11. GitHub code search first, Context7 second, Exa third, then agents per feature

**Carter:** Accept. What is Exa? I believe that the concepts in my reference files (local files)
are distilled into ECC, but we can repurpose the reference file idea (keep them as references for
concepts that we want to be distilled into the skills and agents).

**Response.** Exa is a neural web search API (exa.ai). ECC uses it through the opt-in
`exa-web-search` MCP server, which needs a paid `EXA_API_KEY`, and the `exa-search` skill. Your
local-files-first rule and ECC's step 0 do not collide: ECC's order is about finding existing code
before writing code; yours is about answering questions from your own notes before the web. Both
can stand. For the reference-file idea, ECC ships `rules-distill` (scan skills, extract
cross-cutting principles into rule files) and `search-first`. That is the distillation mechanism
you describe, pointed at your references instead of ECC's skills.

### 12. Conventional commit format

**Carter:** Accept. I am not an engineer and have never shared a GitHub repo with many other
contributors so I do not know what standard commits look like. I believe ECC has the expertise
here.

**Response.** The format is `<type>(<optional scope>): <description>`, one line, imperative, then
an optional body. Types ECC lists: feat, fix, refactor, docs, test, chore, perf, ci. Your recent
"S3: close the §4 stop-gate, delete all 8 worktrees" would become
`chore(plan): close the §4 stop-gate, delete all 8 worktrees`. ECC's bash dispatcher (item 20) has
a `commit-quality` check that inspects commit messages in Bash commands, so this gets nudged
mechanically, not just by rule text. The attribution trailer is a separate line and is item 14.

### 13. Immutability as critical, functions under 50 lines, files 200 to 400 lines

**Carter:** I want to investigate this more. Would like to see if ponytail is compatible.

**Response.** Ponytail's ladder: does it need to exist, already in the codebase, stdlib, native
platform, installed dependency, one line, then minimum code. Against ECC's coding-style.md:

| ECC rule | Ponytail | Verdict |
|---|---|---|
| KISS, DRY, YAGNI section | Same stance | Compatible |
| Early returns, named constants, split long functions | Same | Compatible |
| Immutability CRITICAL, never mutate | Not addressed | Neutral |
| Many small files > few large, 200 to 400 lines typical | "one line before fifty" | Tension: ECC pushes splitting, ponytail pushes less code |
| patterns.md: repository pattern, API response envelope | "speculative abstraction = skip" | Conflict: ponytail would call both premature until needed |
| agents.md: planner for complex features | "does this need to exist at all" | Tension on when to plan |

Test to run: take one file, have ponytail-review and ECC's code-simplifier agent each review it,
and read where they disagree. That is the concrete compatibility check. Ponytail is itself under
review (2026-09-23); its mode has been off since 2026-08-31, so this test only matters if it stays.

### 14. Let plugin setup write `includeCoAuthoredBy: false`

**Carter:** What am I deciding here? I do not want it to say co-authored by ECC but I am fine with
it saying co-authored by Claude Code.

**Response.** The trailer in question is Claude Code's own:
`Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. ECC never adds itself. What ECC does is
turn that trailer **off**, by writing `includeCoAuthoredBy: false`, and only when your settings
have neither `includeCoAuthoredBy` nor `attribution`. Verified: your `settings.json` has neither.
So today the install would switch the trailer off. To keep it on, add `"includeCoAuthoredBy": true`
to `settings.json` before installing; ECC treats any explicit value as your decision and leaves it.
(`attribution` is the newer key; ECC writes the deprecated one because older Claude Code rejects
unknown keys. Either explicit key blocks the write.)

### 15. Let plugin setup write `pluginConfigs["ecc@ecc"].options`

**Carter:** What does this do?

**Response.** Claude Code stores per-plugin user options in `settings.json` under
`pluginConfigs["<plugin id>"].options`. For ECC that is two values, `hooks_enabled` and
`hook_profile`. At runtime the CLI passes them to hook processes as
`CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED` and `CLAUDE_PLUGIN_OPTION_HOOK_PROFILE`. This is the switch
behind item 18. Changed later by re-running `npx ecc-universal setup`, by `/ecc:configure-ecc`, or
by editing the JSON.

### 16. Adopt ECC's settings recommendations

**Carter:** What are my current settings on this say? What would accepting this change?

**Response.** Current, read from `settings.json` directly (the earlier inventory's "model: fable"
was wrong; rtk compressed that read):

| Key | Now | ECC recommends | Effect of accepting |
|---|---|---|---|
| `model` | absent, so the CLI default or launch flag decides; this job runs on Fable | `sonnet` | Every new main session starts on Sonnet 5 |
| `effortLevel` | `xhigh` | not mentioned | none |
| `env.MAX_THINKING_TOKENS` | `10000` | `10000` | none, already matches |
| `env.CLAUDE_CODE_SUBAGENT_MODEL` | absent | `haiku` | Only agents **without** a `model:` pin change: built-ins (Explore, general-purpose, Plan, claude-code-guide) and Workflow phases with no model. Your 7 agents and ECC's 68 are all pinned, so unaffected |
| `ECC_CONTEXT_MONITOR_COST_WARNINGS` | n/a | `off` for subscription users | Suppresses API-cost estimate warnings from ECC's context monitor |

### 17. Replace `~/.claude/CLAUDE.md` with `examples/user-CLAUDE.md`

**Carter:** We will find a way to merge them. This will be done HITL.

**Response.** Inputs for that session: yours is 30 lines plus the ALWAYS.md import. ECC's example
is 109 lines: a philosophy block, a rules table (wrong path, missing `/ecc/`), an agents table
(wrong location for the plugin path), preferences (no emojis, immutability, file sizes,
conventional commits, TDD and 80%, a knowledge-capture routing section), a Zed section, and
success metrics. Nearly all of it restates rules/common, so the merge reduces to which preference
lines you want in CLAUDE.md rather than in rules. The knowledge-capture section already matches
your native-versus-project routing. Sequence it after items 7 through 13 are decided.

---

## Hooks, memory, other harnesses

### 18. Hook profile: `standard`, `minimal`, or off

**Carter:** Need to understand what the hooks are doing before I accept or deny.

**Response.** A hook is a script Claude Code runs at an event: before a tool call (PreToolUse),
after (PostToolUse), when Claude finishes a turn (Stop), at session start, before compaction. Exit
code 2 blocks the action and feeds the script's message back to Claude. Under `standard`:

| Event | Hook | Does | Blocks? | Item |
|---|---|---|---|---|
| PreToolUse Edit/Write | gateguard-fact-force | Demands investigation before first edit of a file | Yes | 19 |
| PreToolUse Bash | bash dispatcher | No-verify block, tmux, push reminder, commit quality, gateguard | Some | 20 |
| PreToolUse Edit/Write | config-protection | Blocks linter/formatter config edits | Yes | 21 |
| PreToolUse Write | doc-file-warning | Warns on TODO/NOTES/DRAFT files outside structured dirs | No | 22 |
| PreToolUse any | mcp-health-check, observe-runner | Blocks unhealthy MCP servers; records observations | MCP only | 23 |
| PreToolUse Edit/Write | suggest-compact | Nudges `/compact` at intervals | No | 29 |
| PreCompact | pre-compact | Saves state before compaction | No | 24 |
| SessionStart | session-start | Injects prior session, instincts, learned skills, package manager | No | 28 |
| PostToolUse any | dispatcher | Quality gate, console warn, metrics, activity tracker, observe | Rare | 23, 27 |
| Stop | session-end | Writes session summary, sometimes via `claude -p` | No | 24 |
| Stop | format-typecheck, check-console-log | Batch format, tsc, console.log audit | Yes on failure | 25 |
| Stop | desktop-notify | macOS notification | No | 26 |
| Stop | cost-tracker, evaluate-session, plan-canvas-pending | Metrics and learning | No | 27 |

`minimal` keeps only the bash dispatcher and a metrics bridge. Off keeps skills and agents only.
`ECC_DISABLED_HOOKS=id,id` turns off individual ones under any profile.

### 19. Fact-forcing gate on Edit and Write

**Carter:** Sounds like this could be useful... explain this more.

**Response.** From `scripts/hooks/gateguard-fact-force.js`. The premise in its header: asking an
LLM "are you sure?" always gets "yes", so instead demand facts.

- **Edit/Write:** the first time a file path is touched in a session, the hook exits 2 with a
  denial that asks for four things: who imports this file, what public API is affected, whether
  the data schemas were verified, and a quote of the user instruction that motivates the edit.
  Claude then greps importers, reads the schema, quotes you, and retries. The retry on the same
  path passes; the path is recorded in `~/.gateguard` (per-session keys, 30-minute session
  timeout).
- **Bash destructive** (rm, reset, force push, and a configurable extra list): list the targets,
  a rollback plan, and the instruction quote.
- **Bash routine:** quote the current instruction once per session.

Cost: one denied call plus an investigation pass per new file, including markdown. Knobs:
`GATEGUARD_EXEMPT_GLOBS` (for example `**/*.md` to exempt prose), `GATEGUARD_BASH_ROUTINE_DISABLED`,
`GATEGUARD_FACT_FORCE_FULL_DENIALS`, `GATEGUARD_DISABLED`, `GATEGUARD_STATE_DIR`. It runs beside
your guard-sharp-edges hook on the same matcher; either one's exit 2 blocks. What it gives you: the
"look before you edit" that superpowers and mattpocock ask for in prose, enforced mechanically.

### 20. Bash preflight dispatcher

**Carter:** What is this?

**Response.** One node process per Bash call that runs, in order: `block-no-verify` (refuses
`git commit --no-verify`), `auto-tmux-dev` (wraps dev servers in tmux), `tmux-reminder` (long
commands), `git-push-reminder`, `commit-quality` (checks the commit message, see item 12), and the
Bash half of gateguard (item 19). After the call: command log audit and cost, PR-created and
build-complete notices. It runs under every profile including `minimal`. It sees the command before
rtk rewrites it, because PreToolUse hooks receive the original input in parallel, and beside your
secrets-scanner.

### 21. Config protection

**Carter:** Seems like a good idea.

**Response.** Protected: eslint, prettier, biome, ruff, shellcheck, stylelint, markdownlint
configs. First-time creation is allowed; modification exits 2. When you legitimately need to change
one, edit it by hand or run that session with `ECC_DISABLED_HOOKS=pre:config-protection`.

### 22. Doc-file warning

**Carter:** Why would this be useful?

**Response.** It exists to stop agents leaving impulse files behind: NOTES.md, SCRATCH.md,
DRAFT.md, WIP.md, TODO.md and similar, outside `docs/`, `.claude/`, `memory/`, `skills/` and a few
other structured directories. It never blocks; it prints a warning Claude sees. Your root `TODO.md`
is deliberate, so on that one file it is a recurring nag with no value. Elsewhere it catches litter.
Disable with `ECC_DISABLED_HOOKS=pre:write:doc-file-warning`.

### 23. MCP health check and observation recorder on every tool call

**Carter:** Why would this be useful?

**Response.** Two different hooks on the same `.*` matcher.

- **mcp-health-check** keeps `~/.claude/mcp-health-cache.json`. After MCP call failures it marks
  the server unhealthy, blocks further calls to it, and tries a reconnect. Concrete case on your
  machine: `plugin:data:definite` failed to connect every session. Carter removed the data plugin
  in claude.ai on 2026-09-23, and a headless probe that day logged no `definite` error, so that
  case is gone. The hook's value now rests on whatever MCP servers fail in future. For non-MCP tools the script exits immediately, but the node spawn still
  happens per call.
- **observe-runner** writes each tool call and outcome to the homunculus observations file. It has
  no value on its own; it is the sensor for item 30. If 30 is denied, this hook is pure cost.

### 24. Session-end summary with a nested `claude -p`

**Carter:** Need to understand comparison.

**Response.** Three things that look similar and are not:

| | ECC session-end | Dream shift | close-session |
|---|---|---|---|
| Trigger | Every Stop, automatic | launchd 07:30 daily | Manual |
| Reads | This session's transcript | All the day's transcripts | The conversation |
| Writes | `~/.claude/session-data/<date>-<id>-session.md` | Native and project memory, proposals in `~/Claude/dreams/` | Memory files, summary file |
| Method | Mechanical extraction; haiku enrichment every 50 messages or under 20% context | Full model run over transcripts, ratchet and KPI | HITL |
| Read by | ECC SessionStart in the same repo (item 28) | Next sessions via MEMORY.md | You |
| Layer | Short-term continuity | Long-term consolidation | Curated |

ECC's file looks like: `## Session Summary`, `### Tasks`, `### Files Modified`, `### Tools Used`,
`### Stats`, `### Notes for Next Session`, `### Context to Load`. The overlap is with
new-session handoffs (item 33), not with dream. (gstack's context-save/restore and save-summary
were removed on 2026-09-23.) The nested `claude -p`
inside background jobs, dream-cron, or the night-shift foreman is the shape that hit the
600-second ceiling in August; mitigations are `ECC_HOOKS_ENABLED=false` in those job environments
or a very large `ECC_LLM_SUMMARY_INTERVAL`.

### 25. Stop-time Prettier or Biome plus tsc, and a console-log audit

**Carter:** Need to understand what this is.

**Response.** When Claude finishes a turn, `stop-format-typecheck` formats every JS/TS file edited
this session (Biome or Prettier, whichever the project has) and runs `tsc`. If either fails it
exits 2, so Claude cannot stop until it fixes the errors. `check-console-log` scans the same edited
files for leftover `console.log`. Compared to your PostToolUse `auto-format.sh`: yours formats per
edit and never blocks; ECC's runs once per turn, adds the typecheck, and blocks. In non-JS projects
both are no-ops.

### 26. Stop-time desktop notification

**Carter:** Need to understand what this is.

**Response.** Correction to the earlier list: these are not duplicates. Your hook is on the
Notification event, which fires when Claude is waiting on you (a permission prompt or idle). ECC's
is on Stop, which fires when Claude finishes a turn. So yours says "waiting", ECC's says "done".
You get both only when a turn ends and then a prompt follows.

### 27. Cost tracker, session evaluator, plan-canvas hooks

**Carter:** Could be useful, need to understand it better.

**Response.**

- **cost-tracker** sums token usage across the session transcript at Stop and appends a row to
  `~/.claude/metrics/costs.jsonl`, plus a snapshot for cheap reads. `/ecc:cost-report` reads it.
  This is the data your cost audits currently reconstruct by hand.
- **evaluate-session** is the v1 learning extractor: at Stop it reads the transcript for reusable
  patterns. v2 (item 30) supersedes it via the observer; both run under `standard`.
- **plan-canvas** is a browser UI (`ecc-plan-canvas`) where you annotate a plan and approve or
  request changes. Its two hooks surface open canvas sessions at start and deliver undelivered
  feedback before Claude stops. Writes `~/.claude/plan-canvas/`.

All three are global-state writes from every session, which is the one-owner concern in
`reference-global-state-parallel-sessions`.

### 28. Prior-session context injected at SessionStart

**Carter:** Why would this be useful? I do like that the session-summary is automatic so maybe
this would be useful... need to see what an example session would look like with both setups.

**Response.** What `session-start.js` prints into context, in order: the most recent session
summary for this repo (matched by git common dir, bounded by `ECC_SESSION_START_MAX_CHARS`), then
ranked instincts, then learned skills, then available session aliases, then the detected package
manager and project type.

Your session today opens with MEMORY.md (the index); the project-root-warning SessionStart hook
was removed on 2026-09-23, so no hook of yours runs at session start now. With both:

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

The value is continuity without a handoff step. The cost is that it is a recall layer injected
every session, which your bake-off ruling says to decide on explicitly. Bound it with
`ECC_SESSION_START_MAX_CHARS` for a trial; `ECC_SESSION_START_CONTEXT=off` disables it.

### 29. Compaction nudges on Edit and Write

**Carter:** Why would this be useful?

**Response.** Auto-compaction fires at a fixed percentage regardless of where you are in a task,
sometimes mid-edit. `suggest-compact` counts tool calls (first nudge at 50, then every 25) and
watches transcript size against a window-scaled threshold (160k tokens on a 200k window), and
prints "consider `/compact` now" at those points. Claude sees it and can run your save-summary
first, then compact at a phase boundary before the automatic one hits. With
`autoCompactEnabled: true` both exist; the nudge just moves the moment.

### 30. Let instincts accumulate

**Carter:** Why would this be useful? Need to understand what 'instincts' are.

**Response.** An instinct is a small learned rule with a confidence score, extracted automatically
from observed sessions. Format:

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
---
## Action
Use functional patterns over classes when appropriate.
## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

Pipeline: observe hooks (item 23) → observations in `~/.local/share/ecc-homunculus/projects/<hash>/`
→ instinct files with confidence 0.3 (tentative) to 0.9 (near certain), project-scoped →
injected at SessionStart ranked by confidence (item 28) → `/ecc:instinct-status` to review,
`/ecc:evolve` to cluster instincts into skills, commands, or agents, `/ecc:promote` to move
project instincts to global when the same id appears in 2+ projects with average confidence ≥ 0.8.

Against your two existing mechanisms: capture-feedback is HITL, one confirmed rule per file with
Why and How. Dream is a nightly model run that consolidates into memory. Instincts are automatic
statistical guesses ("observed 5 instances"). Value: patterns you never stated get caught. Risk:
unverified state, auto-injected, which is the thing your ALWAYS.md forbids in memory. Whether
extraction is heuristic or model-driven I did not verify.

### 31. Let promoted instincts become local skills in `~/.claude/skills/learned/`

**Carter:** Leaning towards manual promote but not sure yet.

**Response.** Promotion is already manual; nothing auto-promotes. The automatic parts are
observation and instinct creation, and those stay outside `~/.claude`. So "manual promote" is
the default, not a choice. The remaining decision is narrower: when you do promote, whether the
result may be written as a file under `~/.claude/skills/learned/`, where each one becomes a listed
skill and counts against item 3, or whether you fold it into a skill or feedback file of your own
by hand.

### 32. Use ECC's unified-memory skill

**Carter:** Why would this be useful? I am leaning away from this.

**Response.** Its purpose is cross-harness memory: one store that Claude, Codex, Cursor, and
OpenCode all read, at `<git root>/.ecc/memory/{project,team}` plus `~/.ecc/memory/`, with an
optional MCP server (`ecc-memory-vault`). The one case where it earns its place is Codex reviewing
your Claude output and needing the same context. Otherwise it is a parallel of `.claude/memory/`
and a third store, which is what the two-store thesis in this project's CLAUDE.md warns against.
Leaning away is consistent with that and with one-current-file-per-thing.

### 33. Make ECC's session-data the resume mechanism

**Carter:** I do not want two mechanisms, need to understand both tradeoffs.

**Response.**

| | ECC session-data | Your stack (new-session, close-session) |
|---|---|---|
| Trigger | Automatic at every Stop | Manual, each a deliberate step |
| Where | `~/.claude/session-data/` (global) | `.claude/memory/handoffs/` in the task (new-session), memory files (close-session) |
| Keyed by | Git common dir, most recent first | Task directory, named handoff |
| Reload | Automatic at SessionStart | Pasting the handoff prompt |
| Content | Mechanical: tasks, files, tools, stats; haiku enrichment periodically | Curated: what you chose to capture |
| Retention | Pruned by `ECC_SESSION_RETENTION_DAYS` | Kept until you delete |
| Fits | Continuity across many short sessions | Deliberate handoffs between tracked sessions |

One mechanism means: choosing ECC removes new-session's handoff file (close-session's memory
updates are a different job and stay). context-save/restore went with gstack on 2026-09-23, so
your side is already down to one handoff mechanism. Choosing yours means
`ECC_DISABLED_HOOKS=stop:session-end,session:start` or a profile without them.

### 34. Sync ECC into Codex

**Carter:** Most likely but only once I have decided how it will look in CC.

**Response.** Two Codex paths, pick one. Native: `codex plugin marketplace add affaan-m/ECC` then
`codex plugin add ecc@ecc`; no file merging, Codex owns hook trust. Legacy sync:
`scripts/sync-ecc-to-codex.sh`, which marker-merges an ECC block into `~/.codex/AGENTS.md`,
add-only merges `config.toml` (adding only `chrome-devtools` as MCP), copies prompts and agents,
and installs global git hooks, with a backup first. Your `~/.codex` already registers marketplaces,
so the native path fits its current shape. Neither runs as a side effect of the Claude install.

### 35. Opt into catalog MCP servers

**Carter:** What are the MCP servers?

**Response.** All 33 are opt-in; the plugin registers none. Grouped:

- **Memory:** memory, omega-memory, memxus, longhand (indexes `~/.claude` session history),
  ecc-memory-vault (item 32).
- **Search and research:** exa-web-search (paid key), parallel-search, firecrawl (paid key),
  context7 (you use the `ctx7` CLI instead).
- **Dev platforms:** github (token), vercel, railway, cloudflare docs/builds/bindings/observability,
  supabase (you have the plugin, under review; 0 uses), clickhouse.
- **Browser:** playwright, browserbase (paid), browser-use (paid). Your 2026-09-23 roles:
  agent-browser (general), Chrome DevTools (debugging; no MCP configured, open in `TODO.md`),
  Playwright (end-to-end), Claude in Chrome (backup). ECC's playwright server fits the end-to-end
  role; ECC's Codex sync (item 34) adds a `chrome-devtools` MCP, which is the missing debugging
  piece on the Codex side only.
- **Tracking:** jira, confluence.
- **Media:** fal-ai (paid), magic (UI components).
- **Meta and infra:** nexus (cost proxy), token-optimizer, devfleet (parallel worktree agents),
  filesystem, sequential-thinking, evalview (agent regression tests), codescene, laraplugins,
  ito-compute (unpublished).

ECC's own guidance in the shortform guide: keep 20 to 30 in config, under 10 enabled, under 80
tools active. Your current enabled set is already large (google_workspace, agentmail, granola, reactbits,
and the claude.ai connectors).

### 36. Adopt the `contexts/` shell aliases

**Carter:** Need to compare both options.

**Response.**

| | ECC contexts | Your modes |
|---|---|---|
| What | Three files, 400 to 600 bytes each: dev, research, review | Three directories: research, plan, make, each with CLAUDE.md and skills |
| Load | `claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"` via a shell alias | Walk-up CLAUDE.md loading by cwd, verified in `reference-claude-code-loading-mechanics` |
| Switch | New process only | `cd` into the mode directory |
| Scope | Replaces the system prompt for that process (`--append-system-prompt` is the additive flag; confirm current flag semantics in the CLI docs) | Adds to the default prompt |
| Shipped | Not in the npm package; only in a git checkout | Single-sourced in `~/.claude/modes/` |
| Content | Behavior bullets and a tool-preference list | Principles, conventions, skill homes per mode |

They are orthogonal: a context sets tone for one launch; a mode sets what loads. Nothing in ECC
depends on contexts.
