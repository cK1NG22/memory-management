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
