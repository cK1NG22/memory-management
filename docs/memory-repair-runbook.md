# Runbook — repairing stranded memory

**What this is for:** memory files that have gone invisible because the folder they were attached to
moved, was renamed, or was dissolved. Followed end-to-end on 2026-08-04 to recover 165 files across
16 dead stores; this is that process, written down so it does not have to be re-derived.

**Tools:** `../make/memory-repair/` — `audit.py`, `dump.py`, `route.py`, `mkindex.py`.
**Historical record of what was actually recovered:** `memory-systems-history.md`.

---

## The mechanism — why this keeps happening

Native memory lives at `~/.claude/projects/<encoded-path>/memory/`, where the encoded name is an
absolute path with non-alphanumerics (`/`, space, `_`) replaced by `-`. **The key is the git root
when the session runs inside a repo, and the exact directory otherwise.** It never walks up past
that the way `CLAUDE.md` does.

Repo-root keying is what makes mode folders and worktrees safe — they share the repo's one store.
Probe-verified 2026-08-10, two ways: a `make/` session's transcript sat in the `…-make` store while
its memory writes landed in the repo-root store, and a session launched inside a worktree reported
the **main repo's** store as its memory dir (the worktree's own store directory held a transcript
and no `memory/` folder). Resolve the key with
`git rev-parse --path-format=absolute --git-common-dir` minus the trailing `/.git` — `--show-toplevel`
returns the *worktree* and is the wrong tool here.

None of that makes the store safe from a **move**: the key is still a path, so relocating the repo
strands everything. That is what this runbook exists for.

So when a folder moves:

- the memory **stays at the old address** and stops loading;
- work continues from the new address, which **silently starts a second, empty store**;
- nothing reports anything, because from inside a session there is no difference between "this project
  has no memory" and "this project's memory is 40 files sitting at an address nobody reads."

> `mana-ventures` ran for weeks with **29 files at a dead address and 7 at the live one.**
> The project didn't lose its memory. It started a second one from zero.

**A move is the failure. Not a crash, not a bad write — an ordinary, successful folder move.**

---

## Step 0 — Detect

```bash
python3 make/memory-repair/audit.py
```

Runs with no arguments, exits `0` when clean and `1` when not. Reports orphaned stores, dangling index
links, and files on disk that no index mentions.

Run it **before** and **after** any folder reorganization. Before, so you know what is about to break;
after, so you find out immediately rather than in three months.

### Why it walks the filesystem instead of decoding the name

The encoding is lossy. `mana-ventures` (one folder, real hyphen) and `mana/ventures` (two folders)
produce the identical string. A naive decode splits on every hyphen and reports a false orphan for
every folder whose name contains one.

`audit.py` instead tries every possible split against the real filesystem and reports the deepest path
that exists. If it cannot consume the whole name, the store is genuinely orphaned and you get the
resolved prefix plus the part that no longer exists — which tells you *where* the folder used to be.

> ⚠️ **Two orphans hid behind directories that still existed.** `~/Projects/Sandbox` and
> `~/Projects/Sandbox/velocity` resolve fine — but they hold nothing except stale git worktrees. The
> real work had moved to `~/Sandbox/builds/velocity`. **Resolving a path is not the same as verifying
> the project is there.** Spot-check anything with a suspiciously small file count.

---

## Step 1 — Back up before touching anything

```bash
cp -R ~/.claude/projects/<slug>/memory ~/Claude/_archive/orphan-stores_<YYYY-MM-DD>/<slug>
```

Copy every affected store first, in one shot. Cheap, and it is the only thing that makes the delete
step safe to do decisively rather than nervously.

Use Python (or `./`-prefixed paths) rather than bare shell globs here: **store names begin with `-`,
so `cp`, `rm`, and `[` parse them as command-line flags.** This bites every single time.

---

## Step 2 — Find where each dead project went

For each orphan, locate the successor folder. `audit.py` gives you the old path; you need the new one.

```bash
ls ~/Optimal ~/Clients ~/Sandbox ~/Projects ~/Archive
```

Three outcomes, and the third is the one people get wrong:

| | |
|---|---|
| **Moved** | The folder exists under a new parent → route the memory to the new cwd. |
| **Gone** | Nothing on disk → the memories are candidates for deletion, but read them first. |
| **Split** | One old folder became two or more → decide which one owns the memory. Do not copy to both. |

Do not skip this. Routing memory to a folder that does not exist just creates a fresh orphan.

---

## Step 3 — Triage by reading descriptions

```bash
python3 make/memory-repair/dump.py <slug> [more-slugs...]
```

Prints each file's `name`, `type`, `description`, and size. **Read descriptions, not bodies.** The
`description:` field is what recall matches on, so it is both the cheapest summary and the thing that
determines whether the file was ever going to be found again.

### The question that does the work

> **Does this file's subject still exist?**

Not the routing test — that comes later, and only for the survivors. Ask whether the thing the file
describes is still real: the repo, the client, the tool, the decision.

Of 165 orphaned files, **only 9 failed this.** Orphaned stores are usually full of live work that went
dark, not rot. (The legacy hub was the opposite — same question, far more deletions. Rules rot when
the world moves; work goes dark when the folder moves. Different failure, same question.)

### Then route the survivors

> **Would this fact still be true if the project were deleted?**
> **Yes** → native memory (Carter and this machine). **No** → project memory (the work).

### Two things `dump.py` will show you

**`[?]` with "(no description)" means it is probably not a memory.** 17 of Locker's 18 files were
phased build plans — no frontmatter, no descriptions — written into a memory folder because it was the
nearest writable place. They were moved to `~/Archive/Locker-UI/plans/`, not deleted: outside the
memory system they cost nothing, and a killed product's plans are still a record.

**A memory store full of files with no frontmatter means the tool was used as a folder.** Move the
contents somewhere they belong instead of routing them.

---

## Step 4 — Route, from an explicit manifest

```bash
python3 make/memory-repair/route.py my-manifest.py
```

The manifest names **every file** — see `route.py`'s docstring for the format. This is deliberate: a
glob would move files nobody looked at, which defeats step 3. `route.py` reports `LEFT n` for anything
unaccounted for, and **the run is not finished until every store reports `LEFT 0`.**

### The two routing decisions that mattered

**Preserve folder depth; fix only the path.** A store existed at `~/Projects/Optimal/mana-drive-reorg`
because sessions were started from that folder. Its successor `~/Optimal/mana-drive-reorg` exists, so
the memory goes *there* — not flattened up to `~/Optimal`, where it would be invisible from the very
folder it describes. Changing the depth is a second, unrequested migration.

**Consolidate a project that was already fragmented.** Velocity had memory in three separate dead
stores. Preserving that split would have preserved the fragmentation that caused the loss, so it was
merged into one. *Fix the path by default; consolidate only when the split is itself the bug.*

Rejected: folding everything into `~/Projects`. Simpler, and wrong — every client and sandbox fact
would then load on every session in the main working directory, which is the cost this whole project
exists to control.

### Collisions are real

`route.py` refuses to overwrite. One duplicate surfaced — the same rule in two stores with different
contents and no way to tell which was authoritative except by reading both. **Nothing detects this
automatically; a forked memory can drift indefinitely.** Resolve by hand, keep the newer, delete the
other.

---

## Step 5 — Rebuild the indexes

A moved file with no index line still *works* — recall matches on `description:` — but it can no
longer be found by browsing, which is how you notice a memory exists at all.

```bash
python3 make/memory-repair/mkindex.py /Users/carterking/Clients/outreach "Cold outreach engine."
```

**Only for stores you just rebuilt.** `mkindex.py` overwrites, so it will throw away hand-merged lines
and editorial ordering.

**For an always-loaded index — `MEMORY.md` in your main working directory — append by hand and merge
related entries onto shared lines.** Every line there is a permanent per-session token cost. The
2026-08-04 pass added 36 memories on 24 lines by grouping them. A topic file is free until recalled;
an index line is never free.

---

## Step 6 — Delete the dead stores

Only after `LEFT 0` everywhere.

Remove the leftover `MEMORY.md` and any derived files (`entities.json`, `mempalace.yaml`) **by explicit
name**, then `rmdir` the emptied directories. Enumerated deletion over recursive globs — narrower, and
it fails loudly if something unexpected is still in there.

**Check the parent directory before removing it.** `~/.claude/projects/<slug>/` also holds session
transcripts (`*.jsonl`). Those are history worth keeping; remove `memory/` and leave the rest. One
store in the 2026-08-04 pass had two transcripts, so its parent was correctly left in place.

---

## Step 7 — Verify

```bash
python3 make/memory-repair/audit.py
```

Clean means: every store resolves to a real directory, every index link resolves to a real file, and
every file appears in an index. Exit code `0`.

If a file is unindexed on purpose, add its name to `INTENTIONALLY_UNINDEXED` in `audit.py` — so that
the next real omission is not lost in a list of known ones.

---

## Gotchas, all of which cost time

- **Store names start with `-`.** Shell tools read them as flags. Use Python, or prefix paths with `./`.
- **zsh does not word-split unquoted variables.** A `for f in $LIST` loop moves zero files and reports
  success. Use an array: `KEEP=(a b c)` / `for f in "${KEEP[@]}"`.
- **`path` is reserved in zsh** and tied to `$PATH`. Assigning to it in a decode loop destroys the
  shell's PATH. Name the variable anything else.
- **`sort` needs `LC_ALL=C`** or it fails with "Illegal byte sequence" on some memory content.
- **A missing transcript does not mean a dead folder.** Deriving cwd from `*.jsonl` fails for old
  stores; that is why `audit.py` resolves against the filesystem instead.

---

## The general lesson

Every failure in this system's history — the stranded stores, the dead symlinks, the deny rules that
did nothing, a hook writing 145,000 characters into a file with no readers — is **a mechanism that
reports success and does nothing.**

That is why step 0 and step 7 are the same command, and why it has an exit code. **The repair is
worth less than the check.** A repair fixes today; a check that runs before and after every move is
what stops the next three years of silent drift.
