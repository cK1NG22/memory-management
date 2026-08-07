# Skill budget A/B — does trimming the catalog restore evicted descriptions?

Claim under test: reducing the loaded skill catalog restores descriptions for skills that were
silently evicted. Source: `../research/sources/skill-description-drop.md`.

## Mechanism recap (binary-verified)
budget ≈ contextWindow × 4 chars/token × skillListingBudgetFraction (default 0.01 → ~8,000 chars
@200K). Non-bundled skills sorted by usage priority; overflow → bare `- name`, silent.

## Fixture — build fresh, don't reuse old fixtures
`~/Sandbox/skill-budget-ab-fixture/` — durable, inspectable, not `/tmp` (old bg-job fixtures
evaporate). Two subdirs, each its own project root:
- `baseline/` — no `.claude/settings.json` (or `{}`). Real global catalog, untouched.
- `subtraction/` — `.claude/settings.json` with `skillOverrides` (below).

## Arms
| Arm | Settings | Expected |
|---|---|---|
| A baseline | none | targets mostly bare (evicted) |
| B subtraction | `skillOverrides` → name-only on heaviest non-target skills | targets mostly full description |

## Subtraction settings — measured, not hardcoded
1. **Re-measure fresh.** The repo's 31,350-char catalog figure (`phase3.md`) is from 2026-08-05/06,
   pre-restructure — stale, do not reuse. For every non-bundled skill in every loaded dir
   (`~/.claude/skills/*`, plugin skill dirs), read SKILL.md frontmatter `name` + `description`,
   compute `len("- {name}: {description}")`.
2. Sort descending by that length.
3. Measure current budget: `200K × 4 × skillListingBudgetFraction` — read the fraction from
   settings if set anywhere, else default 0.01.
4. `deficit = total_catalog_chars − budget_chars`.
5. Walk the sorted list, accumulating freed chars, until `cumulative ≥ deficit`. Write
   `skillOverrides: {"<name>": "name-only"}` for exactly that set into
   `subtraction/.claude/settings.json`. Expect the file-type four (`xlsx`/`docx`/`pptx`/`pdf`) plus
   other verbose entries near the top — confirm from the sorted list, don't assume.
   **Never include the 4 target skills below in this set**, even if one measures heavy.

This is the strong form of the claim: after subtraction, remaining catalog ≤ budget, so nothing
*should* be evicted — a clean binary expectation, not a partial nudge.

## Targets + decoy
Targets (known-affected, from research doc): `sources-cited`, `tdd`, `sync-gbrain`,
`youtube-slide-transcript`. Decoy (hallucination control — does not exist): `zzz-fixture-decoy-99`.

## Probe
From inside each arm's directory: `claude -p --model sonnet "<prompt>"`.

```
For each of these skill names, report exactly what appears in your available-skills list right
now: the full description text if shown, "NAME-ONLY" if only the bare name appears, or "ABSENT"
if it's not listed at all. Do not guess or reconstruct a description from the name.
Names: sources-cited, tdd, sync-gbrain, youtube-slide-transcript, zzz-fixture-decoy-99.
Answer as a table: name | status | description (if any).
```

5 probes per arm (10 total) — session-to-session variance makes single probes unreliable. Discard
any probe where the decoy gets a fabricated description (hallucination, not signal).

## Success criterion
`restoration rate` = (target×probe pairs showing full description) / (valid target×probe pairs).
**Confirmed if:** baseline ≤ 20% AND subtraction ≥ 80% (delta ≥ 60pp).

## Falsifier
- delta < 60pp → budget model wrong, or freed chars insufficient this run
- both arms ≥ 80% already → no eviction present this session (variance) — rerun once a baseline
  probe shows real eviction, don't conclude the model is wrong from this alone
- > 20% of probes have decoy hallucination → probe method unreliable, fix prompt, re-run before
  drawing any conclusion

If falsified: do not act on the trim/relocation plan items on this basis. Re-open the mechanism in
`research/` before touching any real skill file.

## Cost
10 headless `claude -p --model sonnet` calls, single-turn, ~8-10K input tokens (catalog) each,
<200 output tokens each. Negligible — well under $1 total.

## Cleanup
`rm -rf ~/Sandbox/skill-budget-ab-fixture/` — nothing else touched: no `~/.claude/settings.json`,
no real skill files, no `~/.claude/skill-usage.json`.

## Results
Append `## A/B test — <date>` to `../research/sources/skill-description-drop.md`: arms, measured
deficit/freed chars, per-target restoration table, verdict, link back to this file.
