# The middleman folder — process map

How a plugin gets from "installed" to "loads in exactly the folders that need it", as of
2026-10-04. Design only; nothing here is built. The wider picture, including the feedback loop, is
`mode-loop-map.md` beside this file. Rulings: `.claude/memory/decisions.md`, the 2026-10-04
entries. This file's path is a strawman.

Tags: **[ruled]** Carter decided it · **[measured]** probed on this machine · **[proposed]** the
session's suggestion · **[open]** undecided or unmeasured.

## 1. The process

```
 INSTALL                claude plugin install middleman
    │                   lands in ~/.claude/plugins/ with one setup skill
    ▼
 SETUP                  /middleman:setup
    │                   asks where the middleman folder goes (container or project)
    │                   asks the memory setting: off / propose / apply
    │                   creates the folder; copies the other skills into its .claude/skills/
    ▼
 ┌─ MIDDLEMAN FOLDER ──────────────────────────────────────────────────────────────────┐
 │  nothing in here loads in any other session                                         │
 │  .claude/skills/     compliance, scaffold  — load only when a session starts here   │
 │  held plugins        clones or copies of plugins, for taking pieces from            │
 │  personal skills and agents                                                         │
 │  mode source files   (only when memory is on — see mode-loop-map.md)                │
 └─────────────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
 COMPLIANCE             /middleman:compliance      run in the middleman folder
    │                   lists every plugin installed or loading globally
    │                   per plugin: switch it off globally, and hold a copy if pieces
    │                   will be taken from it
    │                   reports first which pieces would break if moved
    ▼
 SCAFFOLD               /middleman:scaffold        run in the middleman folder
    │                   takes a project description
    │                   agents pick candidates from held plugins and personal skills
    │                   checks for conflicting rules and redundant skills
    │                   sorts each pick: which folder needs it (root, research, plan, make)
    ▼
 THE SPLIT              for each plugin, in each folder that needs it:
    │
    │        do you want ALL of it there, or only PART of it?
    │
    ├───────────── ALL ─────────────────────────┬───────────── PART ────────────────────────┐
    ▼                                           ▼                                           │
 SWITCH                                      COPY                                           │
 write into that folder's                    put the chosen pieces into that folder's       │
 .claude/settings.json:                      .claude/:                                      │
   enabledPlugins:                             rules/    real copies (links never load)     │
     <plugin>@<marketplace>: true              skills/   copies, or links to the held copy  │
                                               agents/   copies, or links to the held copy  │
 the plugin stays installed in               the plugin stays switched off in that          │
 ~/.claude/plugins/, switched off            folder and globally — otherwise all of         │
 globally                                    it loads anyway                                │
    │                                           │                                           │
    └─────────────────────┬─────────────────────┘                                           │
                          ▼                                                                 │
 CHECK                    every link resolves; no rule file is a link;                      │
                          a headless probe from each folder confirms what loads ◀───────────┘
```

## 2. The two branches compared

| | ALL — switch the plugin on | PART — copy pieces |
| --- | --- | --- |
| What is written | one `enabledPlugins` line in the folder's settings file | files or links under the folder's `.claude/` |
| Where it takes effect | sessions launched in **that exact folder** **[measured]** | sessions launched in that folder **[measured]** |
| Skill names | `plugin:skill` **[measured]** | bare `skill` name **[proposed]** — not probed for copied plugin skills |
| Pieces that call the plugin's install path | keep working | break — ECC had 26 commands and about 14 skills like this |
| Hooks and MCP servers | **[open]** — not measured whether they follow the switch | not self-contained; left behind |
| Updates | through the plugin manager **[open]** — whether a globally disabled plugin still auto-updates is not established; `claude plugin update <plugin>` is the manual path | links follow the held copy's `git pull`; copies stay as they were until re-copied |
| Cost to the skill-listing budget | the whole plugin's listing | only the chosen pieces |
| Side effects | a root `settings.local.json` probe added a record to `~/.claude/plugins/installed_plugins.json` **[measured]** | none outside the project |

## 3. "A specific folder or project"

The switch does not reach down from a parent folder **[measured]**: set at the project root, the
plugin was absent in `make/`; set in `make/`, it was absent at the root and in `plan/`.

| You want the plugin in… | ALL branch writes the line into… | PART branch copies into… |
| --- | --- | --- |
| one mode | that mode folder's settings file | that mode folder's `.claude/` |
| two modes | each of the two | each of the two — or the root, by the sorting test |
| the whole project | the root **and** every mode folder | the root `.claude/` only |

The last row is an asymmetry: files in the root `.claude/` were visible from mode folders in the
2026-09-28 probe (rules), while the settings switch was not. Root `skills/` and `agents/` from a
mode folder: **[open]**, not probed.

## 4. What decides ALL or PART

Tests for `scaffold` to apply per plugin, per folder **[proposed]**:

1. Does the plugin depend on its own hooks, scripts or MCP servers? Then PART will lose them.
2. Do most of its pieces fit the folder's activity? If few do, ALL spends listing budget on the
   rest.
3. Does a wanted piece call the plugin's install path? Then that piece only works under ALL.
4. Does one of its rules conflict with a rule already in the folder, or a skill duplicate one?
   PART can leave that piece out; ALL cannot.

## 5. A third branch: the slice **[proposed, probed 2026-10-04]**

`enabledPlugins` only says on or off per plugin id. Which pieces load is decided by the plugin's
manifest — and a local marketplace can hold a manifest we write. So PART does not have to mean
copying files into `.claude/`:

```
 MIDDLEMAN FOLDER = a local marketplace
   .claude-plugin/marketplace.json      one entry per held plugin and per slice,
                                        each with defaultEnabled: false
   held/<plugin>/                       the upstream plugin, whole, untouched
   slices/<plugin>-<mode>/
     .claude-plugin/plugin.json         lists only the wanted skills, agents, hooks
     picked/<skill>   ──link──▶         held/<plugin>/skills/<skill>
     agents/<a>.md    ──link──▶         held/<plugin>/agents/<a>.md
     scripts          ──link──▶         held/<plugin>/scripts

 <project>/<mode>/.claude/settings.json
   enabledPlugins:  <plugin>-<mode>@<middleman>: true
```

The per-piece toggle is one list in the slice's `plugin.json`.

| | ALL — switch | PART — copy pieces | PART — slice |
| --- | --- | --- | --- |
| What is written in the project | one settings line | files or links | one settings line |
| Skill names | `plugin:skill` | bare name | `slice:skill` **[measured]** |
| Pieces that call the plugin's install path | work | break | the linked `scripts/` folder resolved under the slice's root **[measured]** |
| Hooks | all of them | left behind | only those the slice lists **[measured]** |
| Updates | plugin manager | re-copy | an edit to the held copy showed next session **[measured]** |
| Remove it | flip the line | delete files | flip the line |
| Global state | install record | none | one marketplace entry in user settings and one in `known_marketplaces.json`; empty data folders for slices with hooks **[measured]** |
| Rules | — | real copies | cannot carry rules — plugins have no rules component (docs) |

Measured limits: a link that leaves the marketplace folder does not load and gives no error; the
held copy was itself a plugin in the same marketplace when the links worked. Full table of probe
results: `.claude/memory/decisions.md`, the entry "a per-piece plugin switch".

## 6. Not yet decided or measured

- Slices **[open]**: two slices of one plugin in one folder; keeping the upstream name so skills
  stay `plugin:skill`; MCP servers in a slice; whether an entry without `defaultEnabled: false`
  loads everywhere; interactive sessions and the trust dialog.

- Where the middleman folder lives is the user's choice at setup **[ruled]**; whether held
  plugins are git clones or copies of the plugin cache **[open]**.
- Whether `compliance` moves a plugin's files or only switches it off and holds a copy
  **[open]** — "do both" was ruled for delivery, not for this step.
- Whether the installed middleman plugin switches itself off globally after setup **[proposed]**.
- Switching a plugin **off** in one folder while it is on globally **[open]**, not measured.
- How `scaffold` records what it delivered, so a later run can update or remove it **[open]**.
