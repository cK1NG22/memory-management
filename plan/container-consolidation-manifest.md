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

**Sequencing vs the Gen 4 restructure (Carter's question, 2026-08-06):** Carter noted the
deep-but-live folders don't follow the Gen 4 mode structure and asked whether every project should
be restructured *before* memory consolidation. Answer: no — the two are independent, with one
ordering rule. A store keys to the project's **path** (its git root), and the Gen 4 restructure
reorganizes folders *inside* a project — the project's path doesn't change, so memory routed now
stays valid through a later restructure. The hazard runs the other way: any restructure that
**moves or renames a project folder** strands its store. Rule: **route memory only into projects
whose paths are final**; if a Phase 3 restructure will relocate a folder, restructure first or
hold that project's routes. Every Tranche 1 destination is a project root and expected stable.

**Destination safety check (done 2026-08-06):** every proposed destination below is either its own
git toplevel (`balkanski`, `claude-architect`, `memory-management`, `velocity`, `agentic-education`,
`skill-factory`) or a plain non-repo directory — no route creates a stranded repo-subdir store.

**Git-toplevel rules** (Carter asked for the re-explanation; full plan in `plan/ROADMAP.md` Phase 3):
- **Containers** (`~/Projects`, `~/Clients`, `~/Sandbox`, `~/Optimal`, `~/Vault`, …) — **never**
  repos. A container repo would make every non-repo project inside it key to the container's git
  root: all their memory collapses into one shared store.
- **Projects** — **each its own repo.** The git root is exactly what makes all of a project's mode
  folders share one store instead of fragmenting per launch folder.
- **Modes** (`research/`, `plan/`, `make/`) — **never** their own repos. They sit inside the
  project repo; a mode with its own git root gets its own separate store, which is the
  fragmentation git-root keying just solved.
- **Nested projects** (e.g. `velocity` inside `~/Sandbox/builds`) — own repo is fine; the
  *innermost* git root wins.
- **Pre-flight:** never `git init` above an existing keyed store without checking first — a new
  repo above a subfolder-keyed store strands it retroactively.

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

**47 → GLOBAL** (they are rules about how Claude works with Carter anywhere — see Tranche 4;
was 48 until `newsession-focus-ghostty` was ruled DELETE):
automation-observability, bg-isolation-worktree-gitignore, browser-auth-no-arc,
carter-owns-folder-structure, check-conformance-suites, claude-slack-connector-single-workspace,
colocate-co-evolving-tools, cos-as-memory-system-cross-harness, cost-vs-quality-defaults,
default-args-and-mock-patch, design-tokens, dogfood-in-real-contexts, dual-surface-parity,
edit-dev-clone-not-plugin, experiment-md-framing, file-versioning-convention,
folder-proximity-two-audiences, incremental-build-not-scaffold-first, independent-verifier,
insight-blocks, kpi-stress-test, l0l1l2-data-model, main-session-stays-interactive,
mid-plan-clarifications, nmt-annotation, no-option-menus,
no-secrets-in-ai-edited-files, no-softening-asks, no-unverified-state, orchestrator-pattern,
output-home-convention, parallel-jobs-worktree-isolation, parallel-sonnet-research,
personal-apps-free-tier, plain-naming-no-jargon, plan-mode-compact, private-first-iteration,
research-spike-card-shape, research-tech-stack-on-scaffolding, research-to-reference-docs,
root-page-is-not-spec, simplify-first, skill-knowledge-mapping, structured-template-scaffolds,
subagent-model-selection, test-principles-not-projects, unattended-no-dynamic-workflows.

Two exceptions, routed:
- `feedback-pareto-honesty` → `~/Projects/balkanski` — it is a balkanski-specific guardrail.
- `feedback-subskill-vs-reference` — **reframed (Carter, 2026-08-06):** fold it into a
  skill-writing reference file inside the skill-factory repo (it is already codified there as
  BP-034), so it loads when skills are being written rather than sitting as a memory topic.
  Once the reference verifiably covers it, the memory copy is redundant → DELETE.
  (Was Tranche 1: route to the skill-factory store. Now Tranche 2: fold + delete.)

Inside the GLOBAL block, three were **already promoted** into `~/.claude/CLAUDE.md`:
`check-conformance-suites` ("Planning a build"), `file-versioning-convention` ("Files & versions"),
`no-option-menus` (also in `plan/CLAUDE.md`'s mode rules).
**Direction reversed (Carter, 2026-08-06): these come OUT of the global CLAUDE.md.** The topic
files stay canonical and get indexed under mode sections in the sorted MEMORY.md (template below);
mode-`CLAUDE.md` templates are the eventual delivery path into project sessions (Phase 3). No
longer delete candidates. The trade, named honestly: the global CLAUDE.md is the only layer that
loads in *every* session — after demotion these rules auto-load only where a MEMORY.md section or
a mode CLAUDE.md carries them.
And one was **superseded**: `newsession-focus-ghostty` describes the Ghostty split-right
launcher that `/new-session` no longer uses (it stages Agent View now — see
`reference-new-session-agent-view`). **RULED: DELETE (Carter, 2026-08-06)** — moved to Tranche 2.

### user-* (3)

- `meta-user-profile`, `user-carter-schema-design`, `user-profile-consulting` — GLOBAL (facts about Carter, needed everywhere). **APPROVED (Carter, 2026-08-06).**

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
| skill-factory | 8 | yes (8) — hand-append index (was 9; `subskill-vs-reference` reframed to Tranche 2) |
| `~/Sandbox/agentic-education` | 6 | yes (13) — hand-append index |
| `~/Projects/loops` | 5 | **create** |
| `~/Projects/balkanski` | 3 | **create** |
| `~/Optimal/custom-agents` | 2 | **create** |
| dad, claude-architect, ai-engineering, hoth, neon-learning, health-insurance, velocity, interviewer, mana-drive-reorg, compliance, Rebrand, future-of-work | 1 each (12) | dad/claude-architect/velocity/mana-drive-reorg exist; other 8 **create** |
| **Tranche 1 total** | **53** | 12 stores to create, 7 existing |

| Tranche | Files | Blocked on |
| --- | --- | --- |
| 1 — mechanical routes | 53 | Carter's go |
| 2 — move-out / delete / fold | 5 (`plan-pmg-life-app`, `notion-multi-workspace-safety`, `model-configuration-guide`, `newsession-focus-ghostty` **ruled: delete**, `feedback-subskill-vs-reference` **fold into skill-factory reference, then delete**) | per-file confirmation (2 of 5 ruled) |
| 3 — HOLD (automations 5, shifts 1) + ASK 8 + PARKED 12 | 26 | Phase 3.5 / per-file rulings |
| 4 — GLOBAL (incl. the 3 CLAUDE.md-demotion files; mode-sorted in the template below) | 90 | the global-tier decision below |
| **Total** | **174** | |

## Tranche 4 — the global tier (the one real decision)

90 files — the feedback rules, user profiles, and machine references — are needed by sessions in
*every* project. But **no native store loads everywhere**: exactly one store loads per session, so
in a project session the `~/Projects` store (where these files live) does not load. That gap
predates the launch convention and survives it. "Consolidate into project stores" cannot apply
here: copying into N project stores is forking (decided 2026-08-06), and symlinking 90 files × N
stores is the fork surface E5 warned about, at scale.

**Proposal:** keep `~/Projects` as the **canonical global library** — and it genuinely loads for
container-level sessions, which is where cross-project work happens:

1. The files stay where they are. No moves, no copies, no symlink fan-out.
2. Universal *rules* are **not** promoted into `~/.claude/CLAUDE.md` — **reversed by Carter,
   2026-08-06.** Topic files stay canonical; the sorted MEMORY.md's mode sections (template
   below) are the index; the three rules currently living in the global CLAUDE.md get demoted
   back out once their topic files verifiably cover the CLAUDE.md text. Mode-`CLAUDE.md`
   templates (Phase 3, Gen 4 restructure) become the delivery path for mode rules into project
   sessions — they load per-mode in every project, which MEMORY.md sections cannot do.
3. High-value *references* needed by a specific project get the shared-topic-file mechanism (one
   symlink + index line into that project's store) — **after** the four audit.py checks are built.
   First candidate stays `reference-claude-code-loading-mechanics` → this repo's store.
4. A one-line pointer to the global store goes in `~/.claude/CLAUDE.md` (like the
   Model-Configuration-Guide pointer), so any session can *fetch* the library even though nothing
   auto-loads it.

The honest cost: these 90 files still have no auto-recall inside project sessions — same as today.
The per-file fixes are a mode-`CLAUDE.md` template line (mode rules, Phase 3), a shared-file
symlink (project-relevant references, post-audit-checks), or the pointer fetch. Relocation fixes
none of it.

## Execution procedure (runbook seed — capture as `docs/` runbook when run)

1. `audit.py` → must be clean before touching anything (baseline 24/315, verified 2026-08-06).
2. Back up all six source stores to `~/Claude/_archive/container-stores_<date>/` (runbook step 1).
3. Re-verify every destination with `git -C <dir> rev-parse --show-toplevel` — must be the dir
   itself or not-a-repo (the stranded-subdir trap; done once 2026-08-06, redo at execution).
4. Tranche 1 via `route.py` manifests generated from this file — one manifest per source store,
   every file named, run until every store reports `LEFT 0` for the tranche.
5. Indexes: `mkindex.py` ONLY for newly created stores; **hand-append** for the 6 existing
   destination indexes (mkindex overwrites hand-merged lines). Remove moved lines from source
   `MEMORY.md`s — a dangling index line is exactly what audit flags. Every index written or
   rewritten follows the **sorted MEMORY.md template** (below); mkindex output is flat, so
   section it by hand at execution.
6. Fix-in-passing items: the two broken frontmatters (`reference-report-tone-conventions`,
   `feedback-skill-input-design`), the stale interviewer path.
7. `audit.py` again → exit 0. Expected end state: same 315 files minus deletions, more stores,
   `~/Projects` down to the global tier only.
8. Tranches 2/3 per Carter's per-file rulings; Tranche 4 per the global-tier decision — including
   demoting the three promoted rules out of `~/.claude/CLAUDE.md` after verifying each topic file
   fully covers the removed text.

## The sorted MEMORY.md (new dimension — Carter, 2026-08-06)

Carter's addition to the manifest: every MEMORY.md index sorts its entries into
**project-specific** and **mode-specific** sections, so a session sees at a glance which rules
apply to what it is doing. MEMORY.md auto-loads in full every session — the sections don't change
*what* loads, they tell the agent which lines to act on and which topics to fetch for its mode.

**Template — project store:**

```markdown
# MEMORY.md

## Project — always relevant here
- [Title](file.md) — hook

## Research — investigating
## Plan — deciding & designing
## Make — building
(same one-line shape under each)

## References — fetch on demand, any mode
```

**Template — the global library (`~/Projects` store):** same shape, with `Project` replaced by
two sections: `User` (who Carter is) and `Always` (rules that apply in every mode).

**The 90 Tranche 4 files, sorted** (48 feedback + 3 user + 39 references):

- **User (3):** meta-user-profile, user-carter-schema-design, user-profile-consulting.
- **Always (12):** bg-isolation-worktree-gitignore, browser-auth-no-arc, cost-vs-quality-defaults,
  file-versioning-convention, insight-blocks, main-session-stays-interactive, nmt-annotation,
  no-secrets-in-ai-edited-files, no-softening-asks, no-unverified-state, plain-naming-no-jargon,
  unattended-no-dynamic-workflows.
- **Research (6):** independent-verifier, parallel-sonnet-research, research-spike-card-shape,
  research-to-reference-docs, root-page-is-not-spec, test-principles-not-projects.
- **Plan (15):** check-conformance-suites, colocate-co-evolving-tools,
  cos-as-memory-system-cross-harness, dogfood-in-real-contexts, dual-surface-parity,
  folder-proximity-two-audiences, kpi-stress-test, l0l1l2-data-model, mid-plan-clarifications,
  no-option-menus, orchestrator-pattern, personal-apps-free-tier, plan-mode-compact,
  research-tech-stack-on-scaffolding, simplify-first.
- **Make (15):** automation-observability, carter-owns-folder-structure,
  claude-slack-connector-single-workspace, default-args-and-mock-patch, design-tokens,
  edit-dev-clone-not-plugin, experiment-md-framing, incremental-build-not-scaffold-first,
  no-model-names-in-claude-md, output-home-convention, parallel-jobs-worktree-isolation,
  private-first-iteration, skill-knowledge-mapping, structured-template-scaffolds,
  subagent-model-selection.
- **References (39):** the machine/tool references already listed per-store above — one flat
  section, not mode-sorted; they are fetched on demand, not bound to a mode.

Borderline calls, moves welcome: test-principles-not-projects (Research vs Plan),
research-tech-stack-on-scaffolding (Plan vs Research), private-first-iteration (Make vs Plan),
nmt-annotation (Always vs Plan).

Tranche 1 destination indexes use the project template at execution; most routed files land under
**Project**, with per-file mode calls made while hand-appending (e.g. the balkanski QA notes → Make).