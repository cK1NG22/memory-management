# MAKE — mode principles

Loads when a session starts in a project's `make/` folder, from `make/.claude/rules/`.
Each project holds a copy of the mode library's file. Edit the library, then re-stamp; `modes.py
check` reports copies that differ.

## Building

- **Build incrementally — never scaffold-first then fill.** One piece deeply at a time: author it
  fully, prove it works, commit, review, then the next. Each stage ends with a working, committed,
  pushable artifact; onboarding docs (README, pattern catalogs) are Stage-1 deliverables authored
  before code; no sub-component ships without fixtures. A repo full of empty stubs hides unfinished
  work behind apparent completion.
- **Carter owns folder structure.** Don't scaffold directories on your own initiative — propose
  paths only as labeled strawmen and wait for his layout. Root-level single files drafted for
  review are fine.
- **Prototypes are experiments: keep an EXPERIMENT.md at repo root** (Hypotheses, Assumptions,
  Tests, Expectations, Limitations, Out of scope), numbered H1/H2/… each mapped to a concrete
  test, updated with verdicts as tests run — so versions are judged against stated hypotheses,
  not vibes.
- **Design tokens: zero hardcoded visual values.** Every color, font, size, spacing, dimension,
  transition, shadow, radius, z-index lives as a CSS variable in one central tokens file, wired
  into the Tailwind config; components reference `var(--token)` only. Token file first, before any
  components. A value used twice is a token.
- **Templates maximize structure.** When templating from an exemplar, keep known sentences as
  static scaffold text and tokenize only the genuinely variable spans (with grammar-constrained
  fill hints); reuse the same token everywhere a fact appears so the deliverable can't
  self-contradict. Never "write 2-3 sentences here" placeholders when the skeleton is known.
- **Skills need explicit knowledge maps.** Every skill step maps to the reference files carrying
  the principles needed at that step; err toward more reference files, over-documented beats vague.
  Process steps = what to do; reference files = how to think about it.
- **In code, the context7 lookup is per-call and per-version.** A lookup covers the call you looked
  up — the other five API calls in the same file are still memory. Read the version from
  `package.json`/lockfile and query that version's docs; answers differ across majors (AI SDK v4
  `maxSteps`/`parameters` → current `stopWhen`/`inputSchema`). A lookup after the code is written is
  a review, not a lookup.

## Repos and parallel work

- **Edit the dev clone, never the installed plugin copy.** Repos that exist under
  `~/.claude/plugins/marketplaces/` are live artifacts — the next auto-update GC-prunes local-only
  branches and unpushed commits unrecoverably. Work in the `~/Projects/` dev clone, commit, push;
  GitHub is canonical.
- **Parallel jobs editing one clone collide.** A shared checkout is single-writer: one job's
  `commit -a` sweeps another's in-progress files. Isolate before the first edit (EnterWorktree, or
  `git worktree add` inside the target repo). Recovery: don't rewrite the other job's commit while
  it's active — back up your files, re-apply in a clean worktree off main, and verify each piece is
  safe (`git merge-base --is-ancestor`) before deleting a tangled branch.
- **Python default-kwarg trap for production paths:** never bind a module-level Path constant in a
  function signature (defaults evaluate once, at import — `mock.patch.object` is silently
  bypassed and tests write to the real filesystem). Default to `None`, resolve in the body; tests
  assert the override took effect. Review smell: a test patches a module attribute that the code
  uses as a signature default.

## Automation and integrations

- **Every automation must be observable** — three questions it must answer: when did it last run
  (stamp `~/Claude/cron-scripts/last-run.json`), did it succeed (log to
  `~/Claude/cron-logs/{job}-{date}.log`), what did it produce (artifact under `~/Claude/`).
  Crons fail silently when the wifi's off; observability is what makes that visible.
- **Skill outputs write to `~/Claude/<skill-name>/`, never `~/Desktop/`.** New subfolders get added
  to `~/Claude/README.md`.
- **Headless Slack posting never uses the claude.ai Slack connector** — it holds one OAuth token
  for one workspace and reauth silently overwrites it (broke ~14 days of digests once). Cron/
  headless skills use the Slack Web API via curl with a bot token from Keychain
  (`security find-generic-password -s "<service>" -a "carterking" -w`); one bot token per
  workspace covers all its channels. Interactive connector use is fine.
- **No model names or availability claims in CLAUDE.md files** — they go stale fast and cause bad
  routing. Phrase model routing agnostically: "inherit the session model," "cheaper tier for
  mechanical phases."
- **Subagent model selection:** a well-scoped mechanical prompt (explicit file list, exact checks,
  hard scope boundary, success criteria, a template to copy) runs on a cheaper tier; genuinely
  exploratory or judgment-heavy work (audits, architecture, cross-cutting refactors, reviewers —
  a reviewer must be at least as strong as the builder) gets the strongest tier. Pre-launch check:
  does the prompt read "build X with these exact pieces" or "figure out how to X"?
