# The middleman and the mode loop — map

The proposed setup as of 2026-10-04. Design only: the parts marked **built** exist on branch
`worktree-mode-rules`; everything else is not built. Rulings and their reasons are in
`.claude/memory/decisions.md` (the 2026-10-04 entries). This file's path is a strawman.

Each line is tagged: **[ruled]** Carter decided it · **[measured]** probed on this machine ·
**[proposed]** the session's suggestion, not ruled · **[open]** undecided.

## 1. The one idea

Claude Code loads whatever sits in a named place. Global places load in every session. A mode
folder's `.claude/` loads only when a session starts in that folder **[measured]**. So the whole
system is one move, done two ways: **keep the source somewhere that does not load, and deliver
only the right pieces into `<project>/<mode>/.claude/`.**

## 2. Two products, one delivery tool

```
            SOURCES (nothing here loads on its own)                DELIVERY                 WHERE IT LOADS
 ┌──────────────────────────────────────────────────┐
 │ MIDDLEMAN FOLDER   (home: user picks at setup)   │
 │                                                  │         ┌───────────┐
 │  held plugins ───────────────────────────────────┼────────▶│           │      <project>/
 │  (other people's skills, agents, rules)          │  pieces │           │        CLAUDE.md          every session
 │                                                  │  copied │           │        .claude/           every session
 │  personal skills and agents ─────────────────────┼────────▶│ scaffold  │        research/.claude/  research sessions only
 │                                                  │         │   skill   │──▶     plan/.claude/      plan sessions only
 │  mode source files: research / plan / make ──────┼────────▶│           │        make/.claude/      make sessions only
 │  (one per mode; your own principles)             │  rules  │           │          rules/   real copies
 │                                                  │  copied │           │          skills/  copies or links
 └──────────────────────────────────────────────────┘         │           │          agents/  copies or links
                                                              │           │          settings.json
 ~/.claude/plugins/  (installed, switched off globally) ─────▶│           │            enabledPlugins
                          whole plugin switched on per folder └───────────┘
```

| | Product 1 — middleman | Product 2 — mode loop |
| --- | --- | --- |
| Serves | other people's plugins, plus personal skills | your own principles |
| Problem it answers | `enabledPlugins` is all-or-nothing per plugin **[measured]**; you want a tailored selection **[ruled]** | principles drift and feedback is lost between sessions |
| Delivery | both: switch a whole plugin on per mode folder, or copy chosen pieces **[ruled]** | copy the mode source file into every mode folder's `rules/` on each source edit **[ruled]** |
| Feedback path | none | section 3 |
| Works alone | yes — memory setting "off" **[ruled]** | no, it rides on product 1's delivery |

## 3. The loop (product 2)

```
   ┌────────────────────────────────────────────────────────────────────────────────────┐
   │                                                                                    │
   ▼                                                                                    │
 SESSION in <project>/<mode>/                                                           │
   loads: project CLAUDE.md + mode CLAUDE.md + <mode>/.claude/{rules,skills,agents}     │
   │                                                                                    │
   │  you give feedback                                                                 │
   ▼                                                                                    │
 CAPTURE — nothing of ours runs                                                         │
   built-in auto-memory writes  ~/.claude/projects/<key>/memory/feedback-*.md           │
   Claude Code appends every prompt to  ~/.claude/history.jsonl                         │
        (text, launch folder, session ID)                                               │
   │                                                                                    │
   ▼                                                                                    │
 GATE — a script, no model call                                                         │
   scope: only projects that have mode folders                                          │
   compare feedback files to the record (path → content hash → state)                   │
        unknown path  = new feedback                                                    │
        changed hash  = an existing memory was updated (an in-project repeat)           │
   look up each file's session ID in history.jsonl → launch folder → mode               │
   nothing new or changed → stop here; no agent runs                                    │
   │                                                                                    │
   ▼                                                                                    │
 DREAMER — the only step that costs model time                                          │
   sort each item:  mode principle  or  project fact  → which mode                      │
   drop redundant items: feedback already present in a source file                      │
   count recurrence: separate files across projects + dated edits within one            │
   read history.jsonl for patterns in your own messages (not the transcripts)           │
   │                                                                                    │
   ▼                                                                                    │
 PROMOTE — at 2 or 3 recurrences                                                        │
   memory setting "propose": write a proposal for you to accept                         │
   memory setting "apply":   edit the mode source file                                  │
   move the promoted feedback out of its store, with its MEMORY.md index line           │
   │                                                                                    │
   ▼                                                                                    │
 COPY OUT — on every source edit                                                        │
   overwrite <project>/<mode>/.claude/rules/<mode>.md in every stamped project ─────────┘
   (copies are generated output; a copy that differs is replaced)
```

Step by step, with status:

| Step | What happens | Status |
| --- | --- | --- |
| Session | mode folder's `.claude/` loads only from that folder; rules must be real files, not links | **[measured]** 2026-09-28, 2026-10-04 |
| Capture | built-in auto-memory, no tool of ours; `capture-feedback` retired | **[ruled]** |
| Capture | every prompt lands in `~/.claude/history.jsonl` with launch folder and session ID; 8,312 rows back to 2026-02-24 on this machine | **[measured]** 2026-10-04 |
| Gate | script before any model call | **[ruled]** |
| Gate | record of path → hash → state | **[proposed]** |
| Gate | only projects with mode folders are harvested | **[ruled]** |
| Gate | mode from session ID → `history.jsonl` launch folder: 43 of 43 IDs found (transcripts gave 6) | **[measured]** 2026-10-04 |
| Dreamer | sorts mode principle vs project fact, and by mode | **[ruled]** |
| Dreamer | removes feedback already promoted into a source file | **[ruled]** |
| Dreamer | harvests patterns from user messages, not whole transcripts | **[ruled]** |
| Dreamer | a classifier-model harness (JEV) does the sorting later | **[ruled]** as an idea; harness **[open]** |
| Promote | threshold 2 or 3 | **[ruled]** as a range; number **[open]** |
| Promote | propose vs apply is a user setting | **[ruled]** |
| Copy out | every source edit overwrites every copy | **[ruled]**; `modes.py` still reports and waits — **built, contradicted** |
| Copy out | the trigger and the list of stamped projects | **[open]**, not built |

## 4. Install and the middleman's skills

```
 claude plugin install middleman
        │   lands in ~/.claude/plugins/ like any plugin — one setup skill
        ▼
 /middleman:setup      asks: where does the middleman folder go? (container or project)
        │              asks: memory off / propose / apply
        │              creates the folder, copies the other skills into its .claude/skills/
        ▼
 open a session IN the middleman folder — the skills load there and nowhere else
        │
        ├── /middleman:compliance   find plugins installed or loading globally; bring them under
        │                           the middleman (switch off globally, or move the files)
        │
        └── /middleman:scaffold     project description → pick pieces from held plugins and
                                    personal skills → check for conflicting rules and redundant
                                    skills → write into each <mode>/.claude/ (agents do the picking)
```

- The tools are not always on; you open the middleman folder to use them — the way
  `memory-management/` is used today **[ruled]**.
- Whether the installed plugin switches itself off globally after setup **[proposed]**.

## 5. What is measured about the built-in switch

| Setting placed in | Session launched in | Plugin's skills |
| --- | --- | --- |
| `make/.claude/settings.json` | `make/` | found |
| `make/.claude/settings.json` | `plan/` or the root | absent |
| root `.claude/settings.local.json` | the root | found |
| root `.claude/settings.local.json` | `make/` | absent |

CLI 2.1.289, one headless run each, 2026-10-04. The root-level probe also added a `local`-scope
record to `~/.claude/plugins/installed_plugins.json` (removed by hand), so writing the setting is
not free of global side effects.

## 6. Where the design is thin

- **The harvest scope is small today.** Two projects have all three mode folders
  (`memory-management`, `claude-architect`). Of the 48 feedback files, 3 sit in those two stores,
  and 2 of the 43 traceable files were written from a mode folder. The loop's input grows only as
  projects get scaffolded.
- **Auto-memory keys to the project root, not the mode.** The mode is recovered by a lookup, and
  5 of 48 files carry no session ID to look up.
- **Moved plugin pieces can break.** ECC had 26 commands and about 14 skills calling their own
  install path; hooks depend on plugin scripts.
- **Not established:** whether a globally disabled plugin still auto-updates; whether hooks and
  MCP servers follow `enabledPlugins`; how long `history.jsonl` is kept (it reaches back 7 months
  here, no retention setting found); whether long prompts are stored in full.
- **A recurrence nobody saved is invisible** to the file count. Mining `history.jsonl` is the only
  step that can see it.
