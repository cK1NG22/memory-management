# Mode folders runbook

Rewritten 2026-10-04 when mode principles moved from `@import`-ed symlinks to rule files. The
previous procedure is `_archive/mode-files-runbook_2026-10-04.md`.

Use when stamping mode folders onto a project, sorting skills, agents and rules into them, or
changing a mode principle. The tool is `make/modes/modes.py`; the `/modes` skill
(`make/modes/SKILL.md`) walks the same steps and carries the sorting tests.

## The mechanics this rides on (probed on this machine — re-test after CLI upgrades)

| Fact | Probed |
| --- | --- |
| `<project>/<mode>/.claude/rules/` and `skills/` load only when the session starts in `<mode>/` | 2026-09-28, CLI 2.1.284, 2/2 runs |
| The same holds for `<mode>/.claude/agents/`; a root session and a sibling-mode session see none of the three | 2026-10-04, CLI 2.1.289, 1 run per launch folder |
| Rules skip symlinks — a linked rule file or folder silently never loads | 2026-09-28 |
| Skills follow symlinks; a dead link vanishes with no warning | 2026-08-07, 2026-09-28 |
| Symlinked agents load at the project level (not re-probed inside a mode folder) | 2026-09-29 |

All probes are headless (`claude -p`) with the model reporting whether a sentinel string is in
context. Full record: `reference-claude-code-loading-mechanics` in the native store.

## The shape

```
<project>/
  CLAUDE.md                     mode-invariant facts; loads in every session
  .claude/{rules,skills,agents} load in every session in the project
  research/
    CLAUDE.md                   thin: what this mode is for in THIS project
    .claude/rules/research.md   a real copy of the library rule
    .claude/skills/  agents/    load only in research/ sessions
  plan/  make/                  same
```

The source for mode rules is `make/modes/library/<mode>/rules/*.md`. Each project holds a copy.
A project rule with the same filename as a library rule is its copy; any other filename is a
project-only rule and is never compared or overwritten.

## Procedure

1. `python3 make/modes/modes.py stamp <project> --dry-run` — read every line.
2. `python3 make/modes/modes.py stamp <project>` — creates what is missing, keeps what exists,
   copies the rules, removes the old `<MODE>-MODE.md` symlink and its `@import` line, then checks.
3. Sort: `modes.py list <project> [--from ~/.claude]`, decide with the tests in the skill, then
   `modes.py place <kind> <name> <mode> --project <project>`.
4. Verify delivery once per project, and again after a CLI upgrade: from a mode folder,
   `claude -p "Is the phrase '<phrase only in that mode's rule>' in your context?"`.
5. `python3 make/memory-repair/audit.py` — its mode folder check runs `modes.py check` on every
   stamped project in the containers.

## Changing a principle

Edit the library file, then `modes.py stamp <project> --update` for each stamped project. Until
then `check` and `audit.py` name every copy that has fallen behind. A change made directly in a
project's copy is reported as a difference, never silently kept or silently overwritten.

## Failure modes

| Symptom | Cause | Caught by |
| --- | --- | --- |
| Mode rules silently absent | rule file or rules folder is a symlink | `check`: "is a symlink — it never loads" |
| Mode rules silently absent | session started at the project root, not in the mode folder | nothing — this is the design; launch in the mode folder |
| Two projects follow different principles | a copy drifted from the library | `check`: "differs from the library" |
| A skill or agent vanished | its link target moved or was deleted | `check`: "dead symlink" |
| Principles loaded twice | old symlink + `@import` left beside the new rule | `check`: "still imports" / "old symlink" |
| A skill stopped triggering at the root | it was moved into one mode folder | the `place` note; decide with sorting test 2 |

`check` proves the files are right. Only the step-4 probe proves a session reads them.
