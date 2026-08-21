# Trim diff — top-10 fattest KEEP-list descriptions

Carter-facing review file. Char counts are from the inventory script (verbatim from the brief),
which counts each escaped `\"` in a quoted YAML description as 2 raw characters — same
methodology used for both the pre-trim and post-trim inventories, so the before/after numbers are
directly comparable even though the true "as read" text is a bit shorter than the count implies.

---

## 1. xlsx (943 → 253)

**Old:**
> Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like "the xlsx in my downloads") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved.

**New:**
> Open, read, edit, create, or convert spreadsheet files (.xlsx, .xlsm, .csv, .tsv) — formulas, formatting, charts, cleaning messy tabular data. Deliverable must be a spreadsheet. Not for Word docs, PDFs, or general Python/database work with tabular data.

---

## 2. ui-ux-pro-max (806 → 200) — revised in fix round 1

**Old:**
> UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples.

**New (round 1 fix):**
> Design or review UI/UX for web/mobile — styles, color palettes, typography, layout, accessibility, components. Stacks: React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui.

*Note: this is the symlinked skill — edited at the canonical path `~/.agents/skills/ui-ux-pro-max/SKILL.md`, not the `~/.claude/skills/` symlink.*

*Fix round 1 (finding 1): initial trim dropped Next.js and React Native from the 9-stack list (7 of
9 kept). Restored both. To stay at the 200-char cap, shortened "for web and mobile apps" to
"for web/mobile" — no routing noun lost, just a word-count trim. 186 → 200.*

---

## 3. docx (785 → 247)

**Old:**
> Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation.

**New:**
> Create, read, edit, or convert Word documents (.docx) — formatting, tables of contents, headings, tracked changes, comments, images, find-and-replace. Use for reports, memos, letters, templates as .docx. Not for PDFs, spreadsheets, or Google Docs.

---

## 4. pptx (694 → 212)

**Old:**
> Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions "deck," "slides," "presentation," or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.

**New:**
> Create, read, edit, or extract from PowerPoint files (.pptx) — slide decks, pitch decks, presentations, templates, layouts, speaker notes. Trigger on "deck", "slides", "presentation", or any .pptx filename.

---

## 5. clean-transcript (567 → 186)

**Old:**
> Clean up a meeting or call transcript — remove filler words, false starts, greetings, closings, and off-topic small talk, and tighten rambling into concise statements, WHILE keeping speaker labels and every real piece of content (decisions, numbers, dates, names, action items, questions). Works on a transcript pasted in chat or a transcript file path. Also used as a sub-step by the notion-transcript skill. Use when: "clean this transcript", "clean up the transcript", "tidy this transcript", "remove filler words", "de-fluff this transcript", "/clean-transcript".

**New:**
> Clean a meeting/call transcript — remove filler words, false starts, small talk; keep speaker labels, decisions, action items. Use when: "clean this transcript", "/clean-transcript".

*Note: converted from a folded `>` YAML block to a single quoted line per the rewrite rules; `argument-hint` and `allowed-tools` keys untouched.*

---

## 6. decide (496 → 184)

**Old:**
> Choose between a dynamic workflow, a loop, and an agent team for a large multi-step task — then map which available skills slot into each phase of it. Use when Carter says "/decide", "decide how to do this", "how should I run this", "what process for this", "plan the process", or is about to hand off a large multi-step job and wants the shape and the skill-routing planned before launch. Deliberately out of scope for small tasks — inline work and plain subagent fan-out are excluded by design.

**New:**
> Pick workflow vs loop vs agent team for a large multi-step task and route skills to phases. Use when: "/decide", "decide how to do this", "plan the process". Not for small tasks.

---

## 7. architecture-review (465 → 185) — revised in fix round 1

**Old:**
> Software architecture reviewer specializing in modern patterns, distributed systems, and clean architecture. Evaluates scalability, resilience, security, and maintainability of system designs. Use when: "review the architecture", "architecture review", "evaluate this design", "assess scalability", "review microservices boundaries", "check architectural compliance", or when proposing major design changes. Do NOT use for small code reviews or minor local changes.

**New (round 1 fix):**
> Review architecture — scalability, resilience, security, maintainability. Use when: "review the architecture", "review microservices boundaries", "check architectural compliance".

*Note: converted from a folded `>` YAML block to a single quoted line; `allowed-tools` untouched.*

*Fix round 1 (finding 3): initial trim dropped "review microservices boundaries" and "check
architectural compliance" — two verbatim trigger phrases. Restored both. To fit under 200,
dropped "and major design changes" (the "scalability/resilience/security/maintainability" nouns
still cover design-change reviews) and dropped the "Not for small code reviews" exclusion
(routing coverage still holds via the positive trigger phrases; it's the smallest cut that made
room for both restored phrases). 198 → 185.*

---

## 8. github-digest (459 → 179)

**Old** (verbatim, as written in the source's folded `>` YAML block):
```
Daily GitHub trending digest. Harvests repo mentions from email-tracker's
sidecar JSON, cross-references with github.com/trending + OSS Insight,
filters by velocity + Carter's topic interests, posts one-liners to Slack
#github-repos, and writes a full README-based breakdown to
~/Research/ai-digest/github-trending/. Cron-friendly — no interactive steps.
Use when:
- "github digest"
- "what's trending on github"
- "run github digest"
- "check trending repos"
```

**New:**
> Daily GitHub trending digest — posts to Slack #github-repos, writes breakdown to ~/Research/ai-digest/github-trending/. Use when: "github digest", "what's trending on github".

*Note: converted from a folded `>` YAML block (with a nested `Use when:` list) to a single quoted line; `argument-hint` and `allowed-tools` untouched. The email-tracker/OSS-Insight sourcing mechanism is body detail, not a routing signal — dropped.*

---

## 9. tdd (447 → 177) — revised in fix round 1

**Old:**
> Test-Driven Development methodology enforcer. Enforces the Red-Green-Refactor cycle: write a failing test first, write minimal code to pass, then refactor. Iron Law: no production code without a failing test. Use when: "use TDD", "test driven development", "write tests first", "red green refactor", "TDD workflow", or when the user wants to build a feature test-first. Do NOT use for adding tests after the fact — use unit-test-generator instead.

**New (round 1 fix):**
> Red-Green-Refactor TDD: write a failing test first, then minimal code to pass. Use when: "use TDD", "test driven development", "write tests first", "red green refactor".

*Note: dropped "— use unit-test-generator instead" — no `unit-test-generator` skill exists anywhere in `~/.claude/skills/`, so the reference didn't route to anything.*

*Fix round 1 (finding 2): initial trim dropped the spelled-out "test driven development" trigger,
keeping only acronym-based phrases. Restored it. To make room, tightened "Enforce Red-Green-
Refactor TDD: failing test first, minimal code to pass, then refactor" to "Red-Green-Refactor TDD:
write a failing test first, then minimal code to pass" (same content, fewer words) and dropped the
trailing "Not for adding tests after the fact" exclusion — it referenced the same nonexistent
unit-test-generator skill, so it wasn't doing real routing work. 195 → 177.*

---

## 10. pdf (437 → 146)

**Old:**
> Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.

**New:**
> Read, extract, merge, split, rotate, watermark, encrypt, fill forms, or OCR PDF files (.pdf). Use whenever a .pdf is mentioned or needs producing.

---

## Totals (these 10 skills, per inventory script)

| | chars |
|---|---|
| Before | 6,099 |
| After round 1 (initial trim) | 1,986 |
| After fix round 1 | 1,969 |
| Reduction (before → fix round 1) | 4,130 (68%) |

## Totals (full KEEP catalog, 48 skills, per inventory script)

| | chars |
|---|---|
| Before | 18,331 |
| After initial trim | 14,218 |
| After fix round 1 | 14,201 |
| Reduction (before → fix round 1) | 4,130 (23%) |
