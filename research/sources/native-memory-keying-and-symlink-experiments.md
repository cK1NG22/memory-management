# Native memory: keying and symlink experiments

**Date:** 2026-08-06 · **Claude Code:** 2.1.223 · **Platform:** darwin 25.5.0
**Method:** sentinel strings planted in pre-created stores under `~/.claude/projects/`, probed with
headless `claude -p --model haiku` runs from throwaway directories under `/private/tmp/memtest-ck/`
(physical path, no symlinks, outside `$HOME` — no real CLAUDE.md or memory chain in scope). All
`CLAUDE*` env vars stripped from probe runs. Everything created was deleted afterward;
`audit.py` exits 0.

**Provenance labels:** *controlled* = reproducible experiment in an isolated throwaway tree.
*machine* = observation of this machine's real state. *derived* = reasoned, not tested.

---

## The headline: native memory is keyed to the git root, not the exact cwd

**[controlled]** A git repo `egit/` with subdir `egit/sub/`. Both candidate stores pre-created with
different sentinels (`…-egit/memory/MEMORY.md` and `…-egit-sub/memory/MEMORY.md`). A session run in
`egit/sub/`:

- loaded **only** the git-root store's sentinel — the subdir store's sentinel appears **nowhere**
  in the session transcript (grep-verified, not just absent from the reply);
- **wrote** its memory to the git-root store too (asked to create a file in "your memory
  directory", it created `…-egit/memory/write-probe.md`). Reads and writes agree;
- put its **transcript `.jsonl` in the cwd-keyed dir** (`…-egit-sub/`). Transcripts and memory key
  differently — a store dir with only `.jsonl` files and no `memory/` is normal, not a bug.

**[controlled]** Control (E0): a **non-git** directory keys to the **exact cwd** — the old rule
still holds outside repos.

**[machine]** Corroboration: this very session (cwd `…/memory-management/research/`, a repo subdir)
was handed `…-Users-carterking-Projects-memory-management/memory/` — the repo root's store — as its
memory directory, while its transcript sits in the `…-memory-management-research` store dir.

**Consequence:** the recorded finding "native memory does not walk up the tree" (2026-08-04) was
**overgeneralized from non-git test dirs**. It is still true outside git repos; inside a repo, the
store follows the repo root. `research/` → `plan/` → `make/` inside one repo project **already
share one store natively**. The per-mode fragmentation problem this session was opened to solve
does not exist on current Claude Code — for git-repo projects.

**New stranding class:** any store keyed to a *subdirectory* of a git repo is now invisible — the
files sit on disk, healthy-looking, and never load. **[machine]** Swept all 24 live stores on
2026-08-06: every one is keyed to a repo root or a non-repo dir — **zero stranded today.** The
2026-08-04 orphan routing happened to land everything in the safe configuration. An audit check
must keep it that way (see the design in `plan/mode-memory-design.md`).

**[derived]** Untested edges: nested repos/submodules; whether "git root" means the innermost or
outermost repo; worktrees are their own `git` toplevel, so each worktree keys to its own store —
consistent with the two `…--claude-worktrees-…` store dirs observed on this machine **[machine]**.

**[controlled, added 2026-08-06]** Ancestor stores never stack — unlike CLAUDE.md. Two probes:
(A) non-git `child/` with sentinels planted in both its own store and its parent folder's store —
only the child's loaded; (B) a git repo with a sentinel planted in the store of the folder *above*
the repo — only the repo-root store loaded. **Exactly one store loads per session, ever.** CLAUDE.md
walks the whole tree upward and stacks; MEMORY.md resolves to one store (git root, else exact cwd)
and reads nothing else.

---

## E4 — logical vs physical cwd: physical wins

**[controlled]** Real dir `e4real/`, symlink `e4link → e4real`. Stores pre-created for both
encodings with different sentinels. Session launched via `cd e4link` (shell `$PWD` = the logical
symlink path): the **physical** store's sentinel loaded.

**Consequence:** entering a project through a symlinked path cannot fork its store. Symlinked
*paths* are safe; it's symlinked *stores* that carry risk (below).

## E1 — a store's `memory/` dir can be a symlink to a shared home

**[controlled]** `~/.claude/projects/<enc>/memory → /…/shared-e1/` (real dir with `MEMORY.md`
sentinel), planted **before** the cwd's first-ever session:

- `MEMORY.md` auto-loads through the dir symlink;
- a session asked to write into "your memory directory" succeeds — the file lands **physically in
  the shared target**;
- the symlink **survives** multiple sessions; the harness never replaces it.

## E3 — `MEMORY.md` alone can be a file-level symlink

**[controlled]** Real store dir, `MEMORY.md → /…/shared-e3/MEMORY.md`:

- auto-loads through the file symlink;
- a session asked to append a line did so **through** the link (Edit tool): target file updated,
  symlink intact. The atomic-rename-replaces-symlink failure did **not** occur with the Edit tool
  on 2.1.223. **[derived]** Other write paths (future harness versions, tools that write via
  rename) are untested — treat "the link survives writes" as version-specific, not permanent.

## E2 — topic files can be symlinks and still lazy-load

**[controlled]** Real store, real `MEMORY.md` with an index line pointing at
`topic-zebra-deploy.md`, which is a symlink to a shared file (frontmatter + sentinel in the body).
A session asked about the topic followed the index, read the file through the symlink, and
surfaced the sentinel.

**[derived]** This proves the **model-driven** read path (index line → Read). Whether the
harness-side `description:`-match recall also follows symlinks is untested — no deterministic way
to trigger it was found. A shared topic file must therefore always carry an index line in each
consuming store's `MEMORY.md`; don't rely on description-match alone.

## E5 — the failure mode: silent, and worse than the skill-symlink deaths

**[controlled]** Simulated a June-style folder move: `mv shared-e1 shared-e1-moved`, leaving the
store's `memory` dir symlink dangling. Then:

- **Read:** the next session reports no sentinels, **no error anywhere** — memory is silently
  empty. Same silence class as the 12 dead skill symlinks.
- **Write:** a later save **succeeds** — the write's `mkdir -p` follows the dangling symlink and
  **recreates the target directory at the stale path**. Result: the moved dir keeps the old
  memories, a fresh dir exists at the dead path holding only the new file, and the symlink
  *resolves again*. The store has forked, and a naive "does the link resolve?" check now passes.
  **A dangling memory symlink self-heals into a camouflaged fork.**

**Consequence for `audit.py`:** resolve-checks alone cannot catch this class after the first
write. Two current blind spots verified by reading the code: (1) a store whose `memory` dir
symlink dangles produces zero `*.md` globs and no index, so the `continue` at the top of the loop
**drops the store from the report entirely**; (2) a dangling topic-file symlink still appears in
the directory listing, so it counts as a present, healthy topic. Both need explicit `lstat`-level
checks — specified in `plan/mode-memory-design.md`.

---

## What this settles

1. **Q1 (shared store per project via symlinks): moot for git projects** — the platform already
   unifies research/plan/make into the repo-root store. The symlink mechanism works (E1) but is
   only needed as a repair tool for non-repo trees.
2. **Q2 (shared topic files): yes** — file symlink + per-store index line, proven end to end.
3. **Q3 (MEMORY.md as symlink): mechanically yes, rejected by design** — the index is the
   per-store surface; sharing it couples unrelated stores (see design doc).
4. **Q4 (logical vs physical): physical** — symlinked entry paths cannot fork stores.
5. **The live specimen:** `reference-claude-code-loading-mechanics.md` sits in the `~/Projects`
   store, which repo sessions never load — the canonical loading reference is invisible from the
   project that maintains it **[machine]**. This is the worked example for the Q2 pattern.
