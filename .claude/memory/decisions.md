# Decisions

Append-only. Each entry: what was decided, and **why**. Git records what changed; only this records
what was rejected and the reasoning that survived.

---

## 2026-08-04 — Founding session (the whole redesign happened in one sitting)

### Structure

- **Modes replace task-types.** `research/` → `plan/` → `make/`, one `CLAUDE.md` each. *Why:* the old
  `Task Type` field conflated three axes — mode, domain, artifact type — and no task could honestly
  pick one.
- **Folders are a loading mechanism, not a locking one.** *Why:* a 4-seat Fable review plus direct
  testing established that nothing available is a hard write boundary — `Edit()` deny rules are
  bypassed by `python -c`/`node -e` (both globally allowlisted), hooks bypass the permission layer
  entirely as subprocesses, and gitignored `.claude/` produces worktrees with no settings at all.
- **Blocking rules stay anyway, as convention with a tripwire.** *Carter's call.* The deny rule
  catches the accident; a mode-level instruction naming **where to write instead** covers intent.
  "Nearest instruction wins" is an asset when the rule lives in the mode folder. Residual risk is the
  channels that never read instructions, not disobedience.
- **Memory lives once at the project root, not per mode.** *Why:* native memory already fragments per
  cwd; three mode folders would mean three empty stores per project — deliberately re-running the
  June accident three times over.
- **Two-field `Mode:` × `Domain:` TASK.md — DROPPED.** *Carter's pushback:* if the session starts in
  the right folder, the folder *is* the label; a field is a second source of truth that drifts.
- **`.claude/` gets committed**, ignoring only `.claude/worktrees/`. *Why:* gitignoring it meant
  worktrees arrived with no settings and teammates could not see project skills. `settings.local.json`
  is already the built-in per-user layer. `CODEOWNERS` is the real answer for team protection — not
  needed while solo.

### Memory

- **Two independent systems, and the split is forced, not chosen.** Native memory (Claude Code's,
  cwd-keyed, in `~/.claude/`) holds facts about *Carter and this machine*. Project memory (ours, in
  the repo) holds facts about *the work*. *Why:* only one of them survives a folder move.
- **`history.md` is retired, along with the `auto_log_history.py` Stop hook.** *Why:* it had **three
  writers and zero readers** — verified by grepping every skill, hook, agent and CLAUDE.md on the
  machine. One file had reached 145,027 characters. Git already answers "what happened, in order."
  This *replaces* the earlier "cap and rotate" recommendation.
- **`decisions.md` survives because it answers a question git cannot:** what was rejected, and why.
- **`dream` will farm patterns from `decisions.md` into skills.** *Carter's idea.* Promotion bar:
  a pattern must appear in **≥3 decisions across ≥2 projects** before it becomes a skill, and `dream`
  proposes rather than creates. *Why the bar:* without one, every decision becomes a skill and we are
  back at a 130-skill global catalog.
- **`dream` orphan cleanup proposes fold-or-delete, never deletes silently.**

### Rejected / suspended

- **Hard write boundary — shelved.** OS `chmod`/ACL and `tools:` frontmatter withholding are the two
  untested candidates; neither is silent-proof. Revisit only after a real bleed-through.
- **Narrowing global permissions — declined.** Standing consequence: a wrong or bypassed rule degrades
  to *silently allowed*, never to *ask me first*. That is the price of avoiding the friction.
- **Re-running the agent team — declined.** What is needed is one *measurement* (after skill pruning)
  and one *trial* (built clean, not migrated onto an existing mess), not four more reviewers
  reproducing the same experiments.
- **"Not worth it anyway" — SUSPENDED as circular.** That argument measured the saving against a
  session baseline that *includes* the ~11K-token global skill catalog the fix would cut. Must be
  re-measured *after* skills are relocated.

### Execution

- **Legacy hub fully dissolved.** All 167 files harvested to live homes or deleted; store reduced to a
  tombstone. Backup at `~/Claude/_archive/legacy-hub_2026-08-04/`.
- **Operational logs are not memory.** `email-tracker-log.md` (97KB) and `github-digest-log.md` (83KB)
  moved to `~/.claude/state/`. They are dedup state that had been filed in a memory folder.
- **A live checklist is a document, not a memory.** `personal-todo-checklist` (72 open items) moved to
  `~/Claude/personal-backlog.md`. *Why:* memory is for recall; a checklist is for editing — filing one
  as the other is how a task hides for five months.
- **Notion material deleted.** Carter is off Notion and removed the global `CLAUDE.md` pointer himself.

---

## 2026-08-04 — Orphan resolution (session 2)

The last cleanup item. 16 native-memory stores were keyed to directories that no longer existed,
holding 166 topic files that had been invisible since the 2026-06-30 reorg.

### How orphans were routed

- **Route by where Carter actually starts sessions, preserving folder depth.** *Why:* a store existed
  at `~/Projects/Optimal/mana-drive-reorg` because he worked from that folder. Its successor
  `~/Optimal/mana-drive-reorg` exists, so the memory goes there — not flattened up to `~/Optimal`,
  where it would be invisible from the folder it describes. Fixing the path is the whole repair;
  changing the depth would be a second, unrequested migration.
- **Rejected: fold everything into `~/Projects`.** Simpler, and wrong — it would make every client
  and Sandbox fact load on every session in the main working directory, which is the cost the whole
  project exists to control.
- **All velocity memory consolidated into one store** at `~/Sandbox/builds/velocity`. *Why:* it was
  spread across three dead stores (`Sandbox`, `Sandbox/velocity`, `Sandbox/future-of-work-velocity`).
  Preserving that split would preserve the fragmentation that caused the loss.
- **The triage question was "does this file's subject still exist?"** — not the routing test. Only 9
  of 166 failed it.

### What was deleted (9 files)

Four superseded memory-system records (the hub review, the migration notice, the dead 4-bucket folder
map, the Locker go/no-go for an archived product), three executed-or-abandoned skill-factory stage
plans plus a Gen 2 handoff whose "next action" was long since done, one duplicate feedback file whose
newer copy already lived in `~/Projects`, and the `principle.ai` tutor project — the only orphan whose
folder is gone from disk entirely.

### What left the memory system

- **Locker's 17 files were never memories.** No frontmatter, no descriptions — they are phased build
  plans (`plan-2.1` … `plan-5-billing`) plus a vision doc, written into the memory store because it
  was the nearest writable place. Moved to `~/Archive/Locker-UI/plans/` with a README explaining the
  provenance. *Why not delete:* the product was killed, but a killed product's plans are a record,
  and they cost nothing outside the memory system.

### Verified

22 live stores · 308 topic files · **0 dangling links** · 6 files unindexed by design. Every remaining
store resolves to a directory that exists. Backup at `~/Claude/_archive/orphan-stores_2026-08-04/`
(181 files, taken before anything moved).

### Roadmap additions (Carter's ask)

- **Mode `CLAUDE.md` templates**, used by the new-project skill at scaffold time. The open question is
  the *update model* — a copied template drifts and can never be fixed centrally; a symlinked one
  stays live but edits every project at once.
- **Auto-symlink each mode's skills** into `<project>/<mode>/.claude/skills/`. This is the mechanism
  the mode structure was actually approved for; without it modes carry instructions but no tooling.
  Depends on relocating skills out of global first, and needs a resolve-check — 7 symlinks died
  silently in the June reorg.

---

## 2026-08-05 — Writing the repair down

- **The check matters more than the repair, so it got built as a tool rather than a doc section.**
  `make/memory-repair/audit.py` takes no arguments and returns a non-zero exit code when anything is
  wrong. *Why:* a repair fixes one incident; a check that runs before and after every folder move is
  what stops the next three years of silent drift. The exit code is deliberate — it lets this drop
  into a cron later without being rewritten.
- **`audit.py` resolves store names by walking the filesystem, not by decoding the string.** *Why:*
  the `/`→`-` encoding is lossy — `mana-ventures` (one folder) and `mana/ventures` (two) produce the
  identical name. A naive decode reports a false orphan for every folder containing a hyphen, which is
  most of them. Walking every possible split against real directories is the only correct method.
- **`route.py` requires an explicit manifest naming every file, and reports `LEFT n`.** *Why:* a glob
  would move files nobody read, which defeats the triage step entirely. The run is not finished until
  every store reports `LEFT 0` — the tool refuses to let a file be silently skipped.
- **Half of `/move-project --check` now exists.** The memory half is done and verified. What the skill
  still has to add is performing the move, plus symlinks and the ~23 config references.
- **The four one-off scripts were generalized rather than archived.** *Why:* they lived in the job's
  temp directory, which is deleted with the job. Proven, working tools were about to evaporate.

---

## 2026-08-05 — history.md retirement executed

- **The hook count was wrong: four writers, not three.** The grep that found "three writers, zero
  readers" missed `memory_migrate.py` inside `close-session` itself — it scaffolded a fresh
  `history.md` on every migration and seeded it from `progress-log.md`. *Lesson:* counting who writes
  a file must include who **creates** it, not just who appends.
- **All four writers retired in one pass, as decided:** Stop hook unwired from settings.json and
  archived (with its test) to `~/.claude/hooks/_archive/` per the file-versioning convention;
  `close-session` Phase 5 step removed; `new-session` Phase 4 tombstoned; `memory_migrate.py` now
  scaffolds the 2-file shape (`context.md` + `decisions.md`) — verified by smoke test.
- **Existing `history.md` files are left in place, inert.** Deleting them across all projects is a
  separate sweep with no urgency — nothing reads them, and nothing writes them anymore. The two pure
  autolog debris files here and in `claude-architect` were removed.
- **Hooks load at session start**, so the removal takes effect for the *next* session; the current
  one no longer has the script to run anyway.

---

## 2026-08-05 — Dead symlinks fixed, skill relocation tranche 1

- **Fix the symlinks before measuring, not after.** *Why:* a dead symlink is a skill that silently
  doesn't load, so the pre-fix state under-reports the true catalog. Measuring after the fix and
  before the relocation is the only order that gives an honest baseline. (The recorded count of 7
  was also wrong — 12 were dead by execution time; counts drift, scans don't.)
- **`qa-design-review` deleted rather than re-pointed.** *Why:* its target no longer exists
  anywhere on disk — the gstack repo removed the skill upstream. A link with no possible target is
  noise, and it's one `ln -s` to recreate if the skill ever returns.
- **Relocated skills land in `<folder>/.claude/skills/` as symlinks to their canonical homes.**
  *Why:* the loading rule (verified 2026-08-04) is that a folder's `.claude/skills/` loads only at
  or below that folder — identical behavior inside the project, zero cost outside it. Nothing was
  physically moved, so rollback is one `ln -s` per skill.
- **The gstack family stays put: 53 of 113 skills, but only ~1,100 tokens.** *Why:* they're
  installer-owned — `./setup` would regenerate anything hand-moved, making the "fix" a permanent
  fight. The token weight is in the other 60 skills anyway.
- **Physical moves are proposed, not executed.** *Why:* Carter owns folder structure; the remaining
  candidates are real directories, and moving them decides where things live. The proposals (with
  destinations and token values) are in `plan/skill-relocation-plan.md`.
- **No fresh headless session for the re-measure.** *Why:* `claude -p` bills the separate
  programmatic credit pool; the next normal session start measures the same thing for free.

---

## 2026-08-05 — The mode-skill shape (Carter's call)

- **Mode skills reach a project through two symlink hops:** each skill lives once in its canonical
  home, is linked into a central mode home (`~/.claude/modes/<mode>/skills/`), and each project's
  `<mode>/.claude/skills` is **one folder-level symlink** to that mode home — not one link per
  skill. *Why:* adding a skill to a mode then reaches every project instantly, with no
  rescaffolding; per-skill links would need a re-scaffold on every addition. The path must be
  exactly `<folder>/.claude/skills/` — the loader scans nothing else.
- **Open verification attached to this decision:** per-skill symlinks are proven to load; a
  symlinked *parent* `skills/` folder is not. Sentinel-test it before the mode templates are
  written — this project's rule is never to build on an untested loading assumption.
- **Double-loading is prevented by invariant + scan, not care.** Each skill loads from exactly one
  place (global / a project / a mode home). The check belongs in `audit.py` and
  `/move-project --check`: flag any skill name reachable from two locations. *Why:* "rescaffold
  everything correctly" is vigilance, and vigilance drifts — the 7-vs-12 symlink count proved it
  again this session.
- **The full per-skill destination map is generated from disk, complete, and lives in
  `plan/skill-relocation-plan.md`** — every one of the 113 skills appears exactly once.

---

## 2026-08-05 — Tranche 2 rulings (Carter) + the automations direction

- **Tranche 2 executed as approved:** curriculum quizzes into `~/Projects/ai-engineering/`,
  `daily-standup`/`source-leads`/`notion-transcript` into `optimal-claude-skills` (linked from
  `~/Optimal/.claude/skills/`), `connect-vault` into `~/Research/.claude/skills/`. Global is 96
  skills, down from 113 at the day's start.
- **`notion-transcript` kept, not retired** — Carter routed it to Optimal instead. *Lesson:* the
  retire recommendation inferred too much from "Carter left Notion"; the skill's users aren't
  only Carter's own workspace.
- **`resolve-vulns` parked in global** — Carter doesn't know what he wants for it yet. Recorded
  as undecided rather than forced into a category; a future automations project is a candidate.
- **The automations-project idea is endorsed because of `WorkingDirectory`, not tidiness:**
  pinning each plist's working directory to the project dissolves the whole cron-locked global
  category. One plist (supply-chain-scan) already proves the key works. Dream is the exception —
  its rules are memory policy, so it colocates with memory-management.
- **Shifts direction noted, deliberately unresolved:** execution in the relevant project's
  `make/` (possibly `make/shift-work/`), foreman stays cross-project. Design when the mode
  rollout reaches those projects.

---

## 2026-08-06 — Mode memory: resolved by the platform, not by us

Sentinel experiments (isolated throwaway trees, Claude Code 2.1.223 — full record in
`research/sources/native-memory-keying-and-symlink-experiments.md`):

- **No mode-memory layer gets built.** *Why:* native memory turned out to be keyed to the **git
  root**, not the exact cwd — a session in `research/` reads *and* writes the repo-root store, so
  the three modes already share one store. The planned symlink layer would duplicate a platform
  behavior while adding a proven fork surface. The 2026-08-04 finding "does not walk up" was
  **overgeneralized from non-git test dirs** — it still holds outside repos. *Lesson:* platform
  findings carry a version stamp; re-test the load-bearing ones before building on them.
- **The one shared-memory mechanism adopted: shared topic files.** One canonical copy where the
  fact was born; any other store that needs it gets a file symlink **plus its own `MEMORY.md`
  index line** (mandatory — description-match recall through symlinks is untested; the index-read
  path is proven). Routing-rule extension: *a native memory lives in exactly one store; copying is
  forking.*
- **Rejected: sharing `MEMORY.md` across stores** — works mechanically (tested), but the index is
  a store's recall surface, and coupling indexes makes every save in one store load in the other.
- **Rejected: store-dir symlinks as design** (kept as repair tool only, for non-repo trees that
  can't `git init`). *Why:* E5 showed their failure mode is worse than the skill deaths — a
  dangling `memory/` link reads as silently *empty* memory, and the **next write recreates the
  stale target, so the link resolves again**: a self-camouflaging fork that resolve-checks pass.
- **`audit.py` grows four checks before any symlink is created** (spec in
  `plan/mode-memory-design.md`): stranded repo-subdir stores (a *new* stranding class — invisible
  memories with the folder still on disk; measured 0-of-24 today, the check keeps it zero),
  lstat-level symlink resolution inside stores (two verified blind spots today: a store whose dir
  link dangles vanishes from the report; a dangling topic link globs as healthy), a containment
  invariant (memory links may only target inside `~/.claude/projects/*/memory/`), and a warn-only
  duplicate-topic-name fork tripwire.
- **Migration deliberately not executed** — this session was research + design only. First
  candidate when approved: the loading-mechanics reference, whose canonical copy lives in the
  `~/Projects` store and is therefore invisible to every session inside this repo.

---

## 2026-08-05 — Wrap-up: pushes, nested repo, next session staged

- **`skill-factory` is a repo nested inside `optimal-claude-skills` — resolved by gitignoring it,
  never by committing it.** *Why:* it has its own remote (private `ck22coding/skill-factory`) and
  its own history; committing a repo inside a repo produces neither. Its uncommitted changes are
  its own open item.
- **The `optimal-skills` GitHub remote pointed at a repo that didn't exist** — the push had been
  failing silently forever (nothing ever pushed). Created it **private** and pushed. *Why private:*
  nothing goes public without Carter's explicit say; flipping visibility later is one click.
- **The symlinked-memory exploration got a designed prompt, not a cold start.** *Why:* the new
  session inherits nothing; the prompt encodes the entry points, the test-first rule, and the
  experiments ranked by value (store-level symlink first — it would collapse per-mode store
  fragmentation). This is ROADMAP Phase 2's "mode memory" item beginning.
