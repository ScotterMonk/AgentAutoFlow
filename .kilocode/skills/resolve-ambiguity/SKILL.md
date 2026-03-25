---
name: resolve-ambiguity
description: >
  Systematic ambiguity resolution through information gathering.
  Use when facing unclear requirements, unknown context, uncertain
  implementation choices, or any situation where guessing would be risky.
  Also use when another skill or rule directs you here via an ambiguity gate.
  Trigger this skill even for partial ambiguity — if you're weighing two
  approaches, unsure which files are in scope, or filling in gaps with
  "probably" or "I assume", that's ambiguity. Don't skip this skill just
  because you *could* guess; the cost of guessing wrong is wasted work.
---

# Resolve Ambiguity

## Why This Matters

Unresolved ambiguity is the #1 cause of wasted agent work. When you guess
wrong about scope, intent, or approach, the user has to reject your output and
start over — sometimes multiple times. Two quick questions up front routinely
save 10–30 minutes of rework. This skill exists to make that trade-off
automatic: a small pause now prevents a large redo later.

## When to Use

Use this skill when:
- A request has multiple plausible interpretations
- Key details (objective, scope, constraints, environment, or safety) are unclear
- You catch yourself thinking "probably", "I assume", "likely means", or
  "I'll go with X"
- Another skill or rule's **ambiguity gate** directed you here
- You are choosing between 2+ implementation approaches and the user hasn't
  indicated preference
- You're about to modify files the user didn't explicitly mention
- The request is broad ("improve this", "fix it", "make it better") without
  specific success criteria

## When NOT to Use

Do not use this skill when:
- The request is unambiguous AND all scope/constraint details are clear
- A discovery read has **already answered** the specific question — not just
  provided more context, but actually resolved the choice between alternatives

**Key distinction**: "I found more information" ≠ "ambiguity resolved."
If after reading code you still face a fork in the road, ambiguity persists — ask.

## Goal

Surface assumptions to the user before they become wrong work.
Ask the minimum set of clarifying questions needed; do not start implementing
until must-have questions are answered (or the user explicitly approves
proceeding with stated assumptions).

**This skill composes with other skills** — after resolution, return to
whatever workflow step invoked you.

---

## Workflow

### Step 1 — Discover before you ask

Before asking the user anything, try to answer your own questions through
low-risk exploration:

- **Read relevant files** — the target file, its imports, its callers, tests
- **Check project conventions** — AGENTS.md, config files, existing patterns
- **Search for prior art** — has something similar been done in the codebase?

Discovery reads are cheap. Questions interrupt the user's flow. Exhaust the
easy reads first, but set a limit: **if after 2–3 discovery reads you're still
choosing between alternatives, stop reading and ask**.

Discovery is for gathering facts, not for committing to a direction. If you
find yourself starting to implement during "discovery," you've gone too far.

### Step 2 — Classify what's unclear

After discovery, categorize remaining unknowns:

**Intent** — What should change vs. stay the same. Ex: "Improve the login" — UI? security? speed?
**Scope** — Which files, components, or users are in/out. Ex: "Update the tests" — all tests? just for this module?
**Done criteria** — How the user will judge success. Ex: "Make it faster" — 2x faster? sub-second? perceptibly?
**Approach** — Which of N valid implementation paths to take. Ex: Refactor in place vs. extract to new module.
**Constraints** — Compatibility, style, deps, performance bounds. Ex: Must it support Python 3.8? Stay under 600 lines?
**Safety** — Reversibility, data risk, rollout concerns. Ex: Will this break existing configs?

### Step 3 — Triage: blocking vs. deferrable

Not all ambiguity needs immediate resolution. Separate into two tiers:

**Blocking** (must resolve before any work):
- Would change which files you touch
- Would change the fundamental approach (refactor vs. patch, new file vs. edit)
- Has safety/data implications
- Affects whether the task is even possible

**Deferrable** (can use a reasonable default and mention it):
- Cosmetic preferences (naming, formatting details)
- Edge cases that don't affect the main path
- "Nice to know" context that won't change your first move

Only ask about blocking unknowns up front. For deferrables, state your
default assumption briefly and move on — the user can correct you later.

### Step 4 — Ask must-have questions (keep it small)

Ask **1–5 questions** in the first pass. Prefer questions that eliminate whole
branches of work.

**Make questions easy to answer:**
- Short, numbered questions — avoid paragraphs
- Offer multiple-choice options when feasible
- **Bold the recommended default**
- Include a fast-path response (e.g., "reply `defaults` to accept all defaults")
- Include "not sure — use default" as an option where helpful
- Separate "Need to know" from "Nice to know" if that reduces friction
- Structure options so the user can respond compactly (e.g., `1b 2a 3c`)

**Example — well-structured question set:**

```text
Before I start, a few quick questions:

1) Scope?
   a) Minimal change — just the reported issue  ← DEFAULT
   b) Refactor while touching the area
   c) Not sure — use default

2) Should existing tests still pass as-is, or expect test updates too?
   a) Tests must pass unchanged  ← DEFAULT
   b) Test updates are fine if behavior changes

Reply: defaults  (or e.g. 1b 2a)
```

### Step 5 — Pause before acting

Until must-have answers arrive:
- Do **not** run commands, edit files, or produce detailed plans that depend
  on unknowns
- Additional discovery reads are allowed if they don't commit you to a
  direction

**If the user explicitly asks you to proceed** without answering:
1. State your assumptions as a short numbered list
2. Ask for confirmation
3. Proceed only after they confirm or correct

### Step 6 — Confirm interpretation, then return

Once you have answers:
1. Restate the resolved requirements in **1–3 sentences** (include key
   constraints and what success looks like)
2. If the user answered compactly (e.g., `1b 2a`), restate in plain language
   so both sides confirm alignment
3. **Return to the calling workflow step** — reference it explicitly
   (e.g., "Returning to coding-init Step 2: Pre-planning")

---

## Assumption Detection (Self-Check)

Run this check **before leaving this skill**. If any item is true, you still
have unresolved ambiguity:

- [ ] Am I picking one interpretation over another without user input?
- [ ] Am I choosing files/components the user didn't specify or confirm?
- [ ] Am I inferring "done" criteria the user didn't state?
- [ ] Am I selecting an approach the user didn't request?
- [ ] Am I saying "I'll assume X" without having surfaced X to the user?
- [ ] Did I default to the simplest interpretation because it's easier, not
      because evidence supports it?

If any box would be checked: **stop and ask**.

---

## Handling Partial Answers

Users sometimes answer some questions and skip others. When this happens:

- **Answered questions**: Accept and integrate — do not re-ask
- **Skipped questions with a default**: Use the default you proposed; briefly
  note you're doing so (e.g., "Using default for scope: minimal change")
- **Skipped questions without a default**: Ask once more, briefly. If still
  skipped, state your best-guess assumption explicitly and proceed — the user's
  silence after two asks is implicit approval to use judgment

---

## Question Templates

Use these as starting points — adapt to context:

**Intent clarification:**
- "When you say '[user's phrase]', do you mean: A) ... B) ... C) ...?"
- "What would you consider 'done'? For example: ..."

**Scope clarification:**
- "Should I touch just [specific file/area], or also [related area]?"
- "This could affect [X, Y, Z]. Should I limit the change to [X] only?"

**Approach clarification:**
- "I see two paths: A) [option] — simpler, faster. B) [option] — more robust,
  more work. Which fits? (**A is my default**)"

**Constraint check:**
- "Any constraints I should know? If none, I'll follow existing project
  patterns."

**Compact format:**
```text
1) Scope?
   a) Just [specific area]  ← DEFAULT
   b) Also [adjacent area]
   c) Not sure — use default
2) Approach?
   a) Quick patch  ← DEFAULT
   b) Refactor while here
   c) Not sure — use default

Reply: defaults (or 1a 2b, etc.)
```

---

## Anti-Patterns and Their Fixes

**Silently picking one interpretation when two are equally plausible** — 50% chance of wasted work. Instead: ask a one-line question with choices.
**Saying "I'll assume X" in reasoning but not surfacing X to the user** — User can't correct what they can't see. Instead: state assumption openly in your response.
**Asking questions you already answered via discovery** — Wastes user's time, erodes trust. Instead: check your notes — don't re-ask answered questions.
**Asking open-ended questions when tight multiple-choice would work** — High friction, slow responses. Instead: offer A/B/C with a bolded default.
**Skipping this skill because "I can probably figure it out"** — "Probably" is the signal, not the solution. Instead: if you thought "probably", this skill applies.
**Over-asking: 10 questions before writing a line of code** — Frustrates user, signals lack of competence. Instead: limit to 1–5 blocking questions; defer the rest.
**Treating all ambiguity as blocking** — Delays work unnecessarily. Instead: triage — use defaults for deferrable items.
