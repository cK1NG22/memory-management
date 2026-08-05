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
