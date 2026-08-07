# Why skill descriptions silently drop from the catalog

**Researched 2026-08-07** (4 parallel agents: docs · GitHub · community · binary forensics, plus
controlled fixture experiments on this machine). CLI **2.1.224**. Settled — the plan changes this
feeds are in `plan/phase3.md` and the ROADMAP frontmatter-trim item.

## L0 — the answer

Claude Code gives the skills listing a **budget: ~1% of the model's context window** (in chars,
≈8,000 at 200K context). When every skill's `- name: description` line doesn't fit, it keeps
descriptions for the **most-used skills first** and renders the rest as **bare names** — silently.
A name-only skill cannot natural-language trigger; only explicit `/name` works.

**Symlinks were never involved.** Names, descriptions, and natural-language triggering all load
through the full two-hop mode-skills chain (proven by experiment). Symlinked skill dirs are
officially documented as supported.

## The mechanism (provenance: binary forensics, byte-verified in the 2.1.224 executable)

```
all skills ──→ sort by priority = usageCount × max(0.5^(daysSinceLastUse/7), 0.1)
                                  (from the CLI's own usage ledger, ~/.claude/skill-usage.json)
   ↓
Anthropic-bundled skills: always keep full description (exempt)
   ↓
greedy: keep each skill's description while it fits the budget
        budget = contextWindow × 4 chars/token × skillListingBudgetFraction (default 0.01)
   ↓
everyone else: bare `- name` — silent (a warn line exists only in debug logs)
```

- Per-entry cap: `skillListingMaxDescChars`, default **1536** chars (raised from 250 — changelog).
- Frontmatter is parsed by a real YAML parser; parse failure still loads the skill (empty
  metadata, fallback description) — so YAML style was never the variable.
- The loader explicitly accepts symlinked skill dirs (`isDirectory() || isSymbolicLink()`);
  a **broken** symlink is dropped from the list entirely (silently — a swallowed `stat`), it does
  NOT render name-only.
- A separate deliberate mechanism exists: `settings.skillOverrides` can force
  `"name-only"`/`"off"` per skill. **Not set anywhere on this machine** (all scopes checked).

## Consequences that make this hard to notice

- **The evicted set varies session to session.** Usage scores decay weekly and the budget scales
  with the model's context window, so the same catalog drops different skills under different
  models and on different days. It looks like the model being forgetful, not like breakage.
- **This machine is measurably over budget** (live `--debug-file` warning, 2026-08-07):
  `130 skills, 35948 chars > 30000 budget` on the default model → ~16 skills bare per session.
  Smaller-context models fare far worse: at 200K context the budget is only ~8,000 chars — same
  catalog, ~4× over — which is why headless sonnet/haiku probes always evicted the fixture skill.
  Baseline sets captured 2026-08-07 differ per session (`youtube-slide-transcript`, `unfreeze`,
  `init`, `security-review`, `ponytail:*`, `superpowers:*` in one; `sources-cited`, `tdd`,
  `sync-gbrain` in another). Every never/rarely-used skill is at risk every session.

## Evidence trail (provenance labels)

| Evidence | Kind |
| --- | --- |
| Fixture skill (zero usage) always bare; every affected real skill absent from `~/.claude/skill-usage.json`; every showing skill has usage (close-session 102×, browse 75×) | this-machine measurement |
| `{"skillListingBudgetFraction": 0.2}` in the fixture project restored the description **through the two-hop symlink chain** instantly | reproducible experiment |
| Two-hop chain loads name + description + natural-trigger fires (behavioral probe, decoy-controlled) | reproducible experiment |
| `formatCommandsWithinBudget` / priority fn / loader symlink handling | binary extraction, byte offsets in the forensics report |
| Budget + eviction order + `/doctor` + knobs documented | official docs (code.claude.com/docs/en/skills) |
| Known reports: #68677, #57515, #74639, #64606 (closed "not planned"), #57168 (budget uses 200K base even on 1M-context models) | GitHub |
| Teardown corroboration: Windy3f3f3f3f/how-claude-code-works (09-skills-system); claudefa.st budget guide; happyskills.ai eviction formula (matches binary, floor 0.1 confirmed) | community |

## Levers (in order of leverage here)

1. **Trim descriptions** (ROADMAP Phase 3 item) — the budget is aggregate, so every verbose
   description evicts someone else's. Terse gstack-style lines keep the whole catalog alive.
2. **Plan A relocation** — skills moved out of global stop counting in every session that doesn't
   load them.
3. **Raise the budget deliberately**: `skillListingBudgetFraction` in settings (e.g. `0.02`), or
   env `SLASH_COMMAND_TOOL_CHAR_BUDGET=<chars>`. Costs context in every session — a trade, not free.
4. **Free budget by hand**: `skillOverrides: {"<name>": "name-only"}` for skills that only ever
   run by `/name`; the `/skills` UI cycles per-skill states and shows what's actually loaded.
5. **Meters**: `/doctor` (listing cost + biggest contributors), `/context` (post-budget Skills
   row), `--debug` (the over-budget warn line). `/skills` shows per-skill state.

## Key Insights

- **The budget is aggregate, so description length is a commons.** One fat description taxes every
  other skill's chance to trigger. Trimming is not polish; it is the fix.
- **Probabilistic failures get blamed on the model.** Deterministic bugs get found; a skill that
  triggers Monday and not Tuesday reads as model mood. Session-varying eviction hid this for months.
- **Names load unconditionally; descriptions are rationed.** Any test that probes only names
  (including our first sentinel test) proves half the mechanism and the wrong half — triggering
  lives in the description.
- **Usage telemetry decides visibility.** The CLI's own `skill-usage.json` ranks eviction — a new
  skill starts at the back of the line precisely when discovery matters most.

## Open margins (not load-bearing)

- Eviction tie-order among zero-usage skills is unspecified (greedy over a sort with ties) —
  explains why fixture drops flickered between projects. Not worth pinning.
- Enterprise/policy settings scopes for `skillOverrides` unchecked (no such deployment here).
