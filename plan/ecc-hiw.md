# ECC — how it works

Source: a chatbot conversation about the ECC kit (original in `_archive/ecc-hiw_2026-09-24.md`).
The chatbot corrected itself twice in that conversation. Retracted claims are kept below, marked
`[superseded → Rn]`, and point to the rule that replaces them.

## 1. Memory layers

**Definitions**

- ECC memory = 4 separate layers: Rules, Session memory, Instincts, Memory Vault.
- Rules = the memory layer loaded every session.
- Session memory = the memory layer where hooks save a summary as you go and load the last 7 days at session start.
- Instinct = a small trigger/action pair with a confidence score, made by the observer.
- Observer = the background process that turns logged tool calls — your corrections and repeated patterns — into Instincts.
- Memory Vault = the optional memory layer: portable markdown memory shared across tools.

**Rules**

- R1. IF you use the plugin THEN it does not install Rules; copy them yourself.
- R2. IF you copy Rules by hand THEN copy `rules/common` plus ONE language pack you actually use into `~/.claude/rules/ecc/`.
- R3. IF you add each extra language pack THEN it costs context every session.
- R4. IF you want a handoff you control THEN use `/save-session` and `/resume-session`.
- R5. IF tool calls happen THEN they get logged (the Observer's input).
- R6. IF Instincts exist THEN the top few get injected each session.
- R7. IF `observer.enabled` in `skills/continuous-learning-v2/config.json` is left at its shipped value (OFF) THEN nothing is learned — no Instincts. Most videos get this wrong.
- R8. IF you want Memory Vault THEN install its npm package separately.

**Comparisons**

| Layer | Loaded when | Written by | Default state | Extra install |
| --- | --- | --- | --- | --- |
| Rules | every session | you (copy by hand, per R1) | — | — |
| Session memory | session start (last 7 days) | hooks, as you go | — | — |
| Instincts | each session (top few) | Observer | OFF (R7) | — |
| Memory Vault | — | — | optional | npm package |

## 2. Skills

**Definitions**

- Model-invoked skill = a skill Claude matches to a task on its own. Almost all ECC skills are model-invoked.

**Rules**

- R9. IF a skill is model-invoked THEN you don't need to know it; Claude matches the task to it.
- R10. IF you want a specific skill to run THEN force it with `/skill-name`.
- R11. IF the skill matters THEN name it, UNLESS you accept that Claude sometimes falls back to its default behavior.
- R12. IF you are on day one THEN learn: `/ecc:plan`, `tdd-workflow`, `/code-review`, `/build-fix`, `/save-session`, `/resume-session`.
- R13. IF you are curious about anything else THEN use `/ecc:ecc-guide`.
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
- R25. `[superseded → R24]` IF you pick developer THEN it picks skills for your stack (one TypeScript reviewer got 121 of the ~281 skills).
- R26. IF you want memory at the lowest weight THEN pick core.
- R27. IF your work is non-coding THEN research is the profile meant for it.
- R28. IF you pick full THEN it equals the plugin install (~27k tokens, R14).
- R29. IF you want only part of a bundle THEN mix: `--profile core --with <module>`.

**Comparisons**

| Profile | Skills | Built as | Hooks → Session memory + Instincts | Adds on top | Note |
| --- | --- | --- | --- | --- | --- |
| minimal | ~48 | agents + commands | no | — | lightest option |
| core | ~48 | minimal + hooks | yes | hooks | lean pick if you want memory |
| developer | ~125 | core + … | yes | every language/framework skill (React, Python, Go, Rust…), database skills, worktree/tmux orchestration | repo calls it the default for most users |
| security | ~67 | core + … | yes | security review/scanning, compliance skills | — |
| research | ~74 | core + … | yes | deep research, writing, SEO, market research, social posting | for non-coding work |
| full | 292 (all) | everything | yes | everything | same as the plugin install; ~27k tokens |

`[ambiguous in source: total skill count given as both ~281 (R25) and 292 (table)]`
`[ambiguous in source: the Core pack is ~47 skills, but minimal and core are each listed at ~48]`

## 5. Hook profiles

**Definitions**

- Hook profile = a setting separate from the install profile: minimal / standard / strict. Default = standard.

**Rules**

- R30. IF hook profile = minimal THEN Session memory stays on and Instinct learning is off.
- R31. IF hook profile = standard THEN you get Instincts plus quality checks.
- R32. IF hook profile = strict THEN you also get pre-commit and push-review checks.

**Comparisons**

| Hook profile | Session memory | Instincts | Quality checks | Pre-commit + push-review checks | Default |
| --- | --- | --- | --- | --- | --- |
| minimal | yes | no | no | no | no |
| standard | yes | yes | yes | no | yes |
| strict | yes | yes | yes | yes | no |

`[ambiguous in source: whether hook profiles apply to a plugin install as well as a profile install]`

## 6. Plugin vs core — the decision

**Definitions**

- Carter's constraint = no heavy maintenance burden.

**Rules**

- R33. IF you run the plugin and a profile install at the same time THEN everything gets duplicated. Never run both.
- R34. IF you use either path THEN two manual steps remain: copy `rules/common` + one language pack (R2), and turn on the Observer if you want Instincts (R7). `[ambiguous in source: R39 says a core install updates Rules itself, so the rule-copy step may apply to the plugin only]`
- R35. IF you use the plugin THEN you never track what you copied where.
- R36. `[superseded → R37]` IF you use the plugin THEN updates come through Claude Code.
- R37. IF you use either path THEN nothing auto-updates in the background; each update means rerunning one command.
- R38. IF sessions feel slow or context runs out early on the plugin THEN switch to a core install. (The chatbot's opening advice was to start with the plugin; it came before R37.)
- R39. IF you use a core install THEN Rules update along with it.
- R40. IF you use the plugin THEN Rules you copied by hand never update; re-copy them to get newer ones.
- R41. IF you customize ECC THEN put it in your own files, UNLESS you accept that updates overwrite ECC's own files. ECC never touches your files.
- R42. IF you weigh the two paths THEN maintenance is about the same, and the real choice is lean (core) vs one-command simple (plugin).

**Comparisons**

| Criterion | Plugin | Core install |
| --- | --- | --- |
| Skills installed | ~292 (all) | ~48 |
| Context cost per session | ~27k tokens | — |
| Local git clone | not needed | kept |
| Update command | `npx ecc-universal@<new version> setup` or `/ecc:configure-ecc` | `ecc auto-update` (manual despite the name) |
| Auto-updates in background | no | no |
| Rules | copied by hand; never update | update with the install |
| Tracks installed files | — | yes (`ecc doctor` / `ecc repair`) |
| Session memory + Instincts | — | yes (has hooks) |
| Release cadence | every 2–4 weeks | every 2–4 weeks |
| Summary | one-command simple | lean |

**Sequences**

Core install update:
1. Run `ecc auto-update` → 2. it pulls the latest from the git clone → 3. it reinstalls your same profile (Rules included).

Core install health check:
1. Run `ecc doctor` → finds anything broken or changed among the tracked files → 2. Run `ecc repair` → fixes it.

Plugin update:
1. Rerun `npx ecc-universal@<new version> setup` (or `/ecc:configure-ecc`) → 2. Re-copy the hand-copied Rules if you want newer ones (R40).

## Application — when to use which rule

- Setting up ECC via the plugin and Rules aren't loading → R1, R2
- Tempted to add a second language pack → R3
- Handing work to a later session on purpose → R4
- Instincts never appear / "it isn't learning" → R7 (then R5, R6 for how it works)
- Want memory shared with other AI tools → R8
- Unsure whether to learn a skill's name → R9
- Skill didn't fire, or Claude did its default thing → R10, R11
- First day on ECC → R12; anything else → R13
- Sessions feel heavy / context fills early → R14, R15, R38
- Wondering which skills an agent can reach → R16, R17
- Which agent a command uses → R18, R19
- Claude spawned the planner or code-reviewer without being asked → R20, R21
- Comparing install profiles on contents → R22 + the profile table
- A profile gives no Session memory → R23 `[inferred]`
- Expecting developer to fit your stack → R24 (not R25, which is retracted)
- Want memory but light → R26
- Non-coding use → R27
- "Is full different from the plugin?" → R28
- Need one module on top of a lean profile → R29
- "minimal" with no Session memory vs "minimal" with Session memory: the cue is which setting. **Install profile** minimal → R23 (no hooks, no memory). **Hook profile** minimal → R30 (memory on, Instincts off). `[inferred]`
- Want Instincts but not pre-commit gates → R31; want pre-commit/push checks → R32
- Plugin and profile install both present → R33
- Listing setup chores → R34
- Worried about tracking copied files → R35
- Expecting updates to arrive by themselves → R37 (not R36, which is retracted)
- Rules are stale → R39 (core) vs R40 (plugin); the cue is which install path you're on
- About to edit an ECC file → R41
- Choosing plugin vs core under the low-maintenance constraint → R42 + the plugin/core table
