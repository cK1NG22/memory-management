# Phase 3 plan — restamp projects, then move the last skills

*(was `skill-relocation-plan.md` — renamed 2026-08-07 when the restructure plan joined it, so both
review together)*

**Status:** approved (Carter, 2026-08-07). The two ❓ calls in Plan A stay open — approval didn't
rule them. Everything below "Plan record" is the measured record from 2026-08-05/06 — unchanged,
still the inventory of what already moved.

## The order (one gate, then B unblocks A)

```
sentinel test ──→ B. restamp every project ──→ A. move the last 15 skills ──→ re-measure floor
(⚠️ SPLIT result    (git init the 9 + wire      (build mode skill homes,      (free — next normal
 — Plan A step 1)    mode CLAUDE.mds+links)      delete global entries)        session start)
```

B before A: the 15 skills will load *through* project wiring — move them first and they load
nowhere. The sentinel test is first because it's cheap and gates both.

---

## Plan A — finish moving skills out of global

Where the 96 remaining global skills go (81 already ruled — only the bottom two rows move):

```
global 96 ─┬─ 53 gstack           → stay   (installer puts them back; only ~1.1K tokens)
           ├─ 17 cross-cutting    → stay   (used from anywhere by design)
           ├─  8 cron/path-locked → stay   (automations project frees them later — Phase 3.5)
           ├─  2 special          → stay   (ui-ux-pro-max managed elsewhere; retire
           │                                restructure-project after Plan B replaces it)
           ├─  1 resolve-vulns    → ❓ Carter (candidate: future automations project)
           └─ 15 mode-home        → MOVE after Plan B:
                  plan/      ← kpi-setter · opusplan
                  research/  ← sources-cited · youtube-slide-transcript
                  make/      ← api-design · architecture-review · database-design · dung
                             · mcp-builder · tdd · vercel-deploy-claimable
                  make/❓    ← docx · pdf · pptx · xlsx  (Carter: make/, or stay global?)
```

Steps:

```
1. ⚠️ sentinel test SPLIT (2026-08-07, CLI 2.1.224, headless probes + decoy control):
      skill NAMES load through folder-level + two-hop symlinks ✓
      natural-language triggering works when the description is in context ✓ (behavioral probe)
      DESCRIPTIONS never appeared through the symlink chain in the headless fixtures ✗
        (production is mixed: notion-transcript shows, discovery-call-prep doesn't)
      a DEAD folder link is SILENT (exit 0, no warning) → step 4's scan is mandatory
      A name-only skill fires only by explicit /name — natural triggering dies with the
      description. GATE: interactive probe of the fixture before any skill moves
      (headless may index skills differently — untestable from a bg job).
2. build the mode homes:  ~/.claude/modes/<mode>/skills/<skill> → canonical home
3. AFTER Plan B: delete the 15 global entries
4. verify each skill loads from exactly ONE place (extend audit.py scan) — then re-measure floor
```

**Deletes:** the 15 global entries (step 3) — verified gone by the step-4 one-place scan.
**Falsifier:** probe a stamped project's mode dir; if a moved skill doesn't load, the chain is
broken → relink to global (nothing is deleted until probes pass).

---

## Plan B — restamp every project to the mode shape

Target shape (this repo is the working model):

```
<project>/                    ← its own git repo (9 still aren't — init below)
├── CLAUDE.md                 ← what this project is + how to navigate it
├── research/
│   ├── CLAUDE.md             ← thin: which mode + directions, ends with @RESEARCH-MODE.md
│   ├── RESEARCH-MODE.md      → ~/.claude/modes/RESEARCH-MODE.md      (symlink, abs target)
│   └── .claude/skills        → ~/.claude/modes/research/skills/      (symlink — Plan A)
├── plan/   ← same three-piece wiring
├── make/   ← same three-piece wiring
└── .claude/memory/           ← once, at project root — never per mode
```

Per project (= mode-files runbook step 5, plus the git pre-flight):

```
audit.py clean
   ↓
pre-flight: any native store keyed to a SUBfolder of this project?
   → resolve it first (git init above it would strand it)
   ↓
git init — only the 9 non-repos: dad · hoth · loops · ai-engineering · neon-learning
           · health-insurance · outreach · mana-ventures · custom-agents
   ↓
make mode folders → write thin CLAUDE.mds → ln -s the three mode files
   ↓
probe: claude -p from a mode dir — is a mode-file-only phrase in context?
   ↓
audit.py exit 0   (its imports check now watches this project forever)
```

Rules that bound the work:

- **Containers (`~/Projects` etc.) stay non-repos** — a repo there swallows every project's store.
- Gen 3 task folders map into modes **where they fit; stay put where they don't.** No forcing.
- One project at a time, probe each — a failed probe stops the line, not the audit three
  projects later.

After ALL projects pass:

- remove `# Planning a build` from `~/.claude/CLAUDE.md` (marked with a comment) — only now is
  the removal recall-neutral (its content lives in PLAN-MODE.md, which needs the wiring to load)
- Plan A steps 3–4 unblock

**Deletes:** the `# Planning a build` section (recall-neutral check above is its verification).
**Falsifier:** any post-stamp probe fails → the wiring pattern is wrong; stop stamping, fix the
pattern, re-probe the already-stamped projects before continuing.

---

# Plan record — skill relocation, measured (2026-08-05/06)

## The measurement (2026-08-05, before any relocation)

- **Session context floor: 44K–55K tokens** at session start, consistent across eight recent
  sessions in different projects (read from `cache_creation_input_tokens` +
  `cache_read_input_tokens` in the session `.jsonl` files — the same data `/context-dashboard`
  will read).
- **Global skill catalog: 113 skills, ~31,350 chars of name+description ≈ ~7,800 tokens** loading
  into every session. The roadmap's "~130 at ~11K" estimate was close but high. Real share of the
  floor: **~15–18%**.
- Measured **after** fixing the dead symlinks, deliberately — a dead symlink is a skill that
  silently doesn't load, so measuring first would have produced a baseline ~12 skills lighter
  than the system's true state.

## The mechanism (verified, see `[[reference-claude-code-loading-mechanics]]`)

`.claude/skills/` inside any folder loads **only when cwd is that folder or below**. Global
`~/.claude/skills/` loads everywhere, always, and folders can add skills but never subtract.
So the only lever is moving a skill's entry out of global into the narrowest folder it's used
from — it then costs nothing outside that folder and behaves identically inside it.

## Executed — tranche 1 (2026-08-05)

The 11 skills that already lived outside global and were only *symlinked* in. Global symlink
removed; a project-level symlink created so they still load where the work happens:

| Skill | Now loads under | Points at |
| --- | --- | --- |
| `411-case` `411-deck` `411-refine` `411-reresearch` `411-research` | `~/School/` | `~/School/strat-411-skills/` |
| `discovery-call-prep` | `~/Optimal/` | `~/Optimal/optimal-claude-skills/` |
| `skill-compliance` `skill-factory` `skill-spec-validator` `skill-to-spec` | `~/Optimal/` | `~/Optimal/optimal-claude-skills/skill-factory/` |
| `acme-board-memo` | `~/Optimal/` | `~/Claude/skill-factory/acme-acme-board-memo/assembled/acme-board-memo` |

**Result: 102 global skills (was 113), ~1,440 tokens removed from every session.**
Rollback for any of them: `ln -s <target> ~/.claude/skills/<name>` — one command, nothing was
deleted. (`acme-board-memo` points at a skill-factory build-output folder — works, but if the
skill matters long-term it deserves a stable home. Carter's call.)

## What stays global (do not relocate)

- **Path-locked:** `gstack` — referenced by absolute path in `~/.claude/CLAUDE.md` and
  `settings.json` allow rules.
- **Cron-locked:** `email-tracker`, `github-digest`, `workout-bot` — invoked by launchd jobs that
  run headless from arbitrary cwds. Also the shift/dream family (`night-shift`, `day-shift`,
  `morning-shift`, `dream`) for the same reason.
- **Cross-cutting workflow:** `close-session`, `new-session`, `capture-feedback`,
  `file-versioning`, `brain-dump`, `decide`, `memory-review`, `skill-creator`, `scout-stack`,
  `claude-audit`, and similar — used from anywhere by design.

## The gstack finding — the biggest single block

**53 of the 113 skills are gstack-family** (installed and regenerated by
`~/.claude/skills/gstack && ./setup`). Hand-moving them fights the installer — the next `./setup`
puts them back. But they're terse: all 53 together cost only **~1,100 tokens**. Recommendation:
**leave them alone.** The token win is small and the fight with the installer is permanent. If
gstack ever grows a scoped-install option, revisit; the iOS five (`ios-*`) would be the first to
scope down to iOS projects.

## Remaining candidates — Carter's call (physical moves, not symlink flips)

These are real directories inside `~/.claude/skills/`, so relocating means moving files —
and Carter owns folder structure. Recommended destinations:

- `check-understanding`, `find-your-level` → the AI Engineering curriculum project
- `daily-standup`, `source-leads` → `~/Optimal/`
- `notion-transcript` → **retire** (Carter left Notion; same status as the unreferenced Notion
  memory file)
- `connect-vault` → `~/Research/`
- `resolve-vulns` → alongside the supply-chain scan in `~/Claude/`
- File-type skills (`xlsx` `docx` `pptx` `pdf`, ~750 tokens) — **open question #2 on the
  roadmap**; they key off file type, not place or activity, so no folder is obviously right.
  Recommendation: stay global until the mode structure exists, then `make/`.

Everything in this section together is worth roughly another ~1,500–2,000 tokens.

## Re-measure

The analytic delta is above (7.8K → ~6.4K catalog). The honest floor number comes free from the
**next normal session start** — read the first request's `cache_creation_input_tokens` in its
`.jsonl` (a fresh headless `claude -p` run would also measure it, but that bills the separate
programmatic credit pool; not worth it when the next real session measures it for free).

## The mode-skill shape (decided 2026-08-05)

Skills reach a mode through **two symlink hops**, and the project-side hop is one link for the
whole folder, not one per skill:

```
<project>/plan/.claude/skills  →  ~/.claude/modes/plan/skills/   (ONE folder-level link per project)
                                   ├── writing-plans  →  <canonical home>
                                   └── kpi-setter     →  <canonical home>   (per-skill links, kept once)
```

*Why folder-level on the project side:* adding a skill to `~/.claude/modes/plan/skills/` makes it
appear in **every project instantly** — no rescaffolding. Per-skill links in each project would
need a re-scaffold on every addition.

*Why per-skill inside the mode home:* the skill itself still lives once, in its canonical repo or
folder, so editing it stays centralized.

**Open verification before building on this:** per-skill symlinks are proven to load; a symlinked
*parent* `skills/` folder is not yet sentinel-tested. Test it before the mode templates are
written. Double-loading is prevented by the invariant — **each skill loads from exactly one
place** (global, a project, or a mode home) — enforced by a scan (extend `audit.py` /
`/move-project --check` to flag any skill name reachable twice), never by scaffolding care.

## Appendix — every skill's proposed load location (complete, generated from disk 2026-08-05)

**Already relocated — done:**
- `~/School/.claude/skills/` (5): `411-case` `411-deck` `411-refine` `411-reresearch` `411-research`
- `~/Optimal/.claude/skills/` (6): `discovery-call-prep` `skill-compliance` `skill-factory`
  `skill-spec-validator` `skill-to-spec` `acme-board-memo`

**Stay global — locked (8):**
- Cron: `email-tracker` `github-digest` `workout-bot`
- Headless shifts: `day-shift` `night-shift` `morning-shift` `dream`
- Path-locked: `gstack` (in CLAUDE.md + settings.json)

**Stay global — gstack family (53, installer-owned, ~1.1K tokens total):**
`_gstack-command` `autoplan` `benchmark` `benchmark-models` `browse` `canary` `careful` `codex`
`connect-chrome` `context-restore` `context-save` `cso` `design-consultation` `design-html`
`design-review` `design-shotgun` `devex-review` `document-generate` `document-release` `freeze`
`gstack-upgrade` `guard` `health` `investigate` `ios-clean` `ios-design-review` `ios-fix` `ios-qa`
`ios-sync` `land-and-deploy` `landing-report` `make-pdf` `office-hours` `open-gstack-browser`
`pair-agent` `plan-ceo-review` `plan-design-review` `plan-devex-review` `plan-eng-review`
`plan-tune` `qa` `qa-only` `retro` `review` `scrape` `setup-browser-cookies` `setup-gbrain` `ship`
`skillify` `spec` `sync-gbrain` `unfreeze` — plus `setup-deploy` (gstack-adjacent)

**Stay global — cross-cutting workflow (17):**
`autoresearch` `brain-dump` `capture-feedback` `claude-audit` `clean-transcript` `close-session`
`decide` `doc-coauthoring` `file-versioning` `learn` `locker` `memory-review` `new-project`
`new-session` `scout-stack` `skill-creator` `transcribe-media`

**Stay global — special cases (2):**
- `ui-ux-pro-max` — a link into `~/.agents/skills/`, managed there; leave.
- `restructure-project` — retire once the mode scaffold replaces it (it builds the Gen 3 shape).

**Moved to a project — approved and executed 2026-08-05 (tranche 2):**
- `check-understanding` `find-your-level` → `~/Projects/ai-engineering/.claude/skills/` (real
  dirs; their content paths were already absolute, so nothing broke)
- `daily-standup` `source-leads` `notion-transcript` → `~/Optimal/optimal-claude-skills/`
  (canonical home, a git repo — the three arrive as uncommitted new files for Carter), linked
  from `~/Optimal/.claude/skills/`. Carter kept `notion-transcript` rather than retiring it.
- `connect-vault` → `~/Research/.claude/skills/` (real dir — no separate canonical home exists
  for Research)

**Parked — Carter undecided (1):** `resolve-vulns` stays global until he knows what he wants
for it (candidate home was next to the supply-chain scan; may instead belong to a future
automations project — see below).

**Global after tranche 2: 96 skills** (day started at 113).

**Move to a mode home — after the mode rollout (15):**
- `plan/`: `kpi-setter` `opusplan`
- `research/`: `sources-cited` `youtube-slide-transcript`
- `make/`: `api-design` `architecture-review` `database-design` `dung` `mcp-builder` `tdd`
  `vercel-deploy-claimable`
- `make/?` — the file-type four, open question #2: `docx` `pdf` `pptx` `xlsx`

## Proposed: an automations project (Carter's idea, 2026-08-05)

A dedicated project as the workspace for the cron jobs — and the mechanism that makes it more
than tidiness: **launchd plists support a `WorkingDirectory` key** (the supply-chain-scan plist
already uses it). Pin each cron's working directory to the project and the "cron-locked" global
category dissolves — `email-tracker`, `github-digest`, `workout-bot`, and the shifts could all
load from the project's `.claude/skills/` instead of taxing every session. It also gives the
crons what they currently lack: one project memory, one roadmap, and one home for the
observability convention, instead of state scattered across `~/Library/LaunchAgents/`,
`~/.claude/state/`, and `~/Claude/`. Plists themselves stay in `~/Library/LaunchAgents/`
(launchd requires it); the project documents them.

**Dream is the exception:** its rules *are* memory policy (the Phase 2 promotion ladder), and
the colocate principle says a tool and its rubric live together or the rubric goes stale — so
dream belongs with memory-management, not the automations project. Carter's call.

## Open: shifts under the mode structure (resolve later)

Carter's direction: `day-shift`/`night-shift`/`morning-shift` execution should land in the
`make/` of the relevant projects — possibly `make/shift-work/`. Unresolved tension to design
around: the shift *foreman* is cross-project (it works a queue spanning projects), while the
*work* belongs to each project's `make/`. Likely shape: the skill stays loadable wherever the
foreman starts; per-project shift state lands in that project's `make/shift-work/`. Not blocking
anything now.

## Fragility guard

Project-level skill symlinks are **the same fragile kind that died in the June reorg** — they die
silently if either end moves. `make/memory-repair/audit.py` doesn't check them today; the check
belongs in `/move-project --check`, and until that exists, this file is the inventory of where
every relocated symlink points.
