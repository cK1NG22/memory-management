# RESEARCH — mode principles

Loads when a session starts in a project's `research/` folder, from `research/.claude/rules/`.
Each project holds a copy of the mode library's file. Edit the library, then re-stamp; `modes.py
check` reports copies that differ.

- **Research isn't done until it's a reusable reference doc.** Every research phase produces a
  standalone markdown deliverable, named plainly by topic, then wired into the skills/projects that
  need it (ask "which skills or projects should this be wired into?"). Knowledge that only lives in
  a conversation evaporates.
- **Independent verifier.** Never let the agent that produced research grade it. Spawn the
  verification pass on a separate agent (a different model), framed as "grading someone else's
  work." Verification moves confidence in both directions — it catches misses *and* upgrades
  over-conservative scores.
- **Parallel researchers with strong planning and synthesis.** For research spanning ≥4 independent
  targets (or broad surveys): plan heavily upfront (detailed self-contained sub-agent prompts with
  explicit output schemas, source URL + date on every factual claim), fan out cheaper parallel
  sub-agents one slice each in a single message, then synthesize centrally — cross-check
  disagreements and flag inter-agent contradictions rather than silently resolving them.
  Single-target research doesn't trigger this; one agent or inline search is fine.
- **Research-spike cards: L0/L1/L2 shape + explicit kill criteria.** Overnight/unattended research
  cards specify (1) the house L0/L1/L2 output shape, (2) the output filename, and (3) kill criteria
  naming both the stop condition and the tempting next step NOT to take. This shape has produced
  merge-ready unattended results with zero rework.
- **The root page is navigation, not specification.** In any structured system (wiki, Notion space,
  codebase), search for the versioned spec/architecture/schema doc *before* trusting the landing
  page's prose — the canonical spec is usually buried (a database row, an ADR). A casual root-page
  mention that surprises you is a signal a spec doc elaborates on it. Capture spec-doc URLs so the
  search isn't repeated.
- **context7 output is a source; cite it like one.** Library and API claims carry the context7
  library ID and version (`/vercel/next.js`, v15) the same way a web finding carries its URL and
  date. If context7 has no entry, the claim is labeled model knowledge, not a finding.
- **When a finding is a count, the unit and the labels ARE the finding.** Two failures, opposite
  directions, both real in `2026-08-12-company-report-examples`. *Inflation:* count independent
  voices, not documents — 8 CFA Research Challenge reports share one mandated rubric, so they are
  one vote on structure, not eight, and any corpus assembled by ease-of-collection over-samples
  whoever publishes most freely (collection ease is *inversely* correlated with independence).
  *Deflation:* normalize every axis you count on, not just the convenient one — merging metric
  synonyms but not section-heading synonyms split one section across six house names and produced
  a confident "there is no standard structure" that was simply wrong (3/18 → 9/18 once fixed).
  **A negative finding deserves more scrutiny than a positive one: insufficient normalization is
  indistinguishable from absence of evidence.**
- **Testimony beats description, and our own files are never evidence about the outside world.** When
  the question is how something actually works or what an experience is really like, weight first-hand
  accounts from people who did it above any material that merely describes it — and never cite our own
  saved study material, notes, or scraped copies as evidence about the thing they describe. Two traps
  make this sharper than it sounds. *Downstream copies masquerade as corroboration:* a community site
  whose numbers match the official document exactly proves only that it copied correctly; agreement is
  evidence only when the sources could have been derived independently. *New topics attract synthetic
  testimony:* within weeks, AI-written "I did it!" affiliate posts outnumber real accounts, so each
  claimed first-hand account needs a refutation attempt (does this person name a score, a date, a
  price, a specific complaint?), not just a relevance check. Prefer failure reports — they name the
  real constraints, where success stories mostly describe prep that happened to work.
- **Test principles, not projects.** When evaluating a proposed design, test its principles in a
  clean, isolated setting (throwaway dirs, sentinel strings, controlled A/B) — never by applying
  the unrefined design to an existing project and reporting what breaks. Label every finding with
  its provenance: reproducible experiment vs. measurement of this machine's current state. Watch
  for circularity: an argument that measures a proposal against a baseline the proposal would
  itself change is not an argument.
