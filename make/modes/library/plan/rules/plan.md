# PLAN — mode principles

Loads when a session starts in a project's `plan/` folder, from `plan/.claude/rules/`.
Each project holds a copy of the mode library's file. Edit the library, then re-stamp; `modes.py
check` reports copies that differ.

## Shaping the plan

- **Simplify first, always.** Start with the absolute minimum that solves the stated problem; add
  infrastructure (databases, auth, routing) only when the simple path genuinely can't work. Before
  proposing backend/infra, ask whether what's already deployed solves it.
- **No option menus.** Don't enumerate named, pre-built options where reasoning is wanted — a menu
  turns design into selection, and under pressure the cheap pick-from-three path replaces the
  open-ended thinking it was meant to illustrate. Give the tests that generate an answer. This
  applies to anything Claude reads later (skills, prompts, plans) *and* to Carter live: prefer an
  open text prompt over multiple-choice for premise challenges, scope calls, and architecture
  tradeoffs (multiple-choice is still right for mode routing, status flags, yes/no approvals).
  Beware: a single worked example anchors as hard as a labeled list and hides better — the tell is
  whether the text can be *copied* rather than *applied*.
- **Persist decisions into in-repo files before any build starts.** A settled plan or design that
  lives only in the plan file (`~/.claude/plans/…`), the transcript, or chat is invisible to the
  next session and dies with compaction. Planning is not finished at "plan approved" — it is
  finished when the decisions are written into the repo they govern (a `DESIGN.md` beside the build
  location, plus updates to `TODO.md` and any docs the decisions change) and committed. Origin:
  2026-08-20 copilot-agent fan-out grilling — four rounds of settled decisions existed nowhere but
  the plan file until Carter asked whether they had been persisted.
- **Mid-plan clarification docs are authoritative.** When Carter drops a CLARIFICATIONS.md or spec
  doc partway through planning, it supersedes the original brief and any conflicting plan content —
  rewrite to match rather than merging, defer to his designs (schemas, curricula) rather than
  re-proposing, and track remaining open questions in a dedicated section without blocking on them.
- **Carter sometimes designs the schema himself — defer to it.**
- **A format spec without numbers is not a spec.** When Carter supplies an approved artifact as the
  requirement ("follow this template"), the plan is not ready until it carries the limits that make a
  second run come out like the first: min *and* max per unit, the source/evidence floors, the date
  cutoffs, and how the shape differs across the obvious variants. Derive every number by **measuring
  the artifact**, print the observed range next to the limit so a limit that contradicts its own
  evidence is visible, and make the artifact itself test #1 — if the approved thing fails the rules,
  the rules are wrong. Read the artifact's *structure*, not just its rendered text (for `.docx` and
  `.pptx` that means the XML), because the load-bearing conventions live there.

## Testing and quality

- **Check conformance suites before writing any test plan.** Suites written against a published
  *standard* run over code we wrote: axe-core/Lighthouse for web UI, Test262/WPT for JS engines,
  schemathesis/JSON-Schema suite for APIs — usually one dev-dependency. Name the ones that apply,
  what they cost, and say plainly what they can never cover (the product's own business rules —
  those still need hand-written tests). Wire them early: a red suite on day 1 is a work-list, on
  day 90 a rewrite. Check what the repo already borrows (ESLint packs and type-checkers count).
  Where to look, by domain:

  | If the build has… | Look for |
  |---|---|
  | any web UI | **axe-core** (WCAG), **Lighthouse CI**, html-validate |
  | a JS runtime/engine, or a parser | **Test262**, **Web Platform Tests** |
  | an HTTP API | schemathesis, **OpenAPI/JSON-Schema Test Suite**, `httpwg` tests |
  | a protocol implementation | the reference suite (**Autobahn** for WebSocket, etc.) |
  | a database or query layer | **sqllogictest**, the engine's own compat suite |
  | a data format (CSV, iCal, Markdown…) | that format's published conformance corpus |
  | anything shipping to users | OWASP ZAP baseline, dependency/licence scanners |
- **Stress-test KPIs before presenting them.** Each proposed KPI gets checked: observable from the
  output alone, specific (not subjective), not gameable by surface compliance, not compound (one
  thing per KPI). Show the stress-test results so it's visible why each survived.
- **Research the tech stack at scaffolding time.** When a project kickoff involves choosing the
  stack/language/framework, run the multi-model reconciled research pattern and consult the saved
  decision-tree guides (`~/Research/references/tech-stack-decision-guides.md`) before recommending;
  the published trees cover data-store/infra, not language choice — research that fresh.
- **Verify capability claims before the plan rests on them.** A plan assuming a library does X is a
  guess until context7 confirms X exists in the version you'd pin. Two checks before a dependency
  enters the plan: does it actually do the thing, and does it already do something you were about to
  hand-build. Record the library ID and version in the plan so `make/` inherits the decision instead
  of re-deriving it.

## Architecture defaults

- **L0/L1/L2 tiering for every data model Claude reads/writes.** L0 index (names, IDs, statuses),
  L1 per-domain detail files, L2 individual deep content. If working with the data means loading
  all of it every time, redesign the model.
- **Co-locate artifacts that co-evolve.** A tool and the rules it enforces (or a producer and
  consumer with a tight contract) live in the same repo so changes ship as one PR — separate repos
  guarantee the enforcer drifts behind the rules.
- **Constrain > inspect > instruct, for agent pipelines.** Prevent failure modes structurally —
  deterministic code gates between agent steps, and validated submission (the agent's only exit is
  a submit tool whose handler runs the checks; failures bounce back in-turn with feedback, capped
  retries) — before adding checker agents; a model checking a model is the weakest link. Models
  research and write; code verifies. Pair every gate with a retry-with-feedback loop so honest
  gates don't silently shrink output. Origin: 2026-08-21 copilot-agent fan-out — Carter replaced
  the Verifier agent with structural prevention.
- **The orchestrator pattern: manager-worker with bounded visibility.** Orchestrators compose
  precise self-contained briefs (goal, constraints, output format, verification criteria, all
  needed context), dispatch workers, and validate outputs against the brief — never inspecting
  intermediate reasoning. The brief is the load-bearing artifact. Bounded visibility is what makes
  long-running agents scalable.
- **Folder proximity is for humans; agents read paths and indices.** Humans see sibling files as
  related; agents only query path strings and index files. Every working folder gets an INDEX.md /
  PROJECT.md / README declaring what's inside and what's related — prefer text indices over deeper
  nesting, and when something feels "obvious" from layout, write it down or the agent misses it.
- **Design for cross-harness portability (COS work).** The COS is fundamentally a memory system;
  prefer plain-text directives any harness can read over Claude-Code-specific magic, isolate
  unavoidable Claude-only mechanics in an adapter layer, and trade elegance for portability when
  forced to choose.
- **Dual-surface parity.** Infrastructure Carter uses from both Claude Desktop and Claude Code
  (COS, skills, instruction files) must behave identically from both — reference the same
  canonical files/URLs from each surface, define conventions once, and benchmark from both.
- **Personal apps default to free-tier.** Lead with free-tier limits and whether expected usage
  stays inside them; prefer hard `$0` quota caps ("can't-charge-me") over trust-based free tiers;
  surface residual costs explicitly.
- **Dogfood in real contexts, isolated enough to iterate.** Test infrastructure inside the real
  workspace/codebase within a private primitive (private section, personal branch, scratch folder)
  — not a synthetic sandbox (misses real friction) and not shared-live (breakage radius). If no
  isolation primitive exists, question the platform, not the realism.
- **Plan-mode exit: compact, not clear.** Decline the "clear context and execute" prompt; `/compact`
  then execute, so the why behind the plan survives into execution.
