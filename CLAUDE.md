# memory-management

Carter's memory, context, and project-structure system. **Ongoing** — not a project that finishes.

This is also the **first project built in the Gen 4 "mode" structure**, so it is the trial as well as
the subject.

## Read this first

- **`.claude/memory/context.md`** — where things stand right now, and what's next.
- **`.claude/memory/decisions.md`** — what was decided and why. Append-only.
- **`docs/memory-systems-history.md`** — the single surviving record of the four memory-system
  generations. **Read before deleting any memory store.** Everything it describes has been deleted.
- **`docs/memory-repair-runbook.md`** — the procedure for recovering memory stranded by a folder move,
  with the tools in `make/memory-repair/`. **Run `audit.py` before and after moving any folder.**
- **`docs/ecc-runbook.md`** — how to use ECC and load it into a build. The library clone is
  `ecc/` (gitignored, its own repo).

## The one thing to know

There are **two independent memory systems**, and conflating them causes every failure in this
project's history:

| | **Native memory** | **Project memory** |
| --- | --- | --- |
| Where | `~/.claude/projects/<encoded-cwd>/memory/` | `<project>/.claude/memory/` |
| Keyed by | the **git root** when cwd is inside a repo, else the exact cwd | path relative to the project |
| Loaded | `MEMORY.md` auto every session; topic files on `description:` match | **nothing auto-loads it** — a pointer must fetch it |
| Survives a folder move | **no** — the store is stranded silently | **yes** |
| Holds | facts about **Carter and this machine** | facts about **the work** |

**Routing test for any fact: would this still be true if the project were deleted?**
Yes → native memory. No → project memory.

**Keying, precisely (probe-verified 2026-08-10):** *transcripts* key to the **launch cwd**; native
*memory* keys to the **main repo root**. That is why `~/.claude/projects/` holds a directory per
working directory — `…-memory-management-make`, `…-research`, one per worktree — while **only the
repo-root directory has a `memory/` folder**. Two probes: the `make/` session's transcript sits in
the `…-make` store while its memory writes landed in the repo-root store; and a session launched
inside `.claude/worktrees/stale-blockers` reported the **main repo's** store as its memory dir.

Resolve the key with `git rev-parse --path-format=absolute --git-common-dir` minus the trailing
`/.git` — **not** `--show-toplevel`, which returns the worktree. So mode folders and worktrees
cannot fragment native memory, and deleting a worktree does not orphan it. A store still strands
when the *repo* moves.

## The modes

`research/` → `plan/` → `make/`. Each carries its own `CLAUDE.md` and its own `.claude/skills/`.
Modes are a **loading mechanism, not a locking one** — they control which skills and instructions
load, and they are a convention, never enforcement. Nothing available in Claude Code is a hard write
boundary; see `docs/mode-review-verdict.md`.

Memory lives **once, at this root** — not per mode. Git-root keying already puts it there: a
`make/` or `research/` session writes to the root store, so the modes cannot fragment it. Project
memory is kept at the root to match.

## Conventions

- `.claude/` is **committed**; only `.claude/worktrees/` is ignored. `settings.local.json` is the
  per-user layer and is never committed.
- No `history.md`. It had three writers and no readers; git already records what happened.
- Plans, PRDs, and roadmaps are **present-tense and rewritten** — they live in `plan/`.
  Memory is **past-tense and immutable** — it lives in `.claude/memory/`.
