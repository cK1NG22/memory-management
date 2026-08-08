# Trim skills to gstack shape

Fixes: skill-listing budget is aggregate (~1% of context, scales w/ model). ~43 non-gstack global
skills carry the bulk of it; fattest descriptions evict thinnest skills' triggering, silently.
Source: `../research/sources/skill-description-drop.md` · `ROADMAP.md` "Trim skill frontmatter…".
Scope: non-gstack global skills only. gstack (49, tagged `(gstack)` in description) and plugin
skills (`superpowers:*`, `ponytail:*`, …) are out of scope — installer/upstream-owned.

## 1. Inventory — work-list, fattest first
```bash
cd ~/.claude/skills && python3 <<'EOF'
import os, re
def read_desc(path):
    text = open(path).read()
    if not text.startswith('---'): return None
    end = text.find('\n---', 3); fm = text[3:end]
    m = re.search(r'^description:\s*(.*)$', fm, re.M)
    if not m: return None
    first = m.group(1).strip()
    if first in ('>', '>-', '|', '|-'):
        block = []
        for line in fm[m.end():].split('\n'):
            if line.startswith('  ') or not line.strip(): block.append(line.strip())
            else: break
        return ' '.join(block).strip()
    return first.strip('"').strip("'")

rows = []
for d in sorted(os.listdir('.')):
    if not os.path.isdir(d) or d.startswith('_'): continue
    real = os.path.realpath(d) if os.path.islink(d) else d
    smd = os.path.join(real, 'SKILL.md')
    if not os.path.isfile(smd): continue
    desc = read_desc(smd)
    if desc is None or desc.rstrip().endswith('(gstack)'): continue
    rows.append((len(desc), d))
rows.sort(reverse=True)
print(f"skills: {len(rows)}  total chars: {sum(n for n,_ in rows)}")
for n, d in rows: print(f"{n:6d}  {d}")
EOF
```
Symlinked dirs (e.g. `ui-ux-pro-max`) resolve to canonical file — edit there. Verified 2026-08-07:
**47 skills, 18,440 chars.** Top 10 work-list: xlsx (943), ui-ux-pro-max (806), docx (785),
sources-cited (735), pptx (694), youtube-slide-transcript (625), restructure-project (617),
new-session (597), capture-feedback (596), new-project (570).

## 1b. Invocation split (Carter, 2026-08-08 — from mattpocock/skills `writing-for-agents`)

**Zero bare names is the wrong target.** A description exists so the *agent* can fire the skill
from natural words. Skills only ever fired by Carter typing the name need NO description in the
listing — bare/absent is their correct, deliberate state.

Three states (all probe-verified on this machine):

| State | Mechanism | Listing cost | Who can fire it |
|---|---|---|---|
| model-invoked | `description:` (trimmed) | description chars | agent from your words · you · other skills |
| name-only | `skillOverrides: {"<name>": "name-only"}` | ~name chars | you · agent/skills by exact name |
| user-invoked | `disable-model-invocation: true` in frontmatter | **zero** (ABSENT) | you by `/name` only |

Classification of the 47 non-gstack global skills:

**FLIP to user-invoked** (`disable-model-invocation: true` — frees their full chars, no rewrite):
`memory-review` · `claude-audit` · `new-project` · `restructure-project` (retiring anyway) ·
`autoresearch` · `kpi-setter` · `opusplan` · `learn` · `resolve-vulns` (parked) ·
`youtube-slide-transcript` (625; has no working description today anyway) ·
`close-session` (303) · `new-session` (597) — both ruled user-invoked (Carter, 2026-08-08)
→ frees ≈ 5K chars before any trimming.

**NAME-ONLY deliberately** (skill-to-skill reach by exact name must survive):
`sources-cited` (735 — invoked by name from 411-case; description was dead weight)

**KEEP model-invoked → trim to band** (agent must fire these itself):
- file-type routing: `xlsx` `docx` `pptx` `pdf` — fattest, trim hardest
- agent self-fire guardrails: `capture-feedback` (fires when Carter corrects) · `file-versioning`
  (fires before making a v2/copy) — the agent, not Carter, must catch the moment
- natural-phrase workflow: `brain-dump` · `clean-transcript` · `transcribe-media` ·
  `doc-coauthoring` · `skill-creator` · `scout-stack` · `decide` · `locker` · `ui-ux-pro-max`
- task-shape (all leaving for the make/ mode home in Plan A): `tdd` `api-design`
  `architecture-review` `database-design` `mcp-builder` `dung`
- cron/shift family — **ruled model-invoked (Carter, 2026-08-08), do not flip:** `email-tracker`
  `github-digest` `workout-bot` `dream` `day-shift` `night-shift` `morning-shift`. They fire
  from launchd/headless prompts that may phrase naturally; trim their descriptions normally.

**Out of scope:** gstack (installer-owned, already terse) · plugins (`superpowers:*`,
`ponytail:*` — the runtime hardcodes plugin skills to "on"; settings overrides are ignored;
`/plugin` disable is the only lever) · Anthropic built-ins (budget-exempt).

## 2. Backup — before any edit
```bash
cd ~/.claude/skills && tar czhf ~/Claude/_archive/skill-trim_$(date +%F).tar.gz */SKILL.md
```
`-h` dereferences symlinks into real content. One dated tar, not per-file `_archive/`
(file-versioning's sibling-folder convention doesn't fit a scattered multi-dir batch). Verified:
97 files archived clean.

## 3. Rewrite rules
| Survives | Dies |
|---|---|
| trigger phrases the user actually types | marketing prose ("intelligence", "pro-max") |
| the "Use when X" clause | enumerated example lists (50 styles, 9 stacks…) |
| one clause of what the skill does | restating the skill's own name |
| file-type/domain nouns that route intent | anything the body already covers |

Target band: 80–200 chars; up to ~300 where the type list *is* the trigger (xlsx, docx, pptx).
Edit `description:` (and `when_to_use:`, if present — counts toward the cap) only. Body, name,
behavior untouched.

## 4. Batch order
Fattest → thinnest, in place. **Stop after the top 10, show Carter the diff.** Resume only on his
go-ahead — a bad trim kills triggering as silently as a bare name does.

## 5. Verification
- Re-run §1 → compare total chars to baseline 18,440.
- Headless bare-name probe: `claude -p "In your system prompt there is a skill list, each 'name:
  description' or bare name-only. Without tools, output ONLY '<described-count>,<bare-count>'."`
  Verified baseline: `114,16`. Target: zero *unintentional* bare names — every KEEP-list skill
  described in every probe; FLIP-list skills ABSENT; only `sources-cited` bare by design.
- Aggregate budget line: `claude --debug-file <path> -p "ok"; grep -i "over budget" <path>` —
  no WARN, or chars drop materially. Baseline: `130 skills, 35948 chars > 30000 budget`.
- Authoritative: Carter runs `/doctor` before/after — only view with per-skill eviction, not just
  the aggregate.

**Target: non-gstack catalog under ~9K chars** (from 18,440: ≈4K freed by §1b flips + ≈5–6K by
trims). If short: Plan A relocation (15 more skills leave global — ROADMAP) next;
`skillListingBudgetFraction: 0.02` is the deliberate last resort (costs context every session).

## 6. Falsifier
KEEP-list skills still showing bare after the cut lands (18,440 → ~9K) means trimming didn't fix
triggering — eviction keys on something besides char budget (stale usage-ledger cache, or a
priority formula weighted differently than researched). Re-open research; don't re-trim harder.
A FLIP-list skill still *listed* after its flip means `disable-model-invocation` isn't honored
for that skill type — fall back to `skillOverrides: name-only` for it.

## 7. What gets deleted
Description prose — marketing language, example lists, restated names. Nothing else moves.
Verified by the §1 diff (per-skill before/after chars) against the §2 tar, the only copy of the
pre-trim text.

## 8. Riders — same pass, same session (Carter, 2026-08-08)
- **`opusplan` → `fable-plan`.** Rename the skill (dir + `name:`), update its body to invoke
  Fable instead of Opus, and grep for callers/references to the old name (settings allow-rules,
  other skills, memory files) before deleting the old dir. It's on the FLIP list — apply
  `disable-model-invocation: true` in the same edit.
- **`capture-feedback` needs a content review against the Gen 4 memory system.** Its routing
  (task-type folders under `~/.claude/task-types/`) is the Gen 3 scheme; global rules now live in
  `~/.claude/modes/ALWAYS.md` and mode principles in `<MODE>-MODE.md`. Update where captured
  feedback gets written before (or while) trimming its description — a trimmed pointer to the
  wrong destination is still a bug.
