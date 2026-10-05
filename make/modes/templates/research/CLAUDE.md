# Mode: research

You are **investigating**, not deciding and not building.

## What this mode is for

Establishing what is true: sources, experiments, measurements. The output is a reference document
the next session can act on without re-deriving it.

## How to work here

- **Label every finding's provenance.** A reproducible experiment, a measurement of this machine, or
  a source with a URL and a date. Say which one you have.
- **Loading is not obeying.** Proving that text arrives in context proves delivery, not control. If
  the claim is about behavior, test the behavior.
- **Watch for circularity.** An argument that measures a proposal against a baseline the proposal
  would itself change is not an argument.

## Where things go

Findings land in `sources/` here. When a finding is settled enough to act on, it becomes a decision
in `../.claude/memory/decisions.md` and the design changes in `../plan/`.

**Write only inside `research/`.** If something belongs in `plan/` or `make/`, say so and stop.

## Mode principles

The rule files in `.claude/rules/` beside this file. They load when a session starts in this folder.
They are copies from the mode library; `modes.py check` reports any that differ.
