# Plan — TO-DO system

**Approved 2026-08-18.** Proposal: standardized per-project TO-DOs, in-session task-list bridge,
cross-project query, feedback loop. Routing verdict: TO-DOs are present-tense work-state → project
side, project root — never native memory, never `.claude/memory/` (past-tense, immutable).

## The standard (load-bearing spec — build inherits this verbatim)

- **Location:** `TODO.md` at each project root. Committed (visible in bg-job worktrees, merges via git).
- **Format:** flat checkboxes, no sections, no priority syntax in v1.

  ```
  # TODO — <project>

  - [ ] <task> — added 2026-08-18
  - [x] <task> — done 2026-08-18
  ```

- **Prune freely:** delete `[x]` lines whenever the file gets long — git is the record (same
  reasoning as the no-`history.md` rule).
- **Sweep (the cross-project query):**

  ```bash
  find ~/Projects -maxdepth 3 -name TODO.md \
    -not -path '*/node_modules/*' -not -path '*/_archive/*' -not -path '*/Archive/*'
  ```

  Depth 3 covers nested container-repos (`~/Projects/products/<project>/TODO.md` — products is the
  first container that is itself a git repo). Membership is self-selecting: no `TODO.md`, not in
  the sweep. No registry, no aggregate index file — the glob is the index.

## Phase 1 — The standard exists

- [ ] **1.1: Seed `TODO.md` in this repo.**
  Move the two open items from `.claude/memory/context.md` "Next steps / open" (§4 stop-gate
  ruling; A/B replacement decision) into a root `TODO.md`. Context.md's Next section shrinks to a
  pointer at the file. This repo proves the format.
  `blocked-by: none`

- [ ] **1.2: One line in `~/.claude/modes/ALWAYS.md`** (under "State, secrets, and files"):
  > **Project TO-DOs live in `TODO.md` at each project root** — flat checkboxes, committed; flip
  > `[ ]`→`[x]` with a `done <date>` note when finished; prune done lines freely (git is the
  > record). Seed the session task list / query across projects with the **`/todos`** slash
  > command (human-invoked; the model must not act on TO-DO questions without it beyond reading
  > the current project's file).

  This is the auto-loaded layer — every session knows the convention without invoking anything.
  `blocked-by: none`

## Phase 2 — The skill

- [ ] **2.1: Create `~/.claude/skills/todos/SKILL.md`.** Two behaviors:
  - **No args, inside a project:** read root `TODO.md`, agree with Carter which items this session
    tackles, seed the built-in session task list from them, and write back to `TODO.md` the moment
    each completes (flip `[x]` + date; add items discovered mid-session). The durable file is
    source and sink; the session list is the working view.
  - **`all`:** run the sweep, report open items grouped by project (oldest first, counts), suggest
    what to work on next. `~/Projects` only in v1; `~/Foundry` is a later one-line addition.

  Constraints (Carter's call 2026-08-18): **human-invoked slash command only.** Frontmatter:
  `disable-model-invocation: true`, **no description**, `argument-hint: "[all]"`. Zero chars
  against the skill-listing budget; the model never auto-triggers it. Discovery therefore rides
  entirely on the ALWAYS.md line (1.2), which must name `/todos` explicitly.
  `blocked-by: 1.2`

## Phase 3 — Repoint the readers (all under `~/.claude` — global state, one owner, sequential)

- [ ] **3.1: `close-session` Phase 4:** add a `TODO.md` step beside the roadmap sweep — flip items
  completed this session, add unplanned work that got done or discovered, prune stale `[x]` lines.
  Same review/auto rules as the roadmap step.
  `blocked-by: 1.1`

- [ ] **3.2: `weekly-digest.md`:** repoint step 5 ("Open TODOs") from grepping memory files to the
  sweep; flag items with an `added` date >2 weeks old as stale. Also fix step 4's stale
  pre-keying path (`-Users-carterking-Projects` no longer exists as the single store).
  `blocked-by: 1.1`

- [ ] **3.3: `new-project` scaffold:** add a step creating `TODO.md` next to the scaffolded
  `ROADMAP.md` (header + one bracketed placeholder line, per the skill's leave-placeholders rule).
  New projects join the sweep from day one. Roadmap keeps phased build tasks; TODO.md keeps loose
  next actions.
  `blocked-by: none`

- Memory Janitor: **no edit.** Its "unchecked `- [ ]` in memory files" staleness check now doubles
  as a misrouting detector — TO-DOs found in memory are on the wrong side of the wall by
  definition.

## Phase 4 — Verify + record

- [ ] **4.1: Run `/todos all`** — must find this repo's `TODO.md`; spot-check that a `products/`
  nested project would be caught at depth 3.
  `blocked-by: 2.1, 1.1`

- [ ] **4.2: Dry-run `close-session` Phase 4** against a scratch `[ ]` item — flips with date.
  `blocked-by: 3.1`

- [ ] **4.3: Native memory note** in this project's store: `feedback-todo-convention.md`
  (type: feedback) recording the adopted convention + one MEMORY.md index line.
  `blocked-by: 4.1`

## Test plan

Conformance suites: **none apply** — deliverables are markdown conventions and skill instructions;
no web UI, API, or engine covered by a published standard. Checks 4.1–4.2 are the whole test plan, plus one frontmatter check: the skill listing must show
`todos` adding **0 chars** (`disable-model-invocation: true`, no description).

## Execution notes

- Phases 2–3 edit **global files under `~/.claude`** — worktrees isolate none of it. One session
  applies them, sequentially. No subagents; the build is ~1 new file + 4 small edits + 1 seed.
- Repo-side work (1.1, and this plan) rides worktree branches; **no remote** — local commits only.
