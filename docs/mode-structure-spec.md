# Mode-based project structure — spec under review

> **Read this first.** This document was written by the person who designed the thing it
> describes. Its framing is not neutral: it will present the design well and is likely to
> under-weight exactly the parts the author is least sure of. Treat every claim below as a
> proposal to be attacked, not a decision to be refined.
>
> **You will not be given the conversation that produced this.** That is deliberate. It contains
> the designer's reasoning chain and conclusions, and reading it would anchor you to them — which
> defeats the reason you were hired. **The ground truth for this review is the filesystem**, and
> you can read all of it yourself.
>
> **One exclusion, for that same reason: do not read `~/.claude/plans/`.** A planning document
> there contains the designer's full reasoning chain and the arguments already made for and
> against each claim. It is exactly the anchoring input this review is structured to avoid, and it
> is findable — so the exclusion has to be stated rather than assumed. Everything else on the
> filesystem is fair game. If you find yourself reaching for it, that is the signal that the packet
> is missing something; say what you needed and reason without it.

**Status:** draft under adversarial review · **Date:** 2026-08-04 · **Owner:** Carter

---

## 1. The problem this claims to solve

Carter's projects today use a "container + task" shape: a project folder holds `PROJECT.md`, and
one or more task subfolders each hold a `TASK.md` declaring a **Task Type** from a fixed list
(`knowledge | coding | skill | strategy | sales | marketing | documentation`). Reusable
per-type instructions live globally at `~/.claude/task-types/<type>/`.

The stated defect: that list conflates three unrelated axes. `coding` is a *mode of work*,
`knowledge` is a *domain*, `documentation` is an *artifact type*. No task can honestly pick one.

The stated goal is **context curation** — controlling what lands in the model's context window —
and Carter has said explicitly he does **not** want this designed around traditional coding
conventions.

## 2. Proposed shape

```
~/Projects/<project>/
├── CLAUDE.md              # WHAT this project is. Mode-invariant only. Tiny.
├── .claude/memory/        # ONE memory per project: context.md, history.md, decisions.md
├── DEVIATIONS.md          # reconciliation queue — belongs to neither mode
├── research/   { CLAUDE.md, .mode -> ~/.claude/modes/research, source material }
├── plan/       { CLAUDE.md, .mode -> …, README.md, CHARTER.md, phases/, decisions/ }
└── make/       { CLAUDE.md, .mode -> …, the actual code }
```

A **container level** (e.g. `dad/`) is optional — used only when unrelated efforts share a
stakeholder. The **mode level is claimed to be universal**.

## 3. The ten claims

Each is a separate target. Attack them independently; they do not all stand or fall together.

| # | Claim |
|---|---|
| 1 | `research → plan → make` is the right axis, replacing Task Type |
| 2 | Project-root `CLAUDE.md` holds only mode-invariant facts; mode `CLAUDE.md` holds the role |
| 3 | Memory lives **once** at the project root, not per mode |
| 4 | Reads flow **backward only**; each mode writes only to itself |
| 5 | Write isolation is enforced by `Edit()` deny rules in each mode's `.claude/settings.json` |
| 6 | `DEVIATIONS.md` at project root is the reconciliation queue, read by `plan/CLAUDE.md` on entry. No task system is built |
| 7 | PRDs split along the existing **L0/L1/L2** convention: `CHARTER.md` (L0) + `phases/NN-*.md` (L1) + `decisions/ADR-*.md` (L2), each phase file independently readable |
| 8 | `plan/README.md` is a **visitor guide** for agents arriving from another mode, succeeding by minimizing how much they read |
| 9 | Loading tiers with budgets — **Tier 0** (CLAUDE.md chain + `@imports`, every turn) ~2K tokens; **Tier 1** (`context.md`, session start) ~1K; **Tier 2** (on demand) unbounded |
| 10 | Cross-project mode instructions live at `~/.claude/modes/<mode>/INDEX.md`, reached by **symlink + relative `@import`** |

## 4. Findings from empirical test — verify, don't assume

These were established by running real headless sessions. **They are claims, not facts.** Each has
a one-line reproduction below. Re-run any you doubt; do not accept any on authority.

| # | Claim | How to falsify |
|---|---|---|
| F1 | `CLAUDE.md` **and** `.claude/CLAUDE.md` both load, at every level from cwd up to the filesystem root | Put a unique sentinel string in each; `cd` to the deepest dir; `claude -p "list any SENTINEL_ strings in your instructions"` |
| F2 | A **git repo boundary does not stop** the upward walk | Same tree, `git init` the leaf, re-run |
| F3 | CLAUDE.md files *below* cwd do not auto-load | Add one in a child dir; confirm its sentinel is absent |
| F4 | Therefore **going deeper is strictly additive** — a child CLAUDE.md cannot remove a parent's rule | Derived from F1–F3, not directly tested. **This one deserves scrutiny.** |
| F5 | `Edit()` deny rules in `<dir>/.claude/settings.json` block cross-directory writes; path form `//abs/path/**` | Deny rule + `claude -p --permission-mode acceptEdits "write to ../other/x.md"`; check file unchanged |
| F6 | **`Write(path)` deny rules are silently ignored.** Only `Edit()` is checked, and it covers all file-editing tools | Use a `Write()` rule instead of `Edit()`; Claude Code emits a warning and does not enforce |
| F7 | **Bash bypasses `Edit()` deny** — the matcher sees a command string, with no file path to match | Structural, derived from the permission model. *Not* directly demonstrated — two attempts were declined by the model on judgment grounds, so **this is the weakest link in the evidence and should be nailed down** |
| F8 | Carter's global allowlist already pre-approves `Bash(echo *)`, `Bash(printf *)`, `Bash(python *)`, `Bash(node *)` — all universal write primitives | `grep -n "Bash(" ~/.claude/settings.json` |
| F9 | `@import` in CLAUDE.md expands **relative paths only** | Sentinel file + `@relative/path.md` → expands |
| F10 | **`@import` with absolute or `~/` paths silently expands nothing** | Same sentinel via `@/Users/...` and `@~/...` → absent, no warning |
| F11 | `@import` **through a symlink works**, which is the proposed workaround for F10 | `ln -s` a dir, then `@symlink/file.md` → expands |
| F12 | No Bash sandbox is configured anywhere in Carter's settings | `grep -ri sandbox ~/.claude/settings*.json` |

**F7 and F4 are the two claims resting on reasoning rather than a clean demonstration.** If the
design's write-isolation story is wrong, it is most likely wrong there.

## 5. Ground truth — read these yourself

Paths, not contents. Pull what your own lens needs.

**The mechanism**
- `~/.claude/settings.json` — global permissions, allowlist, env
- `~/.claude/CLAUDE.md` — always-loaded global instructions (part of the Tier 0 budget)

**What the design would replace**
- `~/.claude/skills/restructure-project/` — SKILL.md + nine templates, builds today's shape
- `~/.claude/skills/new-project/` — the code-conventions half
- `~/.claude/task-types/` — five of seven type folders exist

**The integration surface — 23 unique live files**
- 19 reference `.claude/memory` · 15 reference `TASK.md`/`PROJECT.md` · 6 reference `task-types`;
  deduplicated union = **23 unique live files**
- Reproduce: `grep -rl "\.claude/memory" ~/.claude/{skills,agents,hooks,workflows} | grep -v '\.bak'`
- ⚠️ An earlier draft of this packet claimed **57**. That number double-counted files matching
  more than one pattern and included 8 dead `.bak.*` backups from a June 2026 refactor. It
  overstated the migration surface ~2.5×. Corrected by audit — **size effort off 23, not 57**.
- The grep only covers three literal strings in `~/.claude/{skills,agents,hooks,workflows}`. It
  does **not** catch tools that infer project boundaries some other way — `gstack` writes
  `.gstack/browse-*.log` directly into 8 active project dirs including both grounding targets.
  Treat 23 as a floor, not a census.
- Notable: `skills/close-session/` (fires every session, owns context.md/history.md/decisions.md
  and ships `scripts/memory_migrate.py`), `skills/capture-feedback/`, `skills/new-session/`,
  `skills/day-shift/`, `skills/night-shift/`, `skills/morning-shift/`, `skills/dream/`

**Live examples of today's shape, in two incompatible generations**
- Gen 1 (`INDEX/kpis/todo/decisions/progress-log`, has managed markers): `~/Projects/knowledge-tree/`, `~/Projects/yt-agent-os/`
- Gen 2 (`context/history/decisions`, no markers): `~/Projects/dad/{company-preview,market-assessment,vc-outreach}/`
- Legacy (memory at project root, no tasks): `~/Projects/consulting/`
- `PROJECT.md` but no tasks at all: `~/Projects/{balkanski,portfolio,afton-king-gallery}/`

**Grounding targets**
- **Pilot:** `~/Projects/companion/` — one repo, real `PRD.md` + `BUILD-PLAN.md`, 11 routes, 47 tests
- **Stress case:** `~/Projects/dad/` — to become `king-research/` (three independent git repos
  destined for `make/`: `web/`, `runner/`, `company-preview/skill/`; 141KB + 83KB `history.md`
  files to merge) plus `vc-outreach/`

**Conventions the design leans on**
- `~/.claude/agents/research-deep-dive.md` — the existing **L0/L1/L2** definition
  (L0 = 3–5 bullets ~100 tokens · L1 = ~2K detailed · L2 = full sources)
- `~/.claude/CLAUDE.md` and `~/.claude/skills/file-versioning/` — one current file, stable name
- `~/Sandbox/Model-Configuration-Guide.md` — model routing and per-model prompting

**Current `.claude/` git policy — inconsistent across five repos**
- `dad/web` ignores all of `.claude/` (0 tracked) · `knowledge-tree` ignores it but still tracks
  `.claude/CLAUDE.md` · `balkanski` tracks 10 files including all memory · **`portfolio` has
  `.claude/settings.local.json` committed**, which is the one file designed never to be ·
  `companion` has no rule

## 6. Known open questions the designer could not settle

Stated plainly so you don't have to infer them — and so you can judge whether they are the *right*
open questions:

1. Should `research/` have write isolation at all, or be append-only from any mode?
2. Do worktrees silently void mode isolation? Absolute-path deny rules will not match inside
   `.claude/worktrees/<name>/`, and Carter's `night-shift`/`day-shift` use worktrees routinely.
3. Is one memory per project right, or does each mode need its own?
4. Are the Tier 0/1/2 token budgets (~2K / ~1K / unbounded) correct, or invented? They were
   reasoned to, never measured.
5. Is the migration worth it across 25 project folders, or should this apply only to new projects?

---

## 7. Audit addendum — gaps the designer left out

An independent audit ran over this packet before you received it, specifically hunting for what
the designer omitted. Everything below was **verified against the filesystem**, not accepted on
report. It is here because a reviewer cannot ask for what they don't know exists.

### A. The design omits its largest context channel entirely — and makes it worse

Claude Code maintains a **native per-cwd auto-memory store** at
`~/.claude/projects/<path-encoded-cwd>/memory/MEMORY.md`, injected every session, entirely
independent of the CLAUDE.md chain and `@import`. Verified:

- **99** such cwd-keyed stores already exist on this machine
- `-Users-carterking-Projects/memory/MEMORY.md` is **11,090 bytes ≈ 2,770 tokens**
- That is **larger than the entire proposed ~2K Tier 0 budget**, and claim #9 does not mention it

Worse, the store is **keyed by cwd**, and this design's whole mechanism is changing cwd.
Fragmentation is already visible: `-Users-carterking-Projects-companion` and
`-Users-carterking-Projects-companion--claude-worktrees-companion-build` are *separate stores*.
Adding `research/`, `plan/`, `make/` multiplies distinct cwds per project by three.

**Open question for Seats 2 and 4:** is `cd` the right lever when `cd` also silently re-keys the
native memory store? Does moving into `make/` orphan the accumulated project memory?

### B. Write isolation is already demonstrably void inside worktrees

Not an open question — a reproducible gap. Claim #5 puts enforcement in
`<mode>/.claude/settings.json`. Verified: `dad/web/.gitignore` and `dad/runner/.gitignore` **both
ignore `.claude/` wholesale** (2 of the 3 stress-case repos). `git worktree add` does not copy
untracked or gitignored files. Therefore **every worktree cut from those repos carries no deny
rule at all** — and `night-shift`/`day-shift` use worktrees routinely.

`companion/` has a `.claude/worktrees/` dir already and no gitignore rule either way, so the pilot
may share the blind spot. Open question #2 understated this; treat it as a finding.

### C. The Tier 1 budget is not unmeasured — it is measured and already breached

Open question #4 called the budgets "reasoned to, never measured." The data was one `wc -c` away.
Actual `context.md` files under `dad/`:

| File | Bytes | ≈ tokens | vs ~1K Tier 1 budget |
|---|---|---|---|
| `company-preview/` | 4,444 | ~1,100 | **over** |
| `market-assessment/` | 5,733 | ~1,430 | **over by 40%** |
| `vc-outreach/` | 2,288 | ~570 | under |

Two of three already exceed the budget the design asserts. For contrast, `claude-architect/CLAUDE.md`
is 3,755 bytes (~940 tokens) — genuinely in range for the ~2K Tier 0 target, so not every asserted
number is contradicted.

Note: **no token-counting tool exists in this setup** (no `ccusage`, no token-count skill). Byte
count ÷ 4 is the only available instrument. Say so rather than assuming a measurement you can't take.

### D. Claim #7 transplants L0/L1/L2 rather than deriving it

The L0/L1/L2 sizes come from `research-deep-dive.md`, where they describe **sections inside one
research document**. Claim #7 reuses the same labels and token sizes for a structurally different
artifact — **separate files** in a PRD. The numbers were carried over, never re-derived against any
actual phase-file or ADR in Carter's existing docs.

### E. The stress-case inventory is incomplete

Beyond the three repos and `vc-outreach/`, `dad/` also contains `crm-ui/` (a real shipped app) and
`market-assessment/` (with its own live `.claude/memory/context.md`). Neither is a git repo, neither
appears in the migration plan, and both need a mode-shape decision the design does not make.

### F. Prior art the design never engages

- **Two prior folder-shape generations already exist** (Gen 1 → Gen 2, §5). Nobody asked why Gen 1
  was abandoned or what that migration actually cost — the closest available evidence for whether
  a *third* migration is worth it.
- `~/.claude/hooks/research-enforcer.sh` is a **live, deployed, non-blocking** analog of the
  proposed `research/` mode — the nearest existing comparison for "hard `Edit()` deny vs. soft nudge."
- The `dream` skill already implements a reconcile-against-spec pattern; `DEVIATIONS.md` (claim #6)
  proposes a parallel one without asking whether it should follow that precedent.
- `auto_log_history.py`'s `detect_task_dir()` walks up for any `.claude/memory/` dir rather than a
  `TASK.md` marker — so it **keeps working unchanged** under one-memory-at-project-root. Evidence
  that the migration surface is less alarming per-file than a raw grep count suggests.
