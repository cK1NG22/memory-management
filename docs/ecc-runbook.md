# ECC runbook — using it, and loading it into a build

ECC ("Everything Claude Code", upstream `affaan-m/ecc`) is used here as a **library**, never
installed. Builds take hand-picked pieces from it, as symlinks or copies (step 4). Decision record: `.claude/memory/decisions.md` 2026-09-28 and 2026-09-29; the 36
adoption decisions: `plan/ecc-decisions.md`.

## Where it lives

- **Library clone:** `~/Projects/memory-management/ecc/` — Carter's fork `ck22coding/ECC`, its own
  git repo, ignored by this one. It sits here so this project's memory-system context is loaded
  whenever a build is set up with ECC.
- **Never move or rename it while any build links to it.** Symlinks use absolute paths inside it;
  a move breaks all of them silently (the same failure as a stranded memory store). Copied builds
  don't care.
- **Updating:** `git -C ~/Projects/memory-management/ecc pull`. To take upstream changes, sync the
  fork first (`gh repo sync ck22coding/ECC`), then pull. Symlinked pieces update everywhere at
  once; copied rules do not (see step 5).
- **Do not run the installer** (`install.sh` / `npx ecc-universal`). It writes into `~/.claude/`
  and drops packaging files there. Use it only as `--dry-run --json` to read what a profile holds.

## Using it in a session

| Piece                                | How it is used                                                                                                               | Notes                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Agents** (68)                      | Claude delegates to them by their `description`, or you name one ("use the code-reviewer agent")                             | Each pins a model in frontmatter: 58 sonnet, 4 opus, 6 haiku |
| **Skills**                           | Load on description match, or `/<name>`                                                                                      | Count against the skill-listing budget (see Gotchas)         |
| **Commands** (94)                    | `/<name>` — **no `/ecc:` prefix**; that prefix only exists on the plugin path                                                | 26 are broken here (see Gotchas)                             |
| **Rules**                            | No `paths:` → loaded at session start. With `paths:` → loaded only when Claude reads a matching file (see "When rules load") | Must be real copies                                          |
| **Hooks, instincts, session memory** | **Not used** (decided 2026-09-28)                                                                                            | close-session stays the resume mechanism                     |

## Loading ECC into a build

1. **Decide committed vs local-only.** If the repo is someone else's (eightfaces is Scott
   Murff's), keep ECC **local-only** via `.git/info/exclude`, which is never committed. Committed
   symlinks to `/Users/carterking/...` break for anyone else, so a shared repo would need real
   copies — ask the owner first. Local-only costs one thing: background-job worktrees don't see the
   links (bgIsolation copies only tracked files).
2. **Resolve the profile from ECC's own planner**, not the README. From a scratch git repo:
   ```bash
   node <upstream-or-fork>/scripts/install-apply.js --target claude-project \
     --profile developer --without baseline:hooks --dry-run --json > plan.json
   ```
   Seven profiles exist (minimal, opencode, core, developer, security, research, full); none has a
   permissions setting. "Developer, no hooks" = the command above. The planner resolves
   dependencies, so it adds modules the profile never names (it pulled in `unified-memory`).
3. **Drop what we don't use:** `rules/` until the stack is confirmed; `.agents/`, `.pi/`,
   `plugin.json`, `marketplace.json`, `mcp-configs` (other harnesses / packaging); and the skills
   `continuous-learning`, `continuous-learning-v2`, `unified-memory`, `ck`, `hookify-rules`,
   `plankton-code-quality`, `delivery-gate`, `configure-ecc`.
4. **Link or copy agents, commands and skills — symlinks are optional.** Both load (probed).

   |                          | Symlink                         | Copy                      |
   | ------------------------ | ------------------------------- | ------------------------- |
   | Fork updates             | reach every build at once       | frozen; re-copy to update |
   | Moving `ecc/`            | breaks every link silently      | no effect                 |
   | Commit to a shared repo  | no (absolute paths to this Mac) | yes                       |
   | Background-job worktrees | only if committed — so no       | yes, if committed         |
   | Edit one build's copy    | no — edits hit every build      | yes                       |
   | Rules                    | **do not load**                 | load                      |

   ALWAYS.md's "never vendor" rule targets third-party tools that keep shipping; ECC is our own
   fork, so copying from it is a trade-off, not a violation. Either way, go item by item (not
   whole folders) so the project's own agents/skills/commands sit beside them and an exclude line
   never hides a real file you later want to commit. The symlink version (used for eightfaces;
   swap `ln -s` for `cp -R` to copy):

   ```bash
   L=~/Projects/memory-management/ecc; cd <build>; mkdir -p .claude/agents .claude/commands .claude/skills
   for f in $L/agents/*.md;   do b=$(basename $f); [ -e .claude/agents/$b ]   || { ln -s $f .claude/agents/$b;   echo "/.claude/agents/$b"; }; done >> ex.txt
   for f in $L/commands/*.md; do b=$(basename $f); [ -e .claude/commands/$b ] || { ln -s $f .claude/commands/$b; echo "/.claude/commands/$b"; }; done >> ex.txt
   for s in <skill list from plan.json, minus drops>; do [ -e .claude/skills/$s ] || { ln -s $L/skills/$s .claude/skills/$s; echo "/.claude/skills/$s"; }; done >> ex.txt
   { echo "# ECC — local only, links into $L"; cat ex.txt; echo "# end ECC"; } >> .git/info/exclude; rm ex.txt
   ```

   The `[ -e … ] ||` guard never overwrites a project's own file with the same name.

5. **Rules (once the stack is confirmed): real copies** into `.claude/rules/ecc/`. Rules skip
   symlinks, file and folder alike. Copies are frozen at the day they were made, so note the fork
   commit they came from and re-copy when the fork moves.
6. **Verify, with a negative control**, from the build folder:
   ```bash
   claude -p --model sonnet --no-session-persistence "No tools. Copy verbatim any agent names
   containing 'reviewer', and say yes/no for skills <an ECC skill>, <a project skill>, <a dropped skill>."
   ```
   The dropped skill must come back "no" — a model will otherwise agree with a leading question.
   Also check: `git status` shows nothing new, and
   `find .claude -type l ! -exec test -e {} \; -print` prints nothing.
7. **Record it** in the build's notes and in this repo's `decisions.md`.

**Undo:** `find .claude -type l -lname '*memory-management/ecc/*' -delete`, then delete the
`# ECC … # end ECC` block from `.git/info/exclude`.

## What loads, and from where (probed)

| Setup                                                   | Loads?                                               |
| ------------------------------------------------------- | ---------------------------------------------------- |
| Symlinked skill folder                                  | yes                                                  |
| Symlinked agent file                                    | yes (2026-09-29)                                     |
| Symlinked command file                                  | yes (2026-09-29)                                     |
| Symlinked rule file or rules folder                     | **no**                                               |
| Real subfolder `.claude/rules/ecc/`                     | yes                                                  |
| A mode folder's `.claude/` (e.g. `make/.claude/skills`) | only when the session **starts** in that mode folder |

The last row matters for mode-structured builds: put ECC in the `.claude/` of the folder the build
session is launched from.

## When rules load (docs-verified 2026-10-14)

Source: Claude Code docs, `memory.md` and `claude-directory.md`, read through context7's
`/pjbrito/claude-code-docs` mirror (no official Anthropic entry in context7).

- **Subfolders count.** "All `.md` files are discovered recursively", so `.claude/rules/ecc/<lang>/`
  is found.
- **No `paths:` frontmatter → loads at session start**, like CLAUDE.md. ECC's `common/` files have
  none, so all of them load every session.
- **`paths:` frontmatter → loads only when Claude _reads_ a matching file**, "not on every tool
  use". ECC's `typescript/`, `react/` and `web/` files all carry `paths:` globs (`**/*.ts`,
  `**/*.tsx`, `**/*.css`, …), so a session that never opens code never loads them, and opening one
  `.tsx` file loads all three folders at once.
- **Rules are guidance, not enforcement.** "For guaranteed behavior use hooks or permissions."
- Observed in an eightfaces session the same day: start-of-session context held the nine
  `common/` files and none of the scoped ones.
- **ECC's react globs assume a type-based layout** (`**/components/**`, `**/hooks/**`,
  `**/pages/**`). In a feature-folder build those never match; only `*.tsx`/`*.jsx` triggers them.

**Key Insights**

- To keep a rule out of sessions that don't need it, give it `paths:` instead of deleting it. To
  force a rule to load, remove its `paths:`.
- A scoped rule that contradicts the project's CLAUDE.md (coverage targets, folders by type) arrives
  mid-session, after CLAUDE.md, so the conflict is easy to miss. Name the override in CLAUDE.md.

## Gotchas

- **26 commands (and ~14 skills) still point at plugin paths** — `${CLAUDE_PLUGIN_ROOT}/…` or
  `~/.claude/skills/…`, which exist on neither the link nor the copy path. **Fix them in the fork**
  (it's ours to edit), then every build picks the fix up: repoint to a real path, or delete the
  command. Eight are instinct commands (`evolve`, `promote`, `prune`, `projects`, `skill-create`,
  `instinct-*`), which are out anyway. The rest lean on `scripts/github-coordination.js`,
  `scripts/lib/session-*`, `setup-package-manager.js`, `install-plan.js`. Until fixed they fail
  when run. Open TODO.
- **Skill-listing budget.** The global catalog was already ≈36k chars against a ≈30k budget before
  ECC; a build with 117 ECC skills + 94 commands will truncate descriptions. Not yet measured. The
  69 language/framework skills are the first cut once a build's stack is known.
- **zsh does not word-split `$VAR`.** A `for x in $LIST` loop in the Bash tool (zsh) runs once over
  the whole string and silently matches nothing. Run list loops under `/bin/bash` or use `${=LIST}`.
- **`common/code-review.md` names every language reviewer** in a table, including ones a build has
  unlinked. Harmless, but a session may mention agents that aren't there.
- **The fork lags upstream.** `i18n-sync` is in the upstream developer profile but not the fork.
- **Background jobs in this repo:** the rtk hook rewrites `git push` into a form the worktree
  guard refuses; run `/usr/bin/git …` (absolute paths bypass rtk).

## Builds using ECC

**companion has 14 dead links** as of 2026-10-21 (11 commands, `dmux-workflows`, `ecc-guide`,
`tdd-workflow` — deleted from the fork in `7167296d`). Clean with
`find .claude -type l ! -exec test -e {} \; -delete` in that build.

| Build                                | Mode                                                                               | Pieces                                                                                                                                                                                                   | Added                                |
| ------------------------------------ | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `~/Foundry/clients/perry/eightfaces` | **committed copies** since 2026-10-14 (`09bbd75`, `a89e6db`; `scripts/ecc.sh` removed); local-only links before | 32 agents, 75 commands, skills; 22 rule files copied (`common`, `typescript`, `react`, `web` from fork `a0e8a663`, minus `*/hooks.md` and `react/testing.md`)                                  | 2026-09-29; committed 2026-10-14 |
| `~/Projects/products/companion`      | **committed** symlinks (Carter's private repo; worktree builds need tracked links) | 30 agents, 51 commands, 53 skills linked; 21 rule files copied (`common`, `typescript`, `react`, `web` from fork `a0e8a663`, minus `*/hooks.md`, `common/testing.md`, `react/testing.md`) + `_source.md` | 2026-10-04 (PR #2, merged `4ecef62`) |
