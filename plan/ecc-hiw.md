# ECC — how it works

Source: a chatbot conversation about the ECC kit (original in `_archive/ecc-hiw_2026-09-24.md`).
The chatbot corrected itself twice in that conversation. The retracted developer-profile claim is
deleted; the retracted update claim is kept below, marked `[superseded → Rn]`.
Section 7 answers Carter's review questions from local notes, not from the chat.

## 1. Memory layers

**Definitions**

- ECC memory = 4 separate layers: Rules, Session memory, Instincts, Memory Vault.
- Rules = the memory layer loaded every session [need to review][]
- Session memory = the memory layer where hooks save a summary as you go and load the last 7 days at session start [off to start][]
- Instinct = a small trigger/action pair with a confidence score, made by the observer [do not use][]
- Observer = the background process that turns logged tool calls — your corrections and repeated patterns — into Instincts [do not use][]
- Memory Vault = the optional memory layer: portable markdown memory shared across tools. [do not use][]

**Rules**

- R1. IF you use the plugin THEN it does not install Rules; copy them yourself.
- R2. IF you copy Rules by hand THEN copy `rules/common` plus ONE language pack you actually use into `~/.claude/rules/ecc/`. [what is a language pack][] → §7
- R3. IF you add each extra language pack THEN it costs context every session.
- R4. IF you want a handoff you control THEN use `/save-session` and `/resume-session` [doesn't seem to conflict with /save-session; might be interesting to have /save-session be a hook (automatically updates state files)][]
- R5. IF tool calls happen THEN they get logged (the Observer's input) [why is this useful][] → §7
- R6. IF Instincts exist THEN the top few get injected each session [not going to use unless research on reviews say otherwise][]
- R7. IF `observer.enabled` in `skills/continuous-learning-v2/config.json` is left at its shipped value (OFF) THEN nothing is learned — no Instincts. Most videos get this wrong.
- R8. IF you want Memory Vault THEN install its npm package separately. [no need][]

**Comparisons**


| Layer          | Loaded when                 | Written by                 | Default state | Extra install |
| -------------- | --------------------------- | -------------------------- | ------------- | ------------- |
| Rules          | every session               | you (copy by hand, per R1) | —             | —             |
| Session memory | session start (last 7 days) | hooks, as you go           | —             | —             |
| Instincts      | each session (top few)      | Observer                   | OFF (R7)      | —             |
| Memory Vault   | —                           | —                          | optional      | npm package   |




## 2. Skills

**Definitions**

- Model-invoked skill = a skill Claude matches to a task on its own. Almost all ECC skills are model-invoked.

**Rules**

- R9. IF a skill is model-invoked THEN you don't need to know it; Claude matches the task to it.
- R10. IF you want a specific skill to run THEN force it with `/skill-name`.
- R11. IF the skill matters THEN name it, UNLESS you accept that Claude sometimes falls back to its default behavior.
- R12. IF you are on day one THEN learn: `/ecc:plan`, `tdd-workflow`, `/code-review`, `/build-fix`, `/save-session`, `/resume-session`.
- R13. IF you are curious about anything else THEN use `/ecc:ecc-guide`. [how does ecc-guide work if I dont do the complete download? does it make sure to only reference the skills I downloaded?][] → §7
- R14. IF you do a full install THEN about 27k tokens of skill descriptions load into every session.
- R15. IF a full install feels heavy THEN reinstall with a profile (e.g. "developer") instead of the full plugin.



## 3. Agents

**Definitions**

- Agent–skill link = loose, not hard-wired: agent prompts point to relevant skills by name.

**Rules**

- R16. IF you look at any of the 68 agents THEN none preloads specific skills.
- R17. IF a skill is installed THEN any agent can use it.
- R18. IF you run `/ecc:plan` THEN it uses the planner agent (pairing happens at the workflow level).
- R19. IF you run `/code-review` THEN it uses the code-reviewer agent. UNLESS [other workflow→agent pairs exist: source says "and so on" without listing them].
- R20. IF a feature is complex THEN Rules tell Claude to use the planner automatically.
- R21. IF changes were made THEN Rules tell Claude to use the code-reviewer automatically.



## 4. Install profiles

**Definitions**

- Install profile = one of six fixed ECC bundles: minimal, core, developer, security, research, full.
- Core pack = the ~47 workflow skills every install profile includes (e.g. `tdd-workflow`, `verification-loop`, `continuous-learning-v2`, `ecc-guide`).

**Rules**

- R22. IF you pick any install profile THEN you get all 68 agents, all commands, Rules, and the Core pack.
- R23. IF the install profile has no hooks THEN there is no Session memory and no Instincts.
- R24. IF you pick developer THEN you get a fixed bundle with every framework's skills — it does not tailor itself to your stack.
- R25. IF you want memory at the lowest weight THEN pick core.
- R26. IF your work is non-coding THEN research is the profile meant for it [I want to see if there is a way to download the plugin and separate the skills into my mode folders][] → §7
- R27. IF you pick full THEN it equals the plugin install (~27k tokens, R14).
- R28. IF you want only part of a bundle THEN mix: `--profile core --with <module>`.

**Comparisons**


| Profile   | Skills    | Built as          | Hooks → Session memory + Instincts | Adds on top                                                                                             | Note                                     |
| --------- | --------- | ----------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| minimal   | ~48       | agents + commands | no                                 | —                                                                                                       | lightest option                          |
| core      | ~48       | minimal + hooks   | yes                                | hooks                                                                                                   | lean pick if you want memory             |
| developer | ~125      | core + …          | yes                                | every language/framework skill (React, Python, Go, Rust…), database skills, worktree/tmux orchestration | repo calls it the default for most users |
| security  | ~67       | core + …          | yes                                | security review/scanning, compliance skills                                                             | —                                        |
| research  | ~74       | core + …          | yes                                | deep research, writing, SEO, market research, social posting                                            | for non-coding work                      |
| full      | 292 (all) | everything        | yes                                | everything                                                                                              | same as the plugin install; ~27k tokens  |


`[ambiguous in source: the Core pack is ~47 skills, but minimal and core are each listed at ~48]`

## 5. Hook profiles

**Definitions**

- Hook profile = a setting separate from the install profile: minimal / standard / strict. Default = standard.

**Rules**

- R29. IF hook profile = minimal THEN Session memory stays on and Instinct learning is off.
- R30. IF hook profile = standard THEN you get Instincts plus quality checks.
- R31. IF hook profile = strict THEN you also get pre-commit and push-review checks.

**Comparisons**


| Hook profile | Session memory | Instincts | Quality checks | Pre-commit + push-review checks | Default |
| ------------ | -------------- | --------- | -------------- | ------------------------------- | ------- |
| minimal      | yes            | no        | no             | no                              | no      |
| standard     | yes            | yes       | yes            | no                              | yes     |
| strict       | yes            | yes       | yes            | yes                             | no      |


`[ambiguous in source: whether hook profiles apply to a plugin install as well as a profile install]`

## 6. Plugin vs core — the decision

**Definitions**

- Carter's constraint = no heavy maintenance burden.

**Rules**

- R32. IF you run the plugin and a profile install at the same time THEN everything gets duplicated. Never run both.
- R33. IF you use either path THEN two manual steps remain: copy `rules/common` + one language pack (R2), and turn on the Observer if you want Instincts (R7). `[ambiguous in source: R38 says a core install updates Rules itself, so the rule-copy step may apply to the plugin only]`
- R34. IF you use the plugin THEN you never track what you copied where.
- R35. `[superseded → R36]` IF you use the plugin THEN updates come through Claude Code.
- R36. IF you use either path THEN nothing auto-updates in the background; each update means rerunning one command.
- R37. IF sessions feel slow or context runs out early on the plugin THEN switch to a core install. (The chatbot's opening advice was to start with the plugin; it came before R36.)
- R38. IF you use a core install THEN Rules update along with it.
- R39. IF you use the plugin THEN Rules you copied by hand never update; re-copy them to get newer ones.
- R40. IF you customize ECC THEN put it in your own files, UNLESS you accept that updates overwrite ECC's own files. ECC never touches your files.
- R41. IF you weigh the two paths THEN maintenance is about the same, and the real choice is lean (core) vs one-command simple (plugin).

**Comparisons**


| Criterion                  | Plugin                                                          | Core install                                |
| -------------------------- | --------------------------------------------------------------- | ------------------------------------------- |
| Skills installed           | ~292 (all)                                                      | ~48                                         |
| Context cost per session   | ~27k tokens                                                     | —                                           |
| Local git clone            | not needed                                                      | kept                                        |
| Update command             | `npx ecc-universal@<new version> setup` or `/ecc:configure-ecc` | `ecc auto-update` (manual despite the name) |
| Auto-updates in background | no                                                              | no                                          |
| Rules                      | copied by hand; never update                                    | update with the install                     |
| Tracks installed files     | —                                                               | yes (`ecc doctor` / `ecc repair`)           |
| Session memory + Instincts | —                                                               | yes (has hooks)                             |
| Release cadence            | every 2–4 weeks                                                 | every 2–4 weeks                             |
| Summary                    | one-command simple                                              | lean                                        |


**Sequences**

Core install update:

1. Run `ecc auto-update` → 2. it pulls the latest from the git clone → 3. it reinstalls your same profile (Rules included).

Core install health check:

1. Run `ecc doctor` → finds anything broken or changed among the tracked files → 2. Run `ecc repair` → fixes it.

Plugin update:

1. Rerun `npx ecc-universal@<new version> setup` (or `/ecc:configure-ecc`) → 2. Re-copy the hand-copied Rules if you want newer ones (R39).



## 7. Answers to review questions

Source: `plan/ecc-decisions.md` (items 2, 7, 23) and the `reference-ecc-kit-evaluation` memory note.
Nothing here comes from the chat or the web.

**Definitions**

- `rules/common` = 10 rule files, ≈18,100 bytes ≈ 4,500 tokens: agents, code-review, coding-style, development-workflow, performance, testing, patterns, security, git-workflow, hooks.
- Language pack = a folder of 5–8 rule files that sits beside `rules/common` in ECC's rules tree (whole tree = 122 files, 286 KB). `[inferred: one pack per programming language — the name and R2's "one you actually use" suggest it; the notes don't say]`
- observe-runner = the hook that writes each tool call and its outcome to the homunculus observations file. It is the logging in R5, and the Observer's only input.
- Ledger = `~/.claude/ecc/install-state.json`, the record of every file an ECC install created. `doctor`, `repair` and `list-installed` work from it.

**Rules**

- R42. IF the harness reads subfolders of `~/.claude/rules/ecc/` THEN `rules/common` costs ≈4,500 tokens every session, in every project. `[not verified on this machine — probe in ecc-decisions item 7]`
- R43. IF the Observer is off THEN observe-runner is cost with no benefit. It still starts on every tool call under the `standard` hook profile.
- R44. IF you want one hook off (e.g. observe-runner) THEN list it in `ECC_DISABLED_HOOKS`.
- R45. IF you install skills with `install.sh --skills a,b,c` THEN each is copied to `~/.claude/skills/<name>/`, which is global, not a mode folder.
- R46. IF skills are copied THEN `skillOverrides` and usage-based trimming work on them.
- R47. IF skills come from the plugin THEN `skillOverrides` can't trim them.
- R48. IF you copy skills THEN it is vendoring, which ALWAYS.md forbids. The ledger makes the copy upgradeable (re-run the installer from a newer checkout), which lowers the risk but doesn't make it an exception.
- R49. IF you ask whether `/ecc:ecc-guide` only points to installed skills THEN `[not in local files — needs the ecc-guide skill source in the ECC repo]`.
- R50. IF you move copied skills into `<mode>/.claude/skills/` THEN `[not in local files — whether the ledger, doctor and repair still track them]`.

## Application — when to use which rule

- Setting up ECC via the plugin and Rules aren't loading → R1, R2
- Tempted to add a second language pack → R3
- Handing work to a later session on purpose → R4
- Instincts never appear / "it isn't learning" → R7 (then R5, R6 for how it works)
- Want memory shared with other AI tools → R8
- Unsure whether to learn a skill's name → R9
- Skill didn't fire, or Claude did its default thing → R10, R11
- First day on ECC → R12; anything else → R13
- Sessions feel heavy / context fills early → R14, R15, R37
- Wondering which skills an agent can reach → R16, R17
- Which agent a command uses → R18, R19
- Claude spawned the planner or code-reviewer without being asked → R20, R21
- Comparing install profiles on contents → R22 + the profile table
- A profile gives no Session memory → R23 `[inferred]`
- Expecting developer to fit your stack → R24
- Want memory but light → R25
- Non-coding use → R26
- "Is full different from the plugin?" → R27
- Need one module on top of a lean profile → R28
- "minimal" with no Session memory vs "minimal" with Session memory: the cue is which setting. **Install profile** minimal → R23 (no hooks, no memory). **Hook profile** minimal → R29 (memory on, Instincts off). `[inferred]`
- Want Instincts but not pre-commit gates → R30; want pre-commit/push checks → R31
- Plugin and profile install both present → R32
- Listing setup chores → R33
- Worried about tracking copied files → R34
- Expecting updates to arrive by themselves → R36 (not R35, which is retracted)
- Rules are stale → R38 (core) vs R39 (plugin); the cue is which install path you're on
- About to edit an ECC file → R40
- Choosing plugin vs core under the low-maintenance constraint → R41 + the plugin/core table
- Deciding whether to copy `rules/common` → R42 (run the probe first)
- Observer declined, but tool calls still run a hook → R43, R44
- Want ECC skills split across research / plan / make → R45, then R50 (open); plugin-vs-copy trimming → R46 vs R47; the cue is which install path
- About to copy ECC skills in → R48
- Wondering what `/ecc:ecc-guide` will suggest on a partial install → R49 (open)

