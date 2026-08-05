# Verdict — review of the mode-based project structure

**Date:** 2026-08-04 · **Revised** after Carter's questions, which changed the conclusion.
**Full reviewer reports:** `mode-review-round1.md` · **The design reviewed:** `mode-structure-spec.md`

---

## Read this first

Four reviewers examined the proposed `research/` `plan/` `make/` folder structure. Their verdict
was "don't build it." Carter's questions on the first draft then surfaced something none of the
reviewers tested, and it **partly reverses that verdict**.

The short version:

- **As a way to enforce rules** (stopping a build session from editing planning documents) — the
folder idea **does not work**, and cannot be made to work. This is settled.
- **As a way to control which skills load** — the folder idea **does work**, it is verified, and it
targets the single biggest context cost found in the entire review. This is new.
- **As "not worth the effort anyway"** — that argument is now **suspended, not settled.** It was
built on measuring how small the saving is relative to a session's baseline cost — but ~11,000
tokens of that baseline is the global skill catalog the new recommendation proposes to cut. The
case against the design was measured against a number the design would itself change. It has to
be re-measured *after* skills are relocated, not before.

So the answer isn't "scrap it." It's **"the folders are a loading mechanism, not a locking
mechanism"** — and the question of whether that's worth the trouble is genuinely still open, in a
way the first draft of this document wrongly presented as closed.

---



## The new finding (from Carter's question about mode-specific skills)

**Question asked:** *"Is it possible for me to have project-specific, or even mode-specific, skills
so that they only load when I open a specific mode subfolder?"*

**Answer: yes. Tested and confirmed.**

A skill placed in a `.claude/skills/` folder inside a project loads **only when you're working in
that project or below it**. Open a different folder and it isn't there at all. Skills stack as you
go deeper — a session opened in `myproject/make/` sees skills from both `myproject/` and
`myproject/make/`.

**But there's a catch, and it's the same catch that ran through the whole review:** skills in your
global folder (`~/.claude/skills/`) load in **every session, everywhere**, no matter which directory
you're in. Folders can *add* skills. They cannot *remove* the global ones.

**Why this matters more than anything else in the review:** you currently have around **130 skills
installed globally**. Their descriptions alone are roughly **11,000 tokens loaded into every single
session** — whether you're writing code, planning, or asking a one-line question. That is more than
three times the entire amount the original folder design was trying to save.

So the highest-value thing folders can do for you is not policing writes. It's this:

> **Move skills out of the global folder and into the projects and modes where they're actually
> used.** A skill only useful when planning lives in `plan/`. A skill only useful for one client
> lives in that client's folder. Everything else stops costing you anything in every unrelated
> session.

That is a genuine context-curation win, it's mechanically verified, and it needs no permission
system, no migration of existing work, and no risk.

---



## On the framing you objected to

You wrote: *"It seems that you used the DAD project as the source... I wanted to look at this based
on principles, not an exact example."*

**You're right, and that was my error, not the reviewers'.** I chose `dad/` and `companion/` as the
grounding targets when I briefed them. That decision quietly changed the question from *"is this
structure good?"* to *"is migrating these two messy projects to this structure worth it?"* Those are
different questions and I got an answer to the second one.

So here are the findings separated properly. The first group is about **how Claude Code works** —
true for any project, yours or anyone's. The second group is only about **migrating your existing
folders**, which you've said you want set aside.

---



## Group 1 — Principles (true regardless of your projects)

**Provenance, audited — because "is this actually principles, or just relabelled?" is a fair
question and the honest answer is "mostly, but not entirely":**


|        | Where it came from                                                      | Genuine principle?                                                                    |
| ------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **P1** | Sentinel files in a synthetic throwaway directory tree                  | ✅ yes                                                                                 |
| **P2** | Controlled A/B in an isolated harness that never touched Carter's files | ✅ yes — the strongest                                                                 |
| **P3** | Synthetic harness + a throwaway git repo for the worktree test          | ✅ mechanism yes; *illustrated* below with Carter's repos, which makes it look derived |
| **P4** | **Sampling 33 of Carter's real sessions**                               | ❌ **no** — a measurement of this machine, and circular. See its caveat.               |
| **P5** | Mechanism verified generally; severity numbers from Carter's projects   | ⚠️ mechanism yes, severity no                                                         |


So P1–P3 are experiments anyone could re-run on an empty folder and get the same result. P5's
mechanism is real but its "how bad is it" evidence is local. **P4 is not a principle at all**, and
it is the one the reviewers leaned on hardest to dismiss the design.

### P1. Instructions load *downward and additively* — you can add, never subtract

An instruction file in a folder applies to that folder and everything beneath it. Going deeper only
ever *adds* instructions. There is no way for a subfolder to say "ignore what the parent said."

*Consequence:* a project-level file must contain only things true in **every** mode. Anything
mode-specific put at the top level leaks into all modes permanently.

### P2. Loading an instruction is not the same as it being obeyed ⚠️

**This is the most important technical finding of the review.** A reviewer ran a controlled test:
a top-level file said *"always end your response with this exact marker."* A subfolder file said
*"never output that marker."* The marker did not appear — **even though the top-level rule was fully
loaded and sitting right there in the model's context.**

Nearer and more specific instructions quietly win over distant, general ones. No error, no warning,
nothing looks wrong.

*Consequence:* the idea that a project-level file can hold "invariant" truths that modes must
respect **does not hold**. There is no mechanism enforcing it. And every test I ran before the
review — including ones I reported to you confidently — measured whether text *loads*, never
whether it's *followed*. I proved delivery and called it control.

### P3. Nothing available here is a hard boundary

The design proposed blocking a build session from editing planning files. Testing found:

- The blocking rule works against the direct file-editing tool — genuinely, it stops it.
- But a one-line `python` or `node` command writes straight through it. Both are on your
always-allowed list.
- Background scripts that run automatically at session end bypass the permission system entirely —
they aren't tool calls, so no rule of any kind can see them.
- Simple shell commands (`echo`, `printf`, `cp`) *are* caught — which is the trap. It works just
well enough to pass a casual check while leaving a wide gap open.

*Consequence:* mode separation can be a **convention you honor**, not a rule that's enforced. The
honest ceiling, in a reviewer's words: nothing here is silent-proof; the best available property is
**"defeatable only by a visible act"** — something that shows up in the transcript rather than
happening invisibly.

[I believe that we should use the blocking rules and then explicitly state to not use python or node commands to get around it. If claude understands the shape / structure of our projects, it will respect it. We just need to explain the alternative locations for Claude to write and then claude will follow. He is smart]

### P4. ⚠️ NOT A PRINCIPLE — and partly circular. Read the caveat.

**Provenance:** unlike P1–P3, this did not come from a controlled experiment. It came from sampling
**33 of Carter's own real sessions**. It is a measurement of *this machine*, not a fact about how
Claude Code works. Someone with 10 skills installed instead of 130 would get a different answer.

The finding as stated: a session starts with **40,000–80,000 tokens** already loaded — system
instructions, tool definitions, and the global skill catalog. The folder design was trying to save
around **3,000**. Normal variation between two sessions on the *same* project is **6,400–6,800
tokens**. Conclusion drawn: the effect is smaller than the background noise, so even a perfectly
working design would be undetectable.

**Why that reasoning is circular.** Roughly **11,000 tokens of that 40–80K floor *is* the global
skill catalog** — the very thing the revised recommendation proposes to cut by scoping skills into
folders. So the strongest argument against the design was computed against a baseline that the
design's best version would itself shrink. Nobody caught this during the review, including me,
because skills were never mentioned in the reviewers' briefing.

*Consequence:* **P4 cannot be used to dismiss the folder idea until it is re-measured after skills
are relocated.** The correct order is: relocate skills → re-measure the floor → then judge whether
the remaining effect is detectable. Treat the "rounding error" conclusion as suspended, not settled.

### P5. Changing folders changes your identity to Claude's own memory

Claude Code keeps a private memory file per directory you work in. Change directory, and you're
writing to a different memory. Splitting a project into three mode folders means three separate
memories, each starting empty.

*Consequence:* a real cost of folder-switching that has nothing to do with instructions or
permissions. Worth knowing before adopting; not fatal, but it means the first session in a new
mode folder starts cold.

[This just means that we need to be more particular about what gets saved in .claude memory and what gets saved in files that persist. I think this is a key principle anyways because when working on a team, we need to make sure that all the necessary information is discoverable to the team. What information is saved in the memory files? Is memory auto-loaded or is it lazy loaded? Is memory commited to a github repo (is it discoverable by teammates)? Would claude be able to read from the memory files of a different directory?]

---



## Group 2 — Findings specific to your existing projects (set aside, as you asked)

Recorded so they aren't lost, but they judge *migration*, not the idea:

- Migrating your `dad/` folder would mean building three complete mode structures and roughly nine
new configuration files by hand.
- `companion/` was a poor choice of pilot — its real code sits on an unmerged branch, and it never
had the old structure to begin with, so it couldn't have tested migration anyway.
- About 23 files in your global config refer to today's folder layout and would need updating.

None of this bears on whether the principles are sound.

---



## Your questions, answered



### "What do you mean by cap and rotate? What's in these logs? Why do they exist?"

`history.md` is an **append-only diary of your work sessions.** Every time you finish a session, a
script writes a dated summary of what happened to the bottom of that file. Nothing ever removes
anything, by design — it's meant to be a permanent record.

The problem is that "permanent record" and "no maintenance" don't mix. Two of yours have grown to  
**145,000 and 85,000 characters** — larger, individually, than the entire context budget the folder  
redesign was targeting.

**"Cap and rotate"** means: when the file passes some size (say 20,000 characters), move everything
currently in it into a dated archive file — `history-2026-08.md` — and start a fresh empty one.
Nothing is lost; the old content just moves out of the way. You already use exactly this pattern
elsewhere, via your `file-versioning` convention.

[Agreed, we should cap and rotate. I also and am unsure as to whether we truly need a diary like summary of all my session saved... Why would this be useful? If we can update the roadmap with our progress then why would we need to keep a summary of what we have done? I understand having a history but doesn't github/githistory keep track of what has changed over time? We should be principled about what we actually allow to appear inside of the memory files. My instinct says that we do not need a summary of every session.]

### "Why is `.claude/` gitignored? What happens if it isn't?"

The `.claude/` folder inside a project holds a mix of things: settings you'd want to keep, skills
worth saving, personal preferences that shouldn't be shared, and disposable scratch data. Ignoring
the whole folder is the blunt approach — one line, done, nothing accidentally committed.

The cost of that bluntness: **git literally does not copy ignored files.** So when a tool creates an
isolated copy of your repo to work in (your overnight jobs do this constantly), that copy arrives
with **no** `.claude/` **folder at all** — no settings, no rules, nothing. Any protection you set up is
simply absent there, and nothing warns you.

If you *didn't* ignore it: your settings and memory files would be saved into the repo's history.
For your private solo repos that's mostly harmless and arguably good — except for one file,
`settings.local.json`, which holds personal machine-specific settings and genuinely shouldn't be
committed. (One of your repos has committed it already.)

**The fix is neither extreme:** keep ignoring the folder, but add a single exception for the
settings file. One line, and isolated copies stop arriving empty.

[I actually disagree. I think that we should not gitignore .claude. I think that these files are really helpful, especially when working as a team. Again, we need to be more principled about what shows up in these files. What currently exists in there? What could exist in there? What is worth sharing with team members? Could it be possible to have the .claude files be saved on a per user basis? Meaning that we prevent individuals / agents from editing another user's .claude files? Or is it possible to protect specific files inside of the .claude memory? Would that even be necessary?]

### "Garbage-collect orphaned memory stores — could you explain how this works?"

When you open Claude in a folder, it creates a private memory file for that exact folder path. When
the folder is later deleted — which happens routinely, since your overnight jobs create temporary
copies of repos and remove them afterward — **the memory file stays behind forever.** Nothing cleans
it up. It's now a memory for a place that doesn't exist.

I found three of these. They're harmless individually, just clutter that accumulates.

The fix is small: your `dream` routine already walks through memory files weekly. Add a check —
for each memory file, work out which folder it belongs to; if that folder is gone, flag or delete
the memory. Roughly five lines added to something that already runs.

[I think this is good. And lets have it suggest how to fold it into the existing memory files or to delete it]

### "The two-field TASK.md fix — what is this explicitly referring to?"

Today each task declares one label, `Task Type`, chosen from a list like `coding`, `knowledge`,
`strategy`, `documentation`. The complaint that started this whole redesign was that **this single
label is trying to describe two unrelated things at once** — `coding` describes *what kind of work
you're doing*, while `knowledge` describes *what the subject matter is*. No task can honestly pick
just one.

The proposal is: instead of restructuring your folders, **just use two labels instead of one:**

```
Mode:   plan          ← what kind of work this is
Domain: coding        ← what it's about
```

Same file, one extra line, no folders moved, nothing to migrate. It fixes the exact complaint that
was originally diagnosed. It does **not** help with context curation — the reviewer who proposed it
said so plainly about their own idea.

[Push back: I don't think that the labels would even be necessary if we start sessions inside of the correct folders / working directories. I like the proposed subfolder structure (a subfolder per mode that can be templated so that all of our projects operate the same)]

### "Could tool permissions be set at the file level? Allowed tools changing per file, rather than granting everything upfront."

**Yes — and this mechanism already exists.** You don't need to build a new harness.

Claude Code supports **hooks**: small scripts that run *before* a tool is used. The script receives
the details of what's about to happen — including which file is about to be touched — and can allow
it or block it. That is precisely "permissions that change depending on the file."

You already own a working example. Your `freeze` skill does exactly this: it hooks the edit tools,
checks whether the target file is inside an allowed folder, and blocks it if not.

Two honest limits, both established by this review:

1. It works cleanly for **file-editing tools**, because those announce which file they're touching.
  It does *not* generalize to shell commands, because a shell command is just text — a script
   would have to recognize every possible way of writing to a file, which is unwinnable.
2. Your `freeze` uses one global boundary at a time, so it can't express different rules per folder
  as-is. Making it per-folder is a modest change to a script you already have.

So: a good instinct, mostly already built, and worth extending as a side project — with realistic
expectations that it constrains the tidy tools and not the shell.

[Lets save this because I want to spend more time on this separately. I think this is important]

---



## What to actually do

**In leverage order — the first is worth more than the rest combined.**

1. **Move skills out of global.** ~130 skills load into every session at roughly 11,000 tokens.
  Decide which you genuinely want everywhere, and relocate the rest into the projects or modes
   where they're used. This is the real context-curation win, it's verified, and it's the one thing
   the folder structure is genuinely good for.
2. **Cap and rotate the two oversized history files** (145K and 85K characters).
3. **Add the** `.claude/settings.json` **exception** to the gitignore of repos that ignore `.claude/`,
  so isolated copies stop arriving with no settings.
4. **Add orphan cleanup to** `dream` — five lines, removes memory for folders that no longer exist.
5. **Adopt the two-label fix** if the taxonomy complaint still bothers you.
6. **Merge PR #1** — `companion/BUILD-PLAN.md` still says "not started" while finished, reviewed
  work sits unmerged.

**And write down, somewhere you'll find it later:** blocking rules do not stop shell commands or
background scripts. Otherwise you'll write one in six months and trust it.



[I approve this plan, but make sure everything agrees with the comments that I made. I think you will have to wait on #5]

---



## Still your call

**1. Do you want to test the folder structure properly — as a loading mechanism this time?**
The review tested it as a *permission* system and it failed. It was never tested as a *skill-scoping*
system, which is where the value turns out to be. That's a fresh, cheap experiment on one new
project: does organizing by mode make it obvious which skills belong where? No migration required.

[yes]

**2. Is a hard write boundary worth pursuing at all?**
Two untested candidates: operating-system file permissions (works against everything including
shell commands, but you could undo it yourself — visibly), or withholding the edit tools from a
role entirely (absolute, but breaks any role that needs a shell, which is most of them). Both
reviewers agree nothing here is silent-proof.

[not worth pursuing yet]

**3. Should "one memory per project" be written down as a rule?**
It's already how you work in practice. Writing it down prevents a future regression rather than
fixing a current problem. Cheap either way.

[No I want to wait on this because we need to discuss how we think memory files should work. Then once we have decided, we will bake it into the close-session skill, the dream skill, and any other that need it.]

**4. Your global settings currently allow all file editing everywhere, unconditionally.**
This is what makes every gap above cost-free — a wrong rule fails to *silently allowed* rather than
to *ask me first*. Narrowing it means more prompts across every project. A friction trade only you
can price.

[leave as is for now]

**5. Why did your last folder-structure change actually happen?**
Two incompatible generations exist in your projects and nothing on disk explains why the first was
abandoned. It's the most relevant evidence for whether a third change is worth making, and only you
know the answer.

[please clarify what you mean? Which folder structures are you referring to?]

---



## How much to trust this review

Four reviewers worked independently, then read each other and responded. They corrected me
repeatedly — a file count I'd inflated 2.5×, a memory-store figure I'd presented as typical when it
varied 119× across projects, and my claim that no token-measuring tool existed when the real data
was sitting in every session's records. They also corrected themselves and each other.

Two honest gaps: I never verified one reviewer stayed on the model I intended, and **the review
never examined skill scoping at all** — because my briefing framed the design around instructions,
memory, and permissions, and never mentioned skills. That gap was closed by Carter's question, not
by the review, and it's the finding that changed the conclusion.