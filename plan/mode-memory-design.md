# Mode memory — the design

**Status:** decided 2026-08-06, from the experiments in
`research/sources/native-memory-keying-and-symlink-experiments.md`. Design only — **nothing is
migrated yet.** Every mechanism below is sentinel-tested on Claude Code 2.1.223 unless marked
otherwise.

## The one-line design

**Build no mode-memory layer.** Native memory is keyed to the **git root** on current Claude Code,
so `research/` / `plan/` / `make/` inside a repo project already share one store. The only shared
mechanism this project adopts is the **shared topic file**: one canonical copy in the store where
it was born, a file-level symlink + index line in any other store that needs it. Everything else
stays per-store.

## What's shared vs what stays per-store

| Thing | Rule |
| --- | --- |
| The store itself | One per git-repo project, at the repo-root encoding — **provided by the platform, no symlinks**. Non-repo dirs still key per-cwd. |
| `MEMORY.md` | **Per-store, always a real file.** Sharing it works mechanically (tested) but is rejected: the index is the store's recall surface, and coupling two stores' indexes makes every save in one appear in the other's auto-loaded context. |
| Topic files | Per-store by default. **Shared only when two disjoint stores genuinely need the same fact** — then ONE canonical copy + file symlinks. Copying is forking; never copy. |
| Store-dir symlinks (`memory/` → shared home) | Works (tested), **not part of the design.** Reserved as a repair tool for a non-repo tree that cannot become a repo. Prefer `git init` — it buys the same unification natively, with no new fragile surface. |

## The routing rule, extended

Existing test (unchanged): *would this still be true if the project were deleted?* Yes → native
memory. No → project memory.

New clause: **a native memory lives in exactly one store** — the store of the narrowest directory
from which every session that needs it starts. If a second store genuinely needs it: the canonical
copy stays where it was born; the consuming store gets `ln -s <canonical> <store>/memory/<name>.md`
plus one index line in its own `MEMORY.md`. The index line is mandatory — harness-side
`description:` recall through symlinks is untested; the index-driven read path is the proven one.

## The update model

- **Edit the canonical file from wherever you encounter it** — Edit writes through the symlink and
  leaves it intact (tested; version-specific, guarded by audit below).
- Index lines are maintained per-store — one line per consuming store is the only duplication
  allowed.
- Adding a shared file = one `ln -s` + one index line per consuming store. Removing one = delete
  links first, canonical last.

**First candidate when migration is approved** (not executed): link
`reference-claude-code-loading-mechanics.md` from the `~/Projects` store into this project's
(currently empty) repo-root store — today the canonical loading reference is invisible from every
session in this repo.

## audit.py changes — same silent-death class as the skill symlinks, plus one worse

The June skill deaths were *silent subtraction*. E5 proved memory symlinks add *silent forking*: a
dangling `memory/` link reads as empty memory with no error, and the **next write recreates the
stale target and makes the link resolve again** — after which a resolve-check passes. Two verified
blind spots in today's `audit.py`: a store whose `memory` symlink dangles vanishes from the report
entirely (the empty-store `continue`), and a dangling topic-file symlink is globbed as a present,
healthy topic. Required checks:

1. **Stranded-subdir-store check (new failure class, highest value).** For every store, if its
   resolved key dir lies **inside a git repo but is not the repo toplevel** (`git -C <dir>
   rev-parse --show-toplevel`), flag it — its memories never load on current Claude Code. Baseline
   2026-08-06: **0 of 24 stores**; the check's job is keeping it zero. Also catches the sneaky
   inverse: creating a repo *above* an existing store's dir strands it retroactively.
2. **`lstat`-level symlink audit inside every store.** Any symlink under `<store>/memory/` (the
   dir itself, or any file) must resolve — checked with `lstat`+`realpath`, not through the glob.
   A dangling link is a ❌, and a store must never be silently skipped because its dir link
   dangles.
3. **Containment invariant.** A memory symlink may point only inside `~/.claude/projects/*/memory/`
   (another store, or its own). Targets elsewhere are flagged. This bounds E5: store dirs are
   already audited against real key dirs, so a legal target that disappears is caught as (2)
   before a write can resurrect-and-fork it.
4. **Fork tripwire (warn-only).** The same topic filename existing as a **regular file** in two or
   more stores (excluding `MEMORY.md`) is a possible fork — either a copy that should be a link,
   or a symlink some writer replaced with a real file. Warn, don't fail: the sweep is cheap and
   names drift honestly sometimes.

`/move-project --check` inherits all four when it exists.

## Rejected, and why

- **A store-dir symlink layer for modes** — duplicates a native platform behavior, and E5 makes
  every such link a fork surface. The highest-value unknown resolved to "the platform already did
  it."
- **Sharing `MEMORY.md` across stores** — couples recall surfaces of unrelated stores.
- **Worktree store linking** — each worktree is its own git toplevel, so worktree sessions key to
  their own (ephemeral) stores. Real fragmentation, low stakes, no observed loss. Revisit only if
  a worktree session ever saves a memory worth keeping.
- **Per-mode stores of any kind** — re-confirmed; now platform-enforced for repo projects, not
  just convention.

## Corrections owed elsewhere (say-so-and-stop items, not edited from research mode)

- Root `CLAUDE.md` two-system table: "keyed by the exact absolute cwd — does *not* walk up" is now
  false for git repos; "survives a folder move: no" softens to "no for non-repo dirs; a repo that
  moves keeps its store only if its *encoded root path* is unchanged — i.e. still no."
- `docs/memory-repair-runbook.md`: routing rules assume exact-cwd keying; orphan routing should
  now target repo roots.
- `audit.py`'s orphan message ("keyed to the exact cwd and does not walk up") needs the git-root
  nuance.
