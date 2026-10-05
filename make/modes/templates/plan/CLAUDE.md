# Mode: plan

You are **deciding**, not investigating and not building.

## What this mode is for

Turning settled findings into a design, a sequence, and an explicit set of tradeoffs. The output is
something `make/` can execute without re-litigating it.

## How to work here

- **Sequence matters more than completeness.** A plan that cannot be finished is worse than a
  smaller one that can.
- **A migration that doesn't delete is an addition.** Every plan that moves something must say what
  gets deleted and how that deletion is verified.
- **Name the falsifier.** What result would mean this was wrong? If nothing would, it is not a plan.

## Where things go

`ROADMAP.md` (what's next) · `DESIGN.md` (the settled design) · `decisions/` (ADRs, when a choice
needs its own file). These are **present-tense and rewritten**. Anything past-tense and immutable
belongs in `../.claude/memory/decisions.md` instead.

**Write only inside `plan/`.** If something belongs in `research/` or `make/`, say so and stop.

## Mode principles

The rule files in `.claude/rules/` beside this file. They load when a session starts in this folder.
They are copies from the mode library; `modes.py check` reports any that differ.
