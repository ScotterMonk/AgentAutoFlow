---
name: resolve-ambiguity
description: >
  Systematic ambiguity resolution through information gathering.
  Use when facing unclear requirements, unknown context, uncertain
  implementation choices, or any situation where guessing would be risky.
  Also use when another skill or rule directs you here via an ambiguity gate.
---

# Resolve Ambiguity

## When to Use

Use this skill when:
- A request has multiple plausible interpretations
- Key details (objective, scope, constraints, environment, or safety) are unclear
- You catch yourself thinking "probably", "I assume", "likely means", or "I'll go with X"
- Another skill or rule's **ambiguity gate** directed you here
- You are choosing between 2+ implementation approaches and the user hasn't indicated preference

## When NOT to Use

Do not use this skill when:
- The request is unambiguous AND all scope/constraint details are clear
- A discovery read has **already answered** the specific question (not just provided more context)

**Important**: "I can probably figure it out" is NOT a valid reason to skip this skill.
A discovery read that leaves you choosing between options means ambiguity is still present — ask.

## Goal

Surface assumptions to the user before they become wrong work.
Ask the minimum set of clarifying questions needed; do not start implementing
until must-have questions are answered (or the user explicitly approves
proceeding with stated assumptions).

**This skill composes with other skills** — after resolution, return to whatever
workflow step invoked you.

## Assumption Detection (Self-Check)

Before proceeding past this skill, verify you are not about to:
- Pick one interpretation over another without user input
- Choose a file/component scope the user didn't specify
- Infer "done" criteria the user didn't state
- Select an implementation approach the user didn't request

If you catch yourself doing any of these: **stop and ask**.

## Workflow

### 1) Decide whether the request is underspecified

Treat a request as underspecified if, after any discovery reads, SOME of the
following remain unclear:
- The objective (what should change vs. stay the same)
- "Done" criteria (acceptance criteria, examples, edge cases)
- Scope (which files/components/users are in/out)
- Constraints (compatibility, performance, style, deps, time)
- Environment (language/runtime versions, OS, build/test runner)
- Safety/reversibility (data migration, rollout/rollback, risk)

**Threshold**: If even ONE item above is ambiguous AND would change your approach,
the request is underspecified.

### 2) Ask must-have questions first (keep it small)

Ask 1–5 questions in the first pass. Prefer questions that eliminate whole
branches of work.

Make questions easy to answer:
- Optimize for scannability (short, numbered questions; avoid paragraphs)
- Offer multiple-choice options when possible
- Suggest reasonable defaults when appropriate (bold the recommended choice)
- Include a fast-path response (e.g., reply `defaults` to accept all defaults)
- Include a low-friction "not sure" option when helpful
- Separate "Need to know" from "Nice to know" if that reduces friction
- Structure options so the user can respond compactly (e.g., `1b 2a 3c`);
  restate chosen options in plain language to confirm

### 3) Pause before acting

Until must-have answers arrive:
- Do not run commands, edit files, or produce a detailed plan that depends on unknowns
- Low-risk discovery reads are allowed if they don't commit you to a direction

If the user explicitly asks you to proceed without answers:
- State your assumptions as a short numbered list
- Ask for confirmation; proceed only after they confirm or correct

### 4) Confirm interpretation, then proceed

Once you have answers, restate requirements in 1–3 sentences (including key
constraints and what success looks like), then **return to the calling
workflow step**.

## Question Templates

- "Before I start, I need: (1) ..., (2) ..., (3) .... If you don't care about (2), I'll assume ...."
- "Which of these should it be? A) ... B) ... C) ... (pick one)"
- "What would you consider 'done'? For example: ..."
- "Any constraints I must follow? If none, I'll target existing project defaults."

```text
1) Scope?
   a) Minimal change (default)
   b) Refactor while touching the area
   c) Not sure — use default
2) Compatibility target?
   a) Current project defaults (default)
   b) Also support older versions: <specify>
   c) Not sure — use default

Reply: defaults (or 1a 2a)
```

## Anti-patterns

- Asking questions you already answered via discovery read
- Asking open-ended questions when tight multiple-choice would work
- **Silently picking one interpretation when two are equally plausible**
- **Saying "I'll assume X" in your reasoning without surfacing X to the user**
- Skipping this skill because "I can probably figure it out"
