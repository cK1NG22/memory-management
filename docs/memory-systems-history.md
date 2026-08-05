# Memory systems — what they were, why they failed, what replaced them

**Written 2026-08-04.** This file is the **only surviving record** of the memory systems that came
before Gen 4. Everything it describes is scheduled for deletion. If you need to know why a folder
shape existed or why it was abandoned, it is here or it is nowhere.

**Do not delete this file when cleaning up. It is the reason cleanup is safe.**

---

## L0 — the whole thing in five lines

There are **two independent memory systems**, and every generation of confusion came from treating
them as one. **Native memory** is built into Claude Code, keyed to your working directory, and lives
in `~/.claude/`. **Project memory** is a convention you built, lives inside the project, and can be
committed. Native memory follows the *path*; project memory follows the *work*. Four structures were
tried; none was fully replaced, so as of 2026-08-04 all four were running simultaneously.

---

## The two systems (this is the framing everything else depends on)

|                     | **Native auto-memory**                              | **Project memory**                     |
| ------------------- | --------------------------------------------------- | -------------------------------------- |
| Built by            | **Claude Code** — not us                            | Us (`close-session`, `new-session`)     |
| Where               | `~/.claude/projects/<encoded-abs-cwd>/memory/`       | `<project>/.claude/memory/`             |
| Addressed by        | **exact absolute cwd string**, `/` → `-`             | path relative to the project            |
| Loaded how          | `MEMORY.md` **auto, every session**; topic files **lazy**, matched on their `description:` field | **nothing auto-loads it** — a skill or human must read it |
| In a repo?          | **Never.** Lives in `$HOME`                          | Yes, if committed                       |
| Survives a folder move? | **No** — the store is stranded                   | **Yes** — it moves with the folder      |
| Shareable w/ a team | **Structurally impossible**                          | Yes                                     |

### Native memory file format (Claude Code's, not ours)

```markdown
---
name: <kebab-case-slug>
description: <one line — THIS is what recall matches on, not the body>
metadata:
  node_type: memory
  type: user | feedback | project | reference
---
<one fact. [[links]] to related memories.>
```

Four types only: `user`, `feedback`, `project`, `reference`. `MEMORY.md` is a flat index —
`- [Title](file.md) — hook` — and it loads **whole, every session**, so its byte count is a permanent
per-session tax (~3,300 tokens for `~/Projects`, ~4,600 for `~`).

### The division of labor (decided 2026-08-04)

- **Native memory** → things about **you and this machine**: preferences, feedback, cross-project
  references, the user profile. Path-keyed is *correct* for these, because they belong to the path.
- **Project memory** → things about **the work**: decisions and current state. In the repo, so it
  survives reorgs and a teammate can read it.

This split isn't a matter of taste. It's forced by which system survives a folder move.

---

## Gen 1 — global hub ❌ wrong in kind

**Shape.** Everything in one store keyed to `~`: `~/.claude/projects/-Users-carterking/memory/`.
`MEMORY.md` → `hub-<project>.md` → detail files. Filed by topic. Nothing lived in the project.

**Ours, not native.** Frontmatter was flat (`name`/`description`/`type`/`status`) with a wider type
vocabulary including `research`, which native has no concept of.

**Why it was wrong.** It had no project boundary, so nothing could be moved, shared, archived, or
deleted with its project. Unrelated work interleaved in one folder. There was no failure mode
because there was no boundary to fail at — it simply accreted.

**Measured state at time of writing:** 166 topic files, of which only **5** are native-shaped. 49
`research-*`, 49 `feedback-*`, 12 `project-*`, 12 `hub-*`. Its own `MEMORY.md` header reads
*"LEGACY HUB — being dissolved."*

**How it ended:** it didn't. Migration to Gen 2/3 reached **11 of 23 hubs** and stopped. 12 hub files
remain. `restructure-project` migrates and stamps `[migrated to project/<task>]` but **never deletes**,
so both systems kept running with no signal that the migration had stalled.

---

## Gen 2 — project-local, 5–7 files ⚠️ right instinct, wrong granularity

**Shape.** `<project>/.claude/memory/{INDEX, decisions, kpis, progress-log, todo}.md` + `handoffs/`

**Used by:** `balkanski`, `consulting`, `yt-agent-os/learning`, `knowledge-tree/coding`

**What it got right — and Gen 4 keeps.** Memory moved *into* the project. This is the single most
important correct decision in the whole lineage.

**Why it was wrong.**

1. **Too many slots with blurry edges.** Six destinations. Is a blocker a `todo` or a `progress-log`
   line? Ambiguous filing means inconsistent filing.
2. **`progress-log` was write-only.** `balkanski`'s reached **48K**. This is the same defect that
   later appeared as `history.md` — it existed here first, under a different name, and wasn't caught.
3. **Per-project, not per-effort.** A project holding two unrelated efforts (`dad/`) couldn't
   separate them.

---

## Gen 3 — container + tasks, 3 files ✅ closest to right

**Shape.** `<project>/PROJECT.md` + `<project>/<task>/TASK.md` +
`<task>/.claude/memory/{context, decisions, history}.md`

**Used by:** all three `dad/` tasks

**What it got right — and Gen 4 keeps.** Memory in the repo. Per-effort rather than per-project.
Three files with genuinely distinct roles. This generation was not wrong in kind.

**Why it was still wrong — four specific defects.**

1. **`history.md` had three writers and zero readers.** Writers: the `auto_log_history.py` **Stop
   hook** (fires every session, unattended), `close-session`, `new-session`. Verified by grepping
   every skill, hook, agent and CLAUDE.md on the machine. Result:
   `dad/company-preview/.claude/memory/history.md` = **145,027 characters** nothing ever read;
   `market-assessment` = 84,945. Git already answers "what happened, in order," with better tooling
   and no token cost.
2. **`Task Type` conflated three axes** — mode (`coding`), domain (`knowledge`), and artifact type —
   into one field. No task could honestly pick one. This is the complaint that started the redesign.
3. **Tasks are named after deliverables**, so a finished task's folder becomes archaeology. Modes
   never finish.
4. **Nothing pointed at the memory.** No `CLAUDE.md` anywhere on disk referenced `.claude/memory/`.
   Well-organized and unread.

---

## Gen 4 — container + modes, 2 files ✅ current

**Shape.** `<project>/CLAUDE.md` + `<project>/{research,plan,make}/CLAUDE.md` +
`<project>/.claude/memory/{context, decisions}.md`

```
~/Projects/<project>/
├── CLAUDE.md                  # what this is + POINTER to .claude/memory/context.md
├── .claude/
│   ├── settings.json          # committed — shared rules
│   ├── settings.local.json    # gitignored — the per-user layer (built-in, not ours)
│   ├── memory/
│   │   ├── context.md         # where we are now (overwritten each session)
│   │   └── decisions.md       # why (append-only; `dream` farms patterns from this)
│   └── skills/                # project-wide skills, committed
├── research/  { CLAUDE.md, .claude/skills/, sources }
├── plan/      { CLAUDE.md, .claude/skills/, README.md, CHARTER.md, phases/ }
└── make/      { CLAUDE.md, .claude/skills/, the code }
```

### Every choice traces to a measured finding

| Gen 4 choice | Fixes |
| --- | --- |
| Memory at **project root**, not per mode | native stores already fragment per cwd — adding mode folders would triple the fragmentation and each new store starts empty |
| **Two** memory files, not three | `history.md` had no readers |
| `CLAUDE.md` **points at** `context.md` | project memory has no automatic reader; the pointer *is* the loading mechanism |
| **No `Task Type` field** | the folder is the mode; a field is a second source of truth that drifts |
| Modes = **skill scoping + role instructions**, never permissions | nothing available is a hard write boundary (see below) |
| Mode `CLAUDE.md` names **where to write instead**, not just a prohibition | nearest instruction wins — used deliberately |
| `.claude/` **committed**, only `worktrees/` ignored | gitignored `.claude/` meant worktrees arrived with no settings, and teammates couldn't see project skills |
| `decisions.md` append-only, farmed by `dream` | gives the surviving file a second reader; promotion bar is ≥3 occurrences across ≥2 projects before anything becomes a skill |

### What Gen 4 fixes that no earlier generation addressed

Gen 1–3 each tried to make **one** structure carry both *what the work is about* and *what kind of
work it is*. Gen 1 filed by topic and lost the project. Gen 2 filed by project and lost the activity.
Gen 3 filed by task — a deliverable — so it captured both briefly, then expired.

Gen 4 puts them on separate axes: **project = folder, mode = subfolder**, and memory attaches to the
project because that's the axis that persists.

---

## ✅ The Gen 1 hub is gone — completed 2026-08-04

All **167 files** harvested. The store now holds only a tombstone. Where they went:

| Destination | Files |
| --- | --- |
| Active native store (`-Users-carterking-Projects`) | 30 working norms + the user profile + live operational references and cron specs |
| `~/Research/<topic>/` | 25 research docs + `RESEARCH-INDEX.md`; new `memory-systems/` folder created |
| `~/Archive/Sandbox/privacyguard-research/` | 12 (~370KB) — archived venture, sits with the pitch deck |
| `~/Projects/knowledge-tree/` | 13 research + taxonomy files |
| `~/Sandbox/builds/locker/docs/` | 11 specs and competitive analyses |
| `~/School/`, `~/Optimal/`, `~/Clients/mana-ventures/`, `~/Vault/` | 16 coursework and client files |
| `~/Claude/personal-backlog.md` | the master TODO checklist — **72 items still open** |
| deleted | 8 verified-migrated hubs, all Notion material, duplicates, 5 obsolete rules, 1 dangling symlink |

**Backup of the store as it stood: `~/Claude/_archive/legacy-hub_2026-08-04/` (all 167).**

### What the harvest itself revealed

- **`personal-todo-checklist` had 72 open items**, and the first one was *"dissolve the legacy global
  memory hub."* The task was sitting inside the thing it described, unread since March.
- **The small research files were pointers; the large ones were content.** Anything under ~2.5KB
  summarized research that already lived in `~/Research`. Anything over ~20KB *was* the research,
  filed in a memory folder by mistake — 299KB of it for a venture that had already been archived.
- **The triage rule that did the work was not the routing test.** It was checking whether each file's
  *subject still existed.* Four of five deleted rules were correct when written; they rotted because
  the world moved and nothing re-validated them. `hub-pattern-scales` was still instructing that every
  project get a `hub-<slug>.md` in this very folder.

---

## Measured state on 2026-08-04, before cleanup

Recorded so that after deletion there is still a record of what was deleted.

**471 memory `.md` files across 41 native stores. 229 native-format, 242 not. 33 stores populated.**

### Stranded by the 2026-06-30 folder reorg — 162 files, mostly current-format

The reorg moved folders without moving their memory. Native memory is keyed to the absolute path, so
each moved folder's store was orphaned in place. Nothing warned.

| Stranded store | Files | Native-format |
| --- | --- | --- |
| `~/Projects/Personal` | 38 | 36 |
| `~/Projects/Clients/mana-ventures` | 29 | 28 |
| `~/Desktop/AI-Projects-Locker` | 18 | 0 |
| `~/Projects/skill-factory` | 16 | 0 |
| `~/Projects/Optimal` | 14 | 13 |
| `~/Sandbox/agentic-education` | 14 | 10 |
| `~/Projects/Clients/mana-ventures/attio-network-database` | 10 | 9 |
| `~/Projects/Sandbox/future-of-work-velocity` | 9 | 7 |
| `~/Projects/Clients/outreach` | 8 | 7 |
| `~/Projects/Optimal/mana-ventures` | 6 | 2 |

**`mana-ventures` is the clearest case: 29 files of history at a dead address, 7 at the live one.**
The project didn't lose its memory — it started a second one from zero and nobody noticed.

### Oversized write-only logs

| File | Size |
| --- | --- |
| `dad/company-preview/.claude/memory/history.md` | 145,027 chars |
| `dad/market-assessment/.claude/memory/history.md` | 84,945 chars |
| `balkanski/.claude/memory/progress-log.md` | 48,521 chars |

---

## The lesson that generalizes

**Every generation failed at migration, not at design.**

- Gen 1 → 2/3 stalled at 11 of 23 hubs and left both systems live.
- The June reorg moved folders and left their memory behind.
- `restructure-project` "never deletes" as a safety property — which *guarantees* the old system
  survives every migration.

Four structures coexisted on 2026-08-04 because each migration was safe, partial, and unfinished,
and none emitted a signal when it stopped.

> **A migration that doesn't delete isn't a migration, it's an addition.**

This file exists so that deletion is safe. Finish the migration.

---

## Related facts worth not re-deriving

- **Nothing here is a hard write boundary.** `Edit()` deny rules are bypassed by `python -c` / `node -e`
  (both globally allowlisted), and hooks bypass the permission layer entirely because they are
  subprocesses, not tool calls. `Write()` deny rules are silently ignored — only `Edit()` is checked.
  Mode separation is a **convention with a tripwire**, never enforcement.
- **Loading ≠ obeying.** A nearer, more specific instruction silently overrides a distant general one
  even while the distant one sits fully loaded in context. Verified by controlled A/B.
- **Skills are directory-scoped.** `.claude/skills/` loads at that folder and below. Global
  `~/.claude/skills/` loads *everywhere, always* — folders can add skills, never subtract. Relocating
  skills out of global is the only way to cut their ~11,000-token per-session cost.
- **A skill symlinked from a project folder dies silently if that folder moves.** Seven did in the
  June reorg.

**Full detail:** `mode-review-verdict.md` · `mode-structure-spec.md` · `mode-review-round1.md` ·
`skill-relocation-plan.md` (all in this folder) · memory
`reference-claude-code-loading-mechanics`

---

## ✅ The orphaned stores are gone — completed 2026-08-04

The second and final cleanup. **16 stores keyed to directories that no longer existed, holding 165
topic files.** Where they went:

| Destination | Files |
| --- | --- |
| `~/Projects` (native, machine-wide facts) | 36 — working norms, the tool references, two user-profile facts |
| `~/Clients/mana-ventures` (+ `attio-network-database`) | 43 — four dead stores merged into the two live ones |
| `~/Optimal` (+ `mana-drive-reorg`, `optimal-claude-skills/skill-factory`) | 28 |
| `~/Sandbox/builds/velocity` | 22 — **three** dead velocity stores consolidated into one |
| `~/Clients/outreach` | 7 |
| `~/Sandbox`, `~/Sandbox/builds`, `~/Clients/northstar-preschools` | 3 |
| `~/Archive/Locker-UI/plans/` — **out of the memory system** | 17 |
| deleted | 9 |

**Backup of all 16 stores as they stood: `~/Claude/_archive/orphan-stores_2026-08-04/` (181 files).**

### Verified after

**22 live stores · 308 topic files · 0 dangling links · 6 files unindexed by design.** Every store
now resolves to a directory that exists. Every `MEMORY.md` was rebuilt or extended so nothing landed
unlisted.

### How they were routed

**By where Carter actually starts sessions, preserving folder depth.** A store existed at
`~/Projects/Optimal/mana-drive-reorg` because he worked from that folder; its successor
`~/Optimal/mana-drive-reorg` exists, so the memory went there rather than being flattened up to
`~/Optimal` — where it would be invisible from the folder it describes.

The one deliberate exception is **velocity**, whose memory was split across three dead stores. Keeping
that split would have preserved the fragmentation that caused the loss, so it was consolidated.

### What this cleanup revealed

- **Some "memories" were never memories.** Locker's 18 files had no frontmatter and no descriptions —
  they are phased build plans (`plan-2.1` … `plan-5-billing`) and a vision doc, written into a memory
  store because it was the nearest writable place. They were moved to `~/Archive/Locker-UI/plans/`,
  not deleted: a killed product's plans are still a record, and outside the memory system they cost
  nothing. **A memory store with no frontmatter in it is a sign the tool was used as a folder.**
- **Only 9 of 165 files failed the "does the subject still exist?" test.** The orphaned stores were
  not full of rot — they were full of live work that had simply gone dark. This is the opposite of the
  legacy hub, where the same rule deleted a great deal.
- **Two stores pointed at empty shells, not missing folders.** `~/Projects/Sandbox` and
  `~/Projects/Sandbox/velocity` still exist on disk but contain only stale worktrees, so a naive
  existence check called them healthy. **Resolving a path is not the same as verifying the project is
  there** — a lesson `/move-project --check` has to encode.
- **One duplicate surfaced.** `feedback-subskill-vs-reference.md` existed in two stores with different
  contents. Nothing detects this; a fork of the same rule can drift indefinitely.
