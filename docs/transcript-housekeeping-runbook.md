# Transcript housekeeping — runbook

**Written 2026-08-06**, the day the procedures were first executed (46 dirs / 294 MB archived,
83 items consolidated, zero memory touched). This is the seed for a future skill or dream-process
agent. Tools live in `make/memory-repair/`; every mechanism below was sentinel-tested that day —
see `research/sources/native-memory-keying-and-symlink-experiments.md`.

## The facts everything rests on (all tested)

1. **Transcripts key to the exact folder a session was launched in.** Every distinct launch cwd
   gets its own `~/.claude/projects/<encoded-path>/` dir, forever. Memory converges to the git
   root; transcripts never converge.
2. **A transcript dir holds only three kinds of things:** session `*.jsonl` files, UUID-named
   per-session workspace folders (subagent transcripts), and sometimes `memory/` — the store.
3. **Transcript files are portable.** A `.jsonl` moved by hand into another store dir resumes
   with full recall. **Resume-by-id is global** (searches all of `~/.claude/projects/`), so dir
   placement affects only the per-folder interactive resume picker.
4. **A session's transcript follows it into a worktree.** `EnterWorktree` mid-session relocates
   the live `.jsonl` to the worktree-keyed dir.
5. **The encoded names are lossy** (`/` and `.` both become `-`), so never decode by string —
   resolve against the real filesystem (`audit.py`'s `resolve()`).

## Procedure A — sweep dead transcript dirs

*When:* after deleting worktrees or folders; candidate for a dream-cadence cron.

1. `python3 make/memory-repair/transcript_sweep.py` — read-only report: dirs whose decoded
   working directory no longer exists.
2. Re-run with `--archive` — moves them to `~/Claude/_archive/projects-transcripts_<date>/`.
   **Archive, never delete** (file-versioning convention).
3. Guard built in: any dir containing `memory/` files is untouchable, ever.

## Procedure B — consolidate deep transcript dirs

*Rule (Carter, 2026-08-06; corrected same day to include container level):* sessions are launched
at `<container>/`, `<project>/`, or `<project>/<mode>/`; anything keyed deeper than project folds
up into the project-level dir. Container- and project-level dirs are left alone; mode-level dirs
(`<project>/research|plan|make`) stay.

**Known limit:** the tool assumes projects sit exactly at `<container>/<project>/`. A *nested*
project (e.g. `~/Sandbox/builds/velocity`) looks "deep" to it and would fold up wrongly — review
the dry run for nested projects before every `--execute`.

1. `python3 make/memory-repair/transcript_consolidate.py` — dry run; prints every planned move.
2. Review, then re-run with `--execute`.
3. Built-in safeties: skips dirs with write activity in the last hour (a live session may be
   writing); moves everything except `memory/`; removes source dirs only when empty; containers
   recognized: Projects, Sandbox, Clients, Optimal, School, Research, Vault.

**Ordering rule for worktrees:** consolidate **before** deleting a worktree. While the worktree
exists, its transcript dir resolves and folds up into the project (kept). After deletion it is a
dead dir, and the sweep will *archive* it instead. Fold first if the log should be kept.

## Procedure C — move a single session by hand

1. Move the `.jsonl` **and** the UUID-named folder that shares its session id, together.
2. Never move a `memory/` folder as part of transcript work.
3. Never move a file from a session that may still be running (check mtime).

## Verification — after any of the above

- `python3 make/memory-repair/audit.py` → must exit 0 (24 stores / 315 topics baseline 2026-08-06).
- `python3 make/memory-repair/transcript_sweep.py` → "0 dead transcript dirs".
- The failure mode of this whole domain is **silence** — a wrong move produces no error, just an
  invisible file. The checks are the procedure; the moves are the easy part.

## Not yet captured here

- **Memory-store consolidation** (routing container-store topics into project stores) — a
  different, higher-stakes procedure with its own runbook base: `docs/memory-repair-runbook.md`
  (`dump.py` / `route.py` / `mkindex.py`, explicit manifests, `LEFT 0`). To be executed and
  captured in the next session; the routing rules are in `plan/mode-memory-design.md`.
- **Skill/agent packaging** — when this graduates into the dream process: dream *proposes* moves
  and reports; it never moves silently. The dry-run-by-default tools are built for exactly that.
