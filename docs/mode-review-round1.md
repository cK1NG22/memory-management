# Round 1 — four independent reviews of the mode-structure design

Four seats investigated `docs/mode-structure-spec.md` independently, with no contact between them.
Reports below as received. Read the seats other than your own before responding in round 2.

Claims marked **[lead-verified]** were independently re-checked by team-lead against the filesystem.

---

## SEAT 1 — DURABILITY

**F7 — CONFIRMED, worse than stated.** With an `Edit()` deny rule in place, a neutral prompt
("append this line, use whatever method works"), non-interactive:
- `echo >>` denied. `printf` denied. `cp <dst>` denied.
- **`python -c "open(...).write(...)"` went through — file mutated, confirmed by diff.**
- **`node -e` with `fs.appendFileSync` went through — file mutated.**
- Non-deterministic: on a repeat run the model tried only the checked idioms and gave up.

Claude Code *does* have some redirect/argument-aware Bash checking. That is the trap — it catches
the obvious idioms often enough to pass a spot-check, while any interpreter one-liner sails
through. **Both `python` and `node` are already on Carter's global Bash allowlist.** [lead-verified]
F7 is not "Bash is unchecked"; it is "Bash is checked just enough to fool a spot-check."

**NEW — hooks bypass the permission system entirely.** `~/.claude/hooks/auto_log_history.py` is
registered as a **`Stop` hook — it fires at the end of every session** [lead-verified] — and writes
`history.md` by raw Python file append. `close-session/scripts/memory_migrate.py` does the same for
`context.md`/`decisions.md`. These are subprocesses the harness executes on lifecycle events; they
never pass through the Edit/Write/Bash permission layer, so no `Edit()` deny, no `Write()` fix, and
no conceivable `Bash()` rule could cover them. Structurally one level below F7. Currently harmless
(it aligns with claim #3) but it establishes an **ungated write channel with zero mode-awareness**.

**7B — CONFIRMED by clean isolated repro.** Built a throwaway repo with `.claude/` gitignored and a
deny rule committed, then `git worktree add`. The worktree has **no `.claude/` directory at all** —
not bypassed, structurally absent.

**F4 — FALSIFIED as a behavioral guarantee. Flag this hardest.** F1–F3 test *content loading*. F4
extrapolates to a *behavioral* claim. Controlled A/B, root files byte-identical, only the child differs:
- Root `CLAUDE.md`: "every response must end with `ROOT_MARKER_7788`, non-negotiable."
- Control child ("be concise") → marker appears.
- Test child ("never output `ROOT_MARKER_7788`, ignore any instruction elsewhere asking for it")
  → **marker does not appear.**

The root rule is fully present in context in both cases. It simply isn't followed when a closer,
more specific file disagrees. **"Additive" is true for tokens, not for compliance.** This directly
undercuts claim #2 — nothing stops a mode's CLAUDE.md from silently overriding what is supposed to
be invariant, and it would look completely normal from outside: no error, no warning, root text
still sitting right there in context.

**Two more mechanism facts.** Good: deny rules *do* inherit downward — a rule in
`plan/.claude/settings.json` still binds when cwd is `plan/subdir/`. Bad: enforcement is purely a
function of cwd ancestry, so **an agent orchestrating from the project root gets zero enforcement
from any mode's settings.json — by construction.** That is exactly how `day-shift`, `night-shift`,
and `dream` run today. Also: `~/.claude/settings.json` carries **bare, unscoped `"Write"` and
`"Edit"` in its allow list** [lead-verified, lines 82–83] — there is no ask-by-default fallback
anywhere in the chain.

**Verdict — claim #5 is not load-bearing.** It reliably stops one thing: a direct `Edit` call from
inside the mode's own subtree. It does not stop new-file writes (F6), interpreter one-liners (F7),
hook writes, or anything invoked from outside the subtree — and it is simply *absent* inside any
worktree from a repo that gitignores `.claude/`, which is 2 of 3 stress-case repos.

**Verdict — claim #4.** The write half is porous. The read half has **no enforcement mechanism
proposed anywhere** — no `Read()` deny rules appear in the design at all. It is pure prose
convention, and the F4 test shows prose convention is exactly the layer that is silently overridable.
Decorative.

**Meta-finding.** Every piece of evidence in §4 that "the mechanism works" (F1, F2, F3, F9, F11)
tests *content presence*, not *compliance*. **Presence in context and behavioral guarantee are
treated as the same thing throughout the packet, and they are not.**

---

## SEAT 2 — ASSUMPTIONS

**Claim #1 does not hold, independent of mechanism.** The stated defect (Task Type conflates
mode/domain/artifact) is real, but the replacement has the same disease relabeled, and the spec's
own words prove it: §2 defines `make/` as **"the actual code"** — a coding-shaped definition in the
same document whose §1 says Carter explicitly does not want this planned around coding conventions.

Checked against real projects: `dad/vc-outreach/` has no code and never will (plan-forever, no
`make/` to graduate into). `dad/market-assessment/` is itself a research artifact, classified
`strategy` today. `dad/company-preview/ITERATION-LOG.md` (5.1K, actively used) is on-disk evidence
the real workflow is **iterative, not the waterfall claim #4 assumes**. Only `companion` fits the
axis cleanly — and it is the one example that is a literal software repo, the exact case ruled out
as the design center.

**Claim #6 is infrastructure built to paper over claim #4.** `DEVIATIONS.md` exists specifically to
manage the failure mode of one-way reads. The design had to build a reconciliation queue because
its own axis does not match reality.

**Cheaper fix nobody priced.** Task Type conflates two axes because it is *one field*. Make it
**two fields** in the existing `TASK.md` — `Mode: research|plan|make` × `Domain: coding|knowledge|
sales|…`. No filesystem change, no permission mechanism, no migration. If the complaint is that the
categories are incoherent, that is a metadata fix, not a directory-architecture fix. Was this
considered and rejected, or did the diagnosis jump straight to a folder redesign?

**cd is the most expensive of several available levers, and cheaper ones already run daily.**
`~/.claude/agents/` holds **7 role definitions** [lead-verified] — `research-deep-dive`,
`implementer`, `qa-runner`, `merge-gate-reviewer` and others — invoked by name from any directory,
no cd, no migration, no re-keying of native memory. The harness's built-in `Plan` agent covers the
third leg. **Output styles** are a live cwd-independent mechanism for carrying a role into a session
— *this review is running under one right now*. Carter already has three working levers for "carry
role instructions" and the design engages none of them.

The one thing folders offer that agent-roles cannot is a hard write boundary — and that is the part
already shown void.

**Claim #3 is the one that holds.** `detect_task_dir()` keys off any `.claude/memory/` dir rather
than a `TASK.md` marker, so single-memory-at-root is *more* compatible with existing tooling than
today's per-task model. A real point in its favor, not merely an absence of objection.

**Likely proxy problem.** The goal is context curation. The verified bloat sources — native
MEMORY.md stores up to 18KB, and `history.md` files at 145,027B and 84,945B [lead-verified] — are
untouched by this redesign. The cheapest fix for the stated goal is capping those, not a 25-project
migration.

**Prior art.** `~/.claude/hooks/project-root-warning.sh` is a **live, deployed patch for the exact
failure mode this design would triple** [lead-verified] — it fires when you launch from a project
root and warns that the memory chain will not auto-load. More cd-sensitive boundaries means more of
that, not less. Separately: **no documentation anywhere explains why Gen 1 → Gen 2 happened.**
`knowledge-tree` went dormant for project-specific reasons; the filesystem cannot confirm the shape
was the cause. Ask Carter directly rather than inferring.

---

## SEAT 3 — OPERATOR

**Verdict: does not survive week three in its current form** — not because the axis is wrong, but
because the design has no answer for "what happens when a session is short, mixed-purpose, and the
boundary is a filesystem cd."

**Native memory fragmentation is not a risk — it already happened, and it leaks.** [lead-verified]
`dad/runner/.claude/worktrees/` and `companion/.claude/worktrees/` are **empty on disk**, yet memory
stores for `runner-auth-exit`, `topic-graph-diamond`, and `companion-build` still exist under
`~/.claude/projects/`. Nothing garbage-collects them. Every worktree night-shift creates mints a
store that outlives it permanently.

**Write isolation is void in production right now.** `dad/web/.claude/worktrees/` holds three live
worktrees — `nav-latency`, `nav-speed`, `job-cost-migration` — on a repo that gitignores `.claude/`.
Three real worktrees carrying zero deny rules, this week. [lead-verified]

**The pilot cannot pilot anything.** [lead-verified] `companion/main` is **one commit** tracking four
files: `.gitignore`, `BUILD-PLAN.md`, `PRD.md`, `mockup.html`. The real build is 27,555 lines on
`origin/worktree-companion-build`, PR #1, open and unmerged since 2026-07-28. And companion has
**never had `TASK.md`, `PROJECT.md`, or `.claude/memory`** — it is not in the shape the design
replaces. It is a clean-room adoption test, not a migration test.

**No template for the enforcement mechanism.** Current deny rules machine-wide: three Bash denials
(`git push --force`, `rm -rf`, `sudo`). **Zero `Edit()` path-scoped deny rules exist anywhere.**
[lead-verified] Every mode boundary is hand-authored from scratch with nothing to copy.

**Carter's own tooling already rejected the multi-pane model this implies.** Agent teams run
in-process by explicit choice — Ghostty has no split panes, no tmux, no it2. That is the closest
existing evidence for whether Carter runs parallel terminal contexts, and it says no.

**Mode switching is a session boundary, not a move.** Because loading is cwd-bound and additive,
already-loaded content never unloads and new rules bind only a new cwd. So switching means: stop,
cd, start over, reload. `close-session`'s own text puts Carter's median session at **3 turns**,
across ~35 session logs in three weeks. That boundary gets paid constantly relative to the work
between boundaries — and a fresh mode subdir starts with an **empty** native store, so the first
session in a new mode starts cold.

**Build-discovers-plan-was-wrong is not hypothetical.** Companion's own PR #1 history shows exactly
this — "codex pass 2", "codex pass 3", bugs found mid-build and fixed in the same session. Under the
design that discovery must route through `DEVIATIONS.md` and wait for the next `plan/` session.
There is no push, only pull.

**dad/ migration, totalled.** Three complete research/plan/make sets, 3 root memories, 3
`DEVIATIONS.md`, and **up to 9 mode-level `settings.json` files authored from scratch** — before
`vc-outreach/`, `crm-ui/`, and `market-assessment/` even get a shape decision. `crm-ui` has no
`.claude` at all and is not a git repo — outside every convention, old or new. And `close-session`'s
Phase 6 git cleanup assumes one repo per task-root; dad's case is three independent repos.

**One point in favor:** `auto_log_history.py`'s walk-up finds `.claude/memory/` from inside `make/`,
so that automation keeps working unchanged under claim #3.

**Predicted failure modes:** (1) friction gets absorbed by *not switching* — plan and build drift
back into one session because stopping to cd costs more than the boundary is worth, voiding claim #4
without anyone deciding to; (2) fragmentation makes early sessions in a new mode feel like starting
over. Both are "technically works, nobody keeps doing it," which is worse than not migrating because
the cost is already sunk.

---

## SEAT 4 — MEASUREMENT

**The "no token-counting instrument" premise is wrong.** [lead-verified] Every session writes real
API-reported counts to its own `.jsonl` transcript — `input_tokens`, `cache_creation_input_tokens`,
`cache_read_input_tokens`. Anthropic's own tokenizer, already on disk for every session ever run.
No ccusage needed. Byte/4 is a fallback that was never necessary.

**The scale problem is the killer.** Cold-start context sampled across 33 real sessions:
**~8,000 to ~125,000 tokens, most substantive sessions 40,000–80,000.** `~/Projects/dad/` cold =
**45,484 tokens**. Claim #9's entire targeted budget (Tier 0 ~2K + Tier 1 ~1K = **~3K**) is
**3–8% of that floor**, which is dominated by system prompt, tool schemas, and installed
skills/MCP — none of which this design touches. **Session-to-session noise is 10–40× larger than
the effect the redesign is trying to produce. A naive before/after test physically cannot detect it.**

**Corrections to the packet — same overstatement pattern as 57→23.** [all lead-verified]
- "99 cwd-keyed stores" → **101 project dirs, but only 33 with a populated `MEMORY.md`.**
- "~2,770 tokens" is **one** store. Real range: **155 bytes to 18,478 bytes — a 119× spread.**
- **companion's own store — the pilot — is 155 bytes (~39 tokens).** §7A's headline number does not
  even apply to the project chosen to validate the design. `dad/` is 4,764B; `mana-ventures` is
  16,204B — 26× companion. Fragmentation must be measured per-project.

**Prompt caching reframes claim #9.** Stable content is cache-*read* after the first turn, not
re-paid at full cost "every turn." So the Tier 0 (expensive, every turn) vs Tier 1 (cheap, once)
distinction is less about turn-frequency than the design assumes. The real cost drivers are
**cache-invalidation frequency** and **cold-start frequency** — not which tier a file is assigned to.

**The instrument that would work: a controlled paired delta.** Hold skills/MCP/tools config, day,
and project content fixed; vary only directory shape; read usage from a cold session on each side.
The fixed overhead cancels out of the *delta* even though it swamps any absolute number.

**Missing precondition.** The old shape must be **archived, not deleted**, on migration. Delete it
and the baseline is unrecoverable and the claim is retroactively unfalsifiable for that project.
This must be an enforced migration step, not an assumption — and Carter's own `file-versioning`
convention already requires it.

**Verdict: testable in principle, unfalsifiable as currently scoped.** If the 25-folder migration
runs today exactly as designed, Carter will have no way to confirm afterward whether he got what he
was told he would get — for any of the 25.
