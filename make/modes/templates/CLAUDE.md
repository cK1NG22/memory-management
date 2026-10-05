# {{PROJECT}}

One paragraph: what this project is. Mode-invariant facts only. Keep it tiny; it loads in every
session in this project, whichever mode you start in.

## Read this first

- **`.claude/memory/context.md`** — where things stand right now, and what's next.
- **`.claude/memory/decisions.md`** — what was decided and why. Append-only.
- **`TODO.md`** — the live task list.

## Modes

`research/` → `plan/` → `make/`. Start a session in the folder that matches the work. Each folder
carries its own `CLAUDE.md` and its own `.claude/` (`rules/`, `skills/`, `agents/`), which load only
when the session starts in that folder. Modes control **what loads**, not what you may write: the
boundaries below are a convention with a tripwire, never enforcement.

## Memory

There are two independent memory systems. The routing test for any fact: **would this still be true
if the project were deleted?** Yes → native memory (`~/.claude/projects/<key>/memory/`, facts about
you and your machine). No → project memory (`.claude/memory/`, facts about the work).

Memory lives **once, at this root**, not per mode. Native memory keys to the git root, so mode
folders and worktrees all share this project's one store.

## Conventions

- `.claude/` is **committed**; only `.claude/worktrees/` and `.claude/settings.local.json` are
  ignored.
- Plans and roadmaps are **present-tense and rewritten**; they live in `plan/`.
  Memory is **past-tense and immutable**; it lives in `.claude/memory/`.
