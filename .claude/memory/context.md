# Context — memory-management

**Last updated:** 2026-08-04

## 🎯 Goal

A memory and context system where **nothing fails silently** and **nothing is stranded by moving a
folder.** Optimizing for context curation, explicitly not for traditional coding conventions.

## 🧭 Where we are now

**Every stranded memory file on this machine has been resolved.** That was the last of the cleanup;
everything remaining on the roadmap is net-new building.

- The **legacy hub is gone** — 167 files harvested, store reduced to a tombstone.
- The **16 orphaned stores are gone** — of 165 topic files, 139 were routed to live stores, 17 moved
  out of the memory system entirely, 9 deleted. Backup at
  `~/Claude/_archive/orphan-stores_2026-08-04/`.
- **22 live stores, 308 topic files, 0 dangling links, 6 files unindexed by design.** Every store that
  exists now corresponds to a directory that exists.
- The **two-system split is settled** — native memory for Carter-and-machine facts, project memory for
  the work. Forced by which one survives a folder move, not chosen by taste.
- **This project is the Gen 4 trial** — first thing built in the mode structure, so it tests the design
  while being the place the design is worked on.
- **`MEMORY.md` at `~/Projects` is 14,694 bytes** (was 10,483 before the orphan harvest added 36
  memories on 24 merged lines). Still the largest single per-session cost, and still the main lever.

## ⏭️ Next steps / open

Full list in `plan/ROADMAP.md`. The three that unblock the most:

1. **Fix the 7 dead skill symlinks** — silent failures, and a prerequisite for honest measurement.
2. **Build `/context-dashboard`** — real per-session token data exists in every session `.jsonl`
   (`cache_creation_input_tokens` / `cache_read_input_tokens`). This is what un-suspends the circular
   "not worth it anyway" argument. Read `[[project-orchestrator-agent-deferred]]` first — it was
   recovered from an orphaned store and contains three prior designs for exactly this.
3. **Retire `history.md` + the `auto_log_history.py` Stop hook** — decided, not yet executed.
   `close-session` still writes it and carries a pending-change note saying so.

⚠️ **Sequence is load-bearing:** fix → prune → **measure** → *then* migrate. Relocating skills before
measuring destroys the baseline the whole argument rests on.

## 🧠 Recent decisions

See `decisions.md`. The ones that shape everything else:

- Folders are a **loading** mechanism, not a locking one — nothing here is a hard write boundary.
- Memory lives **once at the project root**, never per mode.
- `history.md` is **deleted**, not capped — three writers, zero readers.
- `.claude/` is **committed**; only `worktrees/` is ignored.
- Orphaned memory is routed by **where Carter actually starts sessions**, preserving folder depth —
  not flattened to one store and not left at the dead path.
- **All velocity memory consolidated into one store**, because it was spread across three.

## 💡 What we learned

- **Loading is not obeying.** A nearer, more specific instruction silently beats a distant general one
  even while the distant one sits fully loaded in context. Testing that text *loads* proves delivery,
  not control — a distinction easy to conflate, and one that invalidated several earlier claims.
- **Native memory does not walk up the tree.** It is keyed to the exact cwd. This is *the* mechanism
  behind every stranding: 165 files orphaned by one reorg, and 49 feedback rules that went invisible
  the day work moved from `~` to `~/Projects`.
- **The triage rule that did the work was not the routing test** — it was asking whether each file's
  *subject still existed*. Rules rot because the world moves and nothing re-validates them.
- **A project that moves doesn't lose its memory — it silently starts a second one from zero.**
  `mana-ventures` had 29 files at a dead path and 7 at the live one, and nothing ever said so. This is
  the single clearest argument for `/move-project`.
- **Some "memories" were never memories.** 17 of Locker's 18 files were phased build plans with no
  frontmatter, written into the memory system because it was the nearest writable place. They now live
  in `~/Archive/Locker-UI/plans/`.
- **An argument measured against a baseline the proposal would itself change is not an argument.**

## 📂 Files touched · 🌿 git

Project at `~/Projects/memory-management/`, committed. Orphan work touched
`~/.claude/projects/*/memory/` (16 stores removed, 11 stores written), plus
`~/Archive/Locker-UI/plans/` (new) and `~/Claude/_archive/orphan-stores_2026-08-04/` (backup).
