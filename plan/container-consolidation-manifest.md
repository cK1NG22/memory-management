# Container-store consolidation — the manifest (Phase 2.5)

**Status: PROPOSAL — nothing has moved.** Drafted 2026-08-06 from `dump.py` descriptions of every
file in the six container stores. Per the orphan-repair precedent: full manifest first, no move
without Carter's approval. Once ruled on, this file is the source for the `route.py` manifests.

**Falsifier:** if Carter's rulings reroute more than ~15% of Tranche 1, the routing rule used here
("narrowest directory from which every session that needs it starts") is not operational and Phase 2.5
needs a different rule before execution.

## Scope: placement, not rescue

**The premise:** sessions launch at `<container>/` (`~/Projects`, `~/Clients`, `~/Sandbox`, …),
`<project>/`, or `<project>/<mode>/` — Carter's launch convention. Container stores therefore
**stay live**: `~/Projects`' 135 topics load whenever a session opens at `~/Projects`.

What makes this migration worth doing anyway (sentinel-proven 2026-08-06): **exactly one store
loads per session — ancestors never stack.** So a project-specific fact filed at container level
loads in container sessions only; it *never* loads in the project sessions that actually consume
it. The balkanski QA notes have never once loaded in a balkanski session. Consolidation is a
**placement** fix: put each fact in the store of the sessions that need it.

Launch history per store, for context on how often container sessions have happened:

| Store | Topics | Last session launched there |
| --- | --- | --- |
| `~/Projects` | 135 | 2026-08-05 |
| `~/Optimal` | 19 | never (0 transcripts) |
| `~/Sandbox` | 10 | 2026-07-22 |
| `~/Sandbox/builds` | 5 | 2026-07-17 |
| `~/Vault` | 4 | never (0 transcripts) |
| `~/Research` | 1 | 2026-07-21 |

**In scope: 174 topic files.** Baseline before any move: `audit.py` clean, 24 stores / 315 topics.

**Explicitly OUT of scope:**
- `/` (1 topic) — cron/headless sessions launch at `/` daily (34 transcripts, newest 2026-08-06);
  its one topic (`project-headless-mcp-path-fix`) serves exactly those sessions. Correctly placed.
- `~` home (0 topics) — live daily; nothing to place anyway.
- The deep-but-live stores (`attio-network-database`, `skill-factory`, `education-philosophy`,
  `memory-systems`) — they load whenever Carter opens sessions there. `skill-factory` is its own git
  toplevel, so it is legal under git-root keying. Whether task-level stores fit the launch convention
  is a separate question; not this migration.
- `~/.claude/skills/restructure-project` (1 topic) — a one-off launch-convention violation, not a
  container store. Footnote for a later sweep.

**Destination safety check (done 2026-08-06):** every proposed destination below is either its own
git toplevel (`balkanski`, `claude-architect`, `memory-management`, `velocity`, `agentic-education`,
`skill-factory`) or a plain non-repo directory — no route creates a stranded repo-subdir store.

## Actions vocabulary

- `→ <path>` — **Tranche 1**, mechanical route to that project's store. Executable on approval.
  The trade of every route: the file gains recall in the project's own sessions and leaves
  container-session recall. That is the right trade for project-specific facts — a project session
  needing its own facts is the common case — but it is a trade, not a free win.
- `GLOBAL` — **Tranche 4**, stays put pending the global-tier ruling (the one real decision, below).
- `HOLD` — **Tranche 3**, destination project doesn't exist yet (automations, shifts); move when it does.
- `PARKED` — **Tranche 3**, dormant idea with no project folder to route to; it stays in the
  container store, which is the honest shelf for it.
- `MOVE-OUT` / `DELETE?` — **Tranche 2**, leaves the memory system entirely. Carter confirms each.
- `ASK` — genuinely ambiguous; Carter rules per-file.

---

## `~/Projects` (135 files)

### feedback-* (50)

**48 → GLOBAL** (they are rules about how Claude works with Carter anywhere — see Tranche 4):
automation-observability, bg-isolation-worktree-gitignore, browser-auth-no-arc,
carter-owns-folder-structure, check-conformance-suites, claude-slack-connector-single-workspace,
colocate-co-evolving-tools, cos-as-memory-system-cross-harness, cost-vs-quality-defaults,
default-args-and-mock-patch, design-tokens, dogfood-in-real-contexts, dual-surface-parity,
edit-dev-clone-not-plugin, experiment-md-framing, file-versioning-convention,
folder-proximity-two-audiences, incremental-build-not-scaffold-first, independent-verifier,
insight-blocks, kpi-stress-test, l0l1l2-data-model, main-session-stays-interactive,
mid-plan-clarifications, newsession-focus-ghostty, nmt-annotation, no-option-menus,
no-secrets-in-ai-edited-files, no-softening-asks, no-unverified-state, orchestrator-pattern,
output-home-convention, parallel-jobs-worktree-isolation, parallel-sonnet-research,
personal-apps-free-tier, plain-naming-no-jargon, plan-mode-compact, private-first-iteration,
research-spike-card-shape, research-tech-stack-on-scaffolding, research-to-reference-docs,
root-page-is-not-spec, simplify-first, skill-knowledge-mapping, structured-template-scaffolds,
subagent-model-selection, test-principles-not-projects, unattended-no-dynamic-workflows.

Two exceptions, routed:
- `feedback-pareto-honesty` → `~/Projects/balkanski` — it is a balkanski-specific guardrail.
- `feedback-subskill-vs-reference` → `~/Optimal/optimal-claude-skills/skill-factory` — codified there as BP-034.

Inside the GLOBAL block, three are **already promoted** into `~/.claude/CLAUDE.md` and are
DELETE? candidates once the CLAUDE.md text is verified to fully cover them:
`check-conformance-suites` ("Planning a build"), `file-versioning-convention` ("Files & versions"),
`no-option-menus` (promoted into `plan/CLAUDE.md`'s mode rules).
And one is likely **superseded**: `newsession-focus-ghostty` describes the Ghostty split-right
launcher that `/new-session` no longer uses (it stages Agent View now — see
`reference-new-session-agent-view`). DELETE? pending Carter.
(These four stay counted in Tranche 4 until ruled on — each file lives in exactly one tranche.)

### user-* (3)

- `meta-user-profile`, `user-carter-schema-design`, `user-profile-consulting` — GLOBAL (facts about Carter, needed everywhere).

### project / tooling / misc (41)

- `autoresearch-chain-testing-todo` → skill-factory
- `autoresearch-research` → skill-factory
- `codex-skill-portability` — GLOBAL (machine tooling)
- `email-tracker-redesign` — HOLD (automations project, Phase 3.5)
- `gemini-cli-free-tier-dead` — GLOBAL (machine fact)
- `github-digest-spec` — HOLD (automations)
- `loops-source-library` → `~/Projects/loops`
- `loops-transcribe-media-skill` → `~/Projects/loops`
- `plan-pmg-life-app` — **MOVE-OUT**: a 35KB Opus build plan, not a memory (the Locker precedent —
  plans written into a memory folder because it was the nearest writable place). Propose
  `~/Projects/Archive/pmg-life-app-plan.md`, or a new project folder if Carter intends to build it.
- `project-agent-dreaming-dogfood` → memory-management (roadmap: dream stays with memory-management)
- `project-ai-engineering-curriculum` → `~/Projects/ai-engineering`
- `project-browser-auth-skill-idea` — PARKED (backlog idea, no folder)
- `project-browser-settings-automation-skill` — PARKED
- `project-canvas-lti-edtech` → `~/Sandbox/agentic-education` (education venture umbrella) — flag: parked venture, could stay PARKED instead
- `project-claude-architect` → `~/Projects/claude-architect`
- `project-dad-projects` → `~/Projects/dad`
- `project-decide-skill` — GLOBAL (pointer to a machine-level skill)
- `project-distributed-compute-harvesting` — PARKED
- `project-hoth-ai-systems-proposal` → `~/Projects/hoth`
- `project-instantly-campaigns-live` → `~/Clients/outreach`
- `project-memory-bakeoff` → memory-management
- `project-memory-management` → memory-management
- `project-mode-structure-review` → memory-management
- `project-move-project-skill-idea` → memory-management (this repo's roadmap links it)
- `project-orchestrator-agent-deferred` — PARKED — flag: arguably memory-management (context-window management is its domain)
- `project-sandbox-build-ideas` — ASK: describes `~/Sandbox/builds/BUILD-IDEAS.md`; `builds/` is a
  sub-container between container and project. Narrowest real consumer unclear (velocity? each build?
  `builds/` itself, if Carter launches sessions there?).
- `project-slack-cron-convergence` — HOLD (automations)
- `project-team-cli-agent`, `-idea`, `-philosophy`, `-substrate-shape`, `-v01-build-notes`,
  `-automations-vision` (6 files) — PARKED (dormant R&D, no code folder exists)
- `project-workout-bot` — HOLD (automations)
- `tooling-cross-app-instructions` — GLOBAL
- `tooling-skill-chain-mapper-idea` → skill-factory — flag: could stay PARKED
- `tooling-skill-usage-tracker` — GLOBAL (machine pointer)
- `tooling-skill-writing-patterns` → skill-factory
- `tooling-skills-ecosystem-todos` → skill-factory
- `velocity-model-caliper` → `~/Sandbox/builds/velocity`
- `x-twitter-live-login-needed` — GLOBAL (machine fact)

### reference-* (41)

Routed / held / delete-candidate (11):
- `reference-apollo-credit-cycle` → `~/Clients/outreach` (the gate on the lead engine)
- `reference-balkanski-ios-qa` → `~/Projects/balkanski`
- `reference-balkanski-project` → `~/Projects/balkanski`
- `reference-health-insurance-2026` → `~/Projects/health-insurance`
- `reference-kinds-of-loops` → `~/Projects/loops`
- `reference-sakana-fugu` → `~/Projects/loops` (agent-loop pattern study) — flag-lite
- `reference-memory-systems-history` → memory-management (pointer to this repo's own doc)
- `reference-agent-memory-systems` → memory-management (the competitor space this project tracks)
- `reference-neon-study-guide` → `~/Projects/neon-learning`
- `reference-cron-scheduling` — HOLD (automations) — flag: half machine-reference; GLOBAL acceptable
- `reference-notion-multi-workspace-safety` — **DELETE?** — roadmap open question #3 already marks it
  unreferenced-delete-when-ready. Carter confirms.

GLOBAL (30 — machine/tooling references usable from any project):
agent-ecosystem-taxonomy, agent-teams-setup, ai-digest-archive, anthropic-billing-june-2026,
bumblebee-supply-chain-scanner, claude-code-loading-mechanics (**canonical for the shared-file
mechanism** — the design doc's first symlink candidate into this repo's store, blocked on the four
audit checks), claude-code-private-marketplace-auth, claude-in-slack, code-graphs,
code-review-resources, copilotkit, desktop-vs-terminal-tokens, finder-alternatives, firecrawl,
gdrive-disk-navigation, kickbacks-ai-evaluation, new-session-agent-view, plugin-clone-no-local-branches,
pptx-shape-defaults, pptx-superscripts, pptx-theme-recolor, projects-structure, reactbits-mcp,
report-tone-conventions (**broken frontmatter — no description; fix while touching it**),
sandbox-ing-app, slack-integration, tech-stack-decision-trees, tenex-content-engine,
transcript-cleanup-skills, workspace-mcp-attachments-dir.

---

## `~/Sandbox` (10 files)

- `claude-code-june-2026-release-learnings` → `~/Projects/loops` (description says it IS the loops hub) — flag-lite: filename/description mismatch
- `feedback-no-model-names-in-claude-md` — GLOBAL
- `project-agentic-education` → `~/Sandbox/agentic-education`
- `project-agentic-lms` → `~/Sandbox/agentic-education`
- `project-dream-shift` → memory-management — flag: it is also a launchd job; automations is defensible. Proposed per roadmap's "dream stays with memory-management."
- `project-grounded-retrieval-experiment` — PARKED
- `project-three-shift-system` — HOLD (shifts placement is an explicit Phase 3.5 open item)
- `reference-free-social-readers` — GLOBAL
- `reference-model-configuration-guide` — **DELETE?** — pure pointer to
  `~/Sandbox/Model-Configuration-Guide.md`, which `~/.claude/CLAUDE.md` already references directly. Redundant.
- `reference-transcribe-and-map-slides` — GLOBAL (skill pointer)

## `~/Sandbox/builds` (5 files)

- `feedback-enforced-floor-is-the-spec` → skill-factory (skill-writing rule)
- `project-ai-adoption-tracker` — PARKED (approved spec, never built, no folder)
- `project-ai-lms-authoring-skills` → `~/Sandbox/agentic-education`
- `project-ai-lms-objectives-have-no-home` → `~/Sandbox/agentic-education`
- `reference-canvas-api-write-payloads` → `~/Sandbox/agentic-education` (the file it points at lives in that tree)

## `~/Optimal` (19 files)

- `feedback-generalize-distributed-docs` — ASK: Optimal-wide rule; no single Optimal store loads everywhere (the global problem at container scope)
- `feedback-human-launch-trigger` → `~/Clients/outreach`
- `feedback-keep-standalone-on-plugin-cutover` — ASK: same Optimal-wide class (or skill-factory)
- `feedback-outreach-voice` → `~/Clients/outreach`
- `feedback-skill-input-design` — ASK: same class; **also has broken frontmatter (no description)**
- `project-awardco-lead` → `~/Clients/outreach`
- `project-client-skills-task-type` → skill-factory — flag: shipping mechanism lives in that repo
- `project-custom-agents` → `~/Optimal/custom-agents`
- `project-instantly-batch2-loaded` → `~/Clients/outreach`
- `project-instantly-copilot` → `~/Clients/outreach`
- `project-interviewer` → `~/Optimal/interviewer` — **its description still says `~/Projects/Optimal/interviewer/`, stale since the June reorg; fix while moving**
- `project-luke-staffing-engagement` → `~/Clients/outreach`
- `project-mana-drive-reorg` → `~/Optimal/mana-drive-reorg` (store exists, 1 topic)
- `project-optimal-compliance-posture` → `~/Optimal/compliance`
- `project-optimal-rebrand` → `~/Optimal/Rebrand`
- `project-outreach-state` → `~/Clients/outreach`
- `project-pricing-model-v2` — ASK: pricing/deck work has no folder (`pricing-v2-spec.md` sits loose at `~/Optimal` root); Rebrand is the nearest candidate
- `reference-client-skill-install-prompt` → skill-factory — flag: same reasoning as client-skills-task-type
- `reference-hermes-architecture` → `~/Optimal/custom-agents`

## `~/Vault` (4 files)

- `feedback-drill-design-principles` — ASK: drill/MCQ-writing rules — claude-architect (cert drills), education-philosophy, or GLOBAL?
- `feedback-never-leak-answer-keys` — ASK: same ruling as above; the two travel together
- `hub-future-of-business` → `~/Sandbox/future-of-work` — flag-lite: name-match is strong, confirm
- `project-standard-works-vault` — ASK: the vault it describes is NOT under `~/Vault` (only
  `education-philosophy` and two PDFs are there); locate the real vault folder first, else PARKED

## `~/Research` (1 file)

- `reorg-research-into-projects` — GLOBAL (machine-layout fact: where research topics went when `~/Research` was dissolved)

---

## Summary by destination (Tranche 1 — executable on approval)

| Destination store | Files | Store exists? |
| --- | --- | --- |
| memory-management (this repo) | 8 | **create** (repo-root store is currently empty) |
| `~/Clients/outreach` | 9 | yes (7 topics) — hand-append index |
| skill-factory | 9 | yes (8) — hand-append index |
| `~/Sandbox/agentic-education` | 6 | yes (13) — hand-append index |
| `~/Projects/loops` | 5 | **create** |
| `~/Projects/balkanski` | 3 | **create** |
| `~/Optimal/custom-agents` | 2 | **create** |
| dad, claude-architect, ai-engineering, hoth, neon-learning, health-insurance, velocity, interviewer, mana-drive-reorg, compliance, Rebrand, future-of-work | 1 each (12) | dad/claude-architect/velocity/mana-drive-reorg exist; other 8 **create** |
| **Tranche 1 total** | **54** | 12 stores to create, 7 existing |

| Tranche | Files | Blocked on |
| --- | --- | --- |
| 1 — mechanical routes | 54 | Carter's go |
| 2 — move-out / delete candidates | 3 (`plan-pmg-life-app`, `notion-multi-workspace-safety`, `model-configuration-guide`) | per-file confirmation |
| 3 — HOLD (automations 5, shifts 1) + ASK 8 + PARKED 12 | 26 | Phase 3.5 / per-file rulings |
| 4 — GLOBAL (incl. 4 delete-candidate flags: the 3 promoted rules + `newsession-focus-ghostty`) | 91 | the global-tier decision below |
| **Total** | **174** | |

## Tranche 4 — the global tier (the one real decision)

91 files — the feedback rules, user profiles, and machine references — are needed by sessions in
*every* project. But **no native store loads everywhere**: exactly one store loads per session, so
in a project session the `~/Projects` store (where these files live) does not load. That gap
predates the launch convention and survives it. "Consolidate into project stores" cannot apply
here: copying into N project stores is forking (decided 2026-08-06), and symlinking 91 files × N
stores is the fork surface E5 warned about, at scale.

**Proposal:** keep `~/Projects` as the **canonical global library** — and it genuinely loads for
container-level sessions, which is where cross-project work happens:

1. The files stay where they are. No moves, no copies, no symlink fan-out.
2. Truly universal *rules* get promoted up the ladder (`~/.claude/CLAUDE.md`, mode templates) —
   that is Phase 2's promotion question, already on the roadmap, and three files show it works
   (conformance-suites, file-versioning, no-option-menus are already living in CLAUDE.md).
3. High-value *references* needed by a specific project get the shared-topic-file mechanism (one
   symlink + index line into that project's store) — **after** the four audit.py checks are built.
   First candidate stays `reference-claude-code-loading-mechanics` → this repo's store.
4. A one-line pointer to the global store goes in `~/.claude/CLAUDE.md` (like the
   Model-Configuration-Guide pointer), so any session can *fetch* the library even though nothing
   auto-loads it.

The honest cost: these 91 files still have no auto-recall inside project sessions — same as today.
The per-file fixes are promotion (universal rules), a shared-file symlink (project-relevant
references, post-audit-checks), or the pointer fetch. Relocation fixes none of it.

## Execution procedure (runbook seed — capture as `docs/` runbook when run)

1. `audit.py` → must be clean before touching anything (baseline 24/315, verified 2026-08-06).
2. Back up all six source stores to `~/Claude/_archive/container-stores_<date>/` (runbook step 1).
3. Re-verify every destination with `git -C <dir> rev-parse --show-toplevel` — must be the dir
   itself or not-a-repo (the stranded-subdir trap; done once 2026-08-06, redo at execution).
4. Tranche 1 via `route.py` manifests generated from this file — one manifest per source store,
   every file named, run until every store reports `LEFT 0` for the tranche.
5. Indexes: `mkindex.py` ONLY for newly created stores; **hand-append** for the 6 existing
   destination indexes (mkindex overwrites hand-merged lines). Remove moved lines from source
   `MEMORY.md`s — a dangling index line is exactly what audit flags.
6. Fix-in-passing items: the two broken frontmatters (`reference-report-tone-conventions`,
   `feedback-skill-input-design`), the stale interviewer path.
7. `audit.py` again → exit 0. Expected end state: same 315 files minus deletions, more stores,
   `~/Projects` down to the global tier only.
8. Tranches 2/3 per Carter's per-file rulings; Tranche 4 per the global-tier decision.
