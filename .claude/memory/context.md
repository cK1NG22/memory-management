# Context — memory-management

**Last updated:** 2026-08-04

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

Foundations are done and the system is coherent for the first time in four generations.

- The **legacy hub is gone** — all 167 files harvested to live homes or deleted; the store is an 8K
  tombstone, backup at `~/Claude/_archive/legacy-hub_2026-08-04/`.
- The **two-system split is settled** — native memory for Carter-and-machine facts, project memory for
  the work. Forced by which one survives a folder move, not chosen by taste.
- **This project is the Gen 4 trial** — first thing built in the mode structure, so it tests the design
  while being the place the design is worked on.
- **`MEMORY.md` is 21,972 bytes (~5,500 tokens/session)**, up from 13,281. That bought visibility for
  30 working norms and the user profile that had been unreachable for months. It is now the largest
  remaining lever if it needs to be smaller.

## ⏭️ Next steps / open

Full list in `plan/ROADMAP.md`. The three that unblock the most:

1. **Fix the 7 dead skill symlinks** — silent failures, and a prerequisite for honest measurement.
2. **Build `/context-dashboard`** — real per-session token data exists in every session `.jsonl`
   (`cache_creation_input_tokens` / `cache_read_input_tokens`). This is what un-suspends the circular
   "not worth it anyway" argument.
3. **Retire `history.md` + the `auto_log_history.py` Stop hook** — decided, not yet executed.
   `close-session` still writes it and carries a pending-change note saying so.

⚠️ **Sequence is load-bearing:** fix → prune → **measure** → *then* migrate. Relocating skills before
measuring destroys the baseline the whole argument rests on.

## 🧠 Recent decisions

See `decisions.md`. The five that shape everything else:

- Folders are a **loading** mechanism, not a locking one — nothing here is a hard write boundary.
- Memory lives **once at the project root**, never per mode.
- `history.md` is **deleted**, not capped — three writers, zero readers.
- `.claude/` is **committed**; only `worktrees/` is ignored.
- The two-label `TASK.md` fix is **dropped** — the folder is the label.

## 💡 What we learned

- **Loading is not obeying.** A nearer, more specific instruction silently beats a distant general one
  even while the distant one sits fully loaded in context. Testing that text *loads* proves delivery,
  not control — a distinction easy to conflate, and one that invalidated several earlier claims.
- **Native memory does not walk up the tree.** It is keyed to the exact cwd. This is *the* mechanism
  behind every stranding: 162 files orphaned by one reorg, and 49 feedback rules that went invisible
  the day work moved from `~` to `~/Projects`.
- **The triage rule that did the work was not the routing test** — it was asking whether each file's
  *subject still existed*. Rules rot because the world moves and nothing re-validates them.
- **`personal-todo-checklist` had 72 open items and its first entry was "dissolve the legacy global
  memory hub."** The instruction to do this work was sitting inside the folder it described, in a
  store that had stopped loading. It could not surface itself.
- **An argument measured against a baseline the proposal would itself change is not an argument.**
  Caught once here; worth watching for again.

## 📂 Files touched · 🌿 git

New project at `~/Projects/memory-management/` (**not a git repo yet** — worth `git init`).
Five docs moved here from `~/Projects/docs/`, which is now empty apart from `superpowers/`.

Outside the project: `~/.claude/skills/{close-session,new-session,restructure-project,email-tracker,
github-digest,capture-feedback,brain-dump,memory-review,connect-vault}`, `~/.claude/agents/*`,
`~/.claude/state/` (new), `~/Claude/personal-backlog.md` (new), and the native store at
`~/.claude/projects/-Users-carterking-Projects/memory/`.
