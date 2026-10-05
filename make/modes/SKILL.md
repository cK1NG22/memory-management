---
name: modes
description: Give a project research/ plan/ make/ mode folders and sort its skills, agents and rules into them. Use on "/modes", "scaffold mode folders", "stamp this project", "sort these skills into modes", "check the mode folders".
disable-model-invocation: true
---

# Modes

Stamp mode folders onto a project, sort skills, agents and rules into them, and check that
everything placed there actually loads.

`modes.py`, `library/` and `templates/` sit beside this file. Call the script by its full path:
`python3 <this skill's folder>/modes.py …`. It never needs the project to be the current directory.

## What loads where

| Placed in | Loads when |
| --- | --- |
| `~/.claude/{rules,skills,agents}/` | every session, every project |
| `<project>/.claude/…` | every session in the project, mode folder or not |
| `<project>/<mode>/.claude/…` | **only** when the session starts in `<mode>/` |

Two facts decide how an item is placed (both probed on this machine, 2026-09-28 and 2026-10-04):

- **Rules skip symlinks.** A linked rule file or folder never loads, with no warning. Rules are
  always real copies. The cost is drift, which `check` reports.
- **Skills and agents follow symlinks.** Link them from wherever they live so they keep tracking
  their source. A dead link vanishes with no warning, which `check` also reports.

## 1. Stamp

```
modes.py stamp <project> --dry-run     # show every change first
modes.py stamp <project>               # apply, then check
```

Show the dry run and get a yes before applying. The stamp:

- creates `research/`, `plan/`, `make/` with a `CLAUDE.md` each, plus the root `CLAUDE.md`,
  `TODO.md`, `.gitignore` and `.claude/memory/` — **existing files are kept, never overwritten**;
- copies each library rule to `<mode>/.claude/rules/`;
- removes the old wiring if present (the `<MODE>-MODE.md` symlink and its `@import` line).

A rule copy that differs from the library is reported, not overwritten. Read the difference before
choosing: a project edit worth keeping belongs in the library (edit it there, re-stamp every
project) or in a separately named project-only rule file. `--update` overwrites the copy.

If the project is not a git repo, say so and stop before the first session: native memory keys to
the git root, and without one each mode folder gets its own separate store.

After stamping, fill the placeholders: the paragraph at the top of the root `CLAUDE.md`, and the
"What this mode is for" section of each mode `CLAUDE.md`, in the project's own terms.

## 2. Sort

```
modes.py list <project>                          # what the project holds, by where it loads
modes.py list <project> --from ~/.claude         # plus candidates from another .claude folder
```

For each item, work out where it should load. Do not sort by name or by guess: read the item's
description (and its body when the description is thin) and apply these tests in order.

1. **Would it still be true or useful if this project were deleted, in every project?** It stays
   global. Do not place it.
2. **Is it needed in sessions at the project root, or in two or more modes?** It stays at (or goes
   to) the project root `.claude/`. A skill or agent may instead be linked into each mode that
   needs it; a rule may not, because every copy is another file to keep in step.
3. **Otherwise, which activity does it serve?**
   - establishing what is true — sources, probes, verification of findings → `research`
   - deciding — scope, sequence, tradeoffs, specs, test plans → `plan`
   - building and proving it works — code, tests, review, release, automation → `make`
4. **Nothing fits, or no session has used it?** Leave it where it is and say so. An unsorted item
   costs nothing new; a wrongly sorted one disappears from the sessions that needed it.

Weigh the cost while sorting. Every rule placed in a mode is read in full by every session in that
mode. Every skill adds its description to a listing with a fixed budget, and the overflow loses
its description silently — so a mode with fewer, sharper skills triggers better than a full one.

Present the result as one table — item, kind, where it loads now, where it would load, the test
that decided it — and get a yes on the table before moving anything. Then place each item:

```
modes.py place skills <name> <mode> --project <project>                    # in-project: moves it
modes.py place agents <name> <mode> --project <project> --from ~/.claude   # outside: links it
modes.py place rules  <name> <mode> --project <project> --from ~/.claude   # outside: copies it
```

Defaults: an item already inside the project is **moved**; one from outside is **linked** (skills,
agents) or **copied** (rules). `--move`, `--link`, `--copy` override; linking a rule is refused.
`<mode>` may be `root` to send an item back to the project root. Add `--dry-run` to preview.

Moving an item out of the project root removes it from root sessions and from the other modes.
Name that in the table for any item currently loading at the root.

## 3. Check

```
modes.py check <project> [<project> …]
```

Exit 0 means: every mode folder exists with its `CLAUDE.md`, every library rule is present as a
real file matching the library, nothing in a rules folder is a symlink, no skill or agent link is
dead, and none of the old wiring is left. Run it after stamping, after sorting, and after editing
the library.

`check` proves the files are right, not that a session reads them. After the first stamp of a
project, or after a Claude Code upgrade, confirm delivery once: start a headless session in a mode
folder and ask whether a phrase that exists only in that mode's rule is in context.

```
cd <project>/make && claude -p "Is the phrase '<phrase from make.md>' in your context? PRESENT or ABSENT."
```

## The library

`library/<mode>/rules/*.md` is the source for mode rules. Edit a principle there, then re-stamp
each project with `--update`; `check` names every project copy that has fallen behind. A project
rule whose filename matches a library rule is that rule's copy. Any other filename is a
project-only rule: never compared, never overwritten.
