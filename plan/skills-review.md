# Skills review — 2026-09-24

The 80 skills from `/skills`, in the same order. Put `x` in **Keep** or **Delete**; add a note for maybes.

- **Source** — `claude.ai sync` (account skills), `plugin`, or `local` (`~/.claude/skills/`).
- **Status** — `user-only` = only runs when typed as `/<name>`, never auto-loads.
`locked by plugin` = can't be removed alone; deleting it means uninstalling the whole plugin.
- **~tok** — listing cost. claude.ai and plugin values are from the `/skills` screen where visible;
the rest are estimated (description length ÷ 4).

## Name clashes (from the `/skills` footer)

Your local `docx`, `mcp-builder`, `pdf`, `pptx`, `skill-creator`, `xlsx` take the slash command, so
typing `/docx` etc. runs **yours**, not Anthropic's. To use Anthropic's, delete (or rename) the local
one. `/deep-research` is also taken by another command — source not found on disk.

## claude.ai sync

Delete these in claude.ai → Settings → Capabilities, not on disk.


| Keep | Delete | Skill                          | Status                           | ~tok |
| ---- | ------ | ------------------------------ | -------------------------------- | ---- |
| [X]  | [ ]    | anthropic-skills:deep-research |                                  | 200  |
| [X]  | [ ]    | anthropic-skills:docx          | clashes with local docx          | 320  |
| [X]  | [ ]    | anthropic-skills:mcp-builder   | clashes with local mcp-builder   | 100  |
| [X]  | [ ]    | anthropic-skills:pdf           | clashes with local pdf           | 150  |
| [X]  | [ ]    | anthropic-skills:pptx          | clashes with local pptx          | 330  |
| [X]  | [ ]    | anthropic-skills:skill-creator | clashes with local skill-creator | 120  |
| [X]  | [ ]    | anthropic-skills:xlsx          | clashes with local xlsx          | 320  |
| [X]  | [ ]    | built-in-browser               | Desktop-app browser pane (Claude_Browser tools) | 280  |
| [X]  | [ ]    | chrome-browser                 | How to drive Claude in Chrome (your real Chrome) | 260  |
| [X]  | [ ]    | computer-use                   | Screenshot + click/type in desktop apps | 320  |
| [X]  | [ ]    | docs                           | Claude Docs: shared, editable docs | 330  |
| [ ]  | [X]    | import-memory                  | Import memory export from another AI; delete in claude.ai | 60   |
| [ ]  | [X]    | morning                        | delete in claude.ai | 120  |
| [X]  | [ ]    | slack-gif-creator              |                                  | 90   |




## Plugin: supabase (1)


| Keep | Delete | Skill    | Status           | ~tok |
| ---- | ------ | -------- | ---------------- | ---- |
| [X]  | [ ]    | supabase | locked by plugin | ~145 |




## Local — `~/.claude/skills/` (22)

Each one can be deleted on its own.


| Keep                                                             | Delete | Skill                    | Status                    | ~tok |
| ---------------------------------------------------------------- | ------ | ------------------------ | ------------------------- | ---- |
| [X]                                                              | [ ]    | blocksite                |                           | ~85  |
| [X]                                                              | [ ]    | capture-feedback         |                           | ~50  |
| [X]                                                              | [ ]    | clean-transcript         |                           | ~45  |
| [X]                                                              | [ ]    | close-session            | user-only                 | ~75  |
| [X]                                                              | [ ]    | day-shift                |                           | ~70  |
| [X]                                                              | [ ]    | dream                    |                           | ~70  |
| [X; remove description]                                          | [ ]    | email-tracker            |                           | ~85  |
| [X]                                                              | [ ]    | equationify              | user-only                 | ~35  |
| [X; make this a project specific skill for the associated class] | [ ]    | fill-notes               | moved to business-law     | ~60  |
| [ ]                                                              | [ ]    | find-docs                | ctx7 library docs; same as rules/context7.md | ~225 |
| [X; remove description]                                          | [ ]    | github-digest            |                           | ~50  |
| [X; need to remember what this does]                             | [ ]    | memory-review            | user-only                 | ~55  |
| [X]                                                              | [ ]    | morning-shift            |                           | ~75  |
| [X; remove description]                                          | [ ]    | new-project              | user-only                 | ~140 |
| [X]                                                              | [ ]    | night-shift              |                           | ~90  |
| [X]                                                              | [ ]    | restructure-project      | user-only                 | ~155 |
| [X; make this a project specific skill for the associated class] | [ ]    | supplement               | moved to business-law     | ~80  |
| [X]                                                              | [ ]    | todos                    | user-only, no description | 0    |
| [X]                                                              | [ ]    | transcribe-media         |                           | ~65  |
| [X]                                                              | [ ]    | ui-ux-pro-max            |                           | ~50  |
| [X]                                                              | [ ]    | write-doc                |                           | ~65  |
| [X; change name to /yt and remove description]                   | [ ]    | youtube-slide-transcript | user-only                 | ~155 |




## Not in `/skills` (for reference)

- **Installed but disabled plugins:** modern-web-guidance (2 skills), vercel (~40 skills). Uninstall
with `/plugin` if you don't want them on disk.
- **mattpocock folders the plugin doesn't register** (10): claude-handoff, loop-me,
setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape, git-guardrails-claude-code,
migrate-to-shoehorn, scaffold-exercises, setup-pre-commit. They never load.
- **Built into Claude Code** (dataviz, artifact-*, loop, schedule, code-review, simplify, etc.) —
not listed by `/skills`, not removable.

