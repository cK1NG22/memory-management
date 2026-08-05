# Mode: research

You are **investigating**, not deciding and not building.

## What this mode is for

Establishing what is *true* about how memory, context, and loading actually work — by running the
experiment, not by reading the docs. Most of what this project knows was discovered by sentinel
strings in throwaway directories, and several documented behaviors turned out to be false.

## How to work here

- **Test the principle in isolation.** Build a synthetic throwaway tree and probe it. Do not apply an
  unrefined design to a real project and report what breaks — that answers a different question.
- **Label every finding's provenance.** A controlled experiment anyone could reproduce is not the
  same as a measurement of this machine. Say which one you have.
- **Watch for circularity.** An argument that measures a proposal against a baseline the proposal
  would itself change is not an argument. This has already happened once here.
- **Loading is not obeying.** Proving that text arrives in context proves delivery, not control.
  If the claim is about behavior, test the behavior.

## Where things go

Findings land in `sources/` here. When a finding is settled enough to act on, it becomes a decision
in `../.claude/memory/decisions.md` and the design changes in `../plan/`.

**Write only inside `research/`.** If something belongs in `plan/` or `make/`, say so and stop.
