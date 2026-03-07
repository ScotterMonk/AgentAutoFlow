---
name: simplification
description: Finds insights that eliminate multiple components at once — "if this is true, we don't need X, Y, or Z." Use this skill whenever you notice the same concept implemented multiple ways, a growing list of special cases, complexity that keeps spiraling, or when you hear "we just need to add one more case." Also trigger when refactoring feels like whack-a-mole, config files are growing, or someone says "don't touch that, it's complicated." Trigger immediately when asked to add yet another special case to an already long list. Otherwise known as "Simplification Cascades" — one insight that collapses 10 things at once.
---

# Simplification Cascades

One insight can eliminate 10 components. Look for the unifying principle that makes multiple things unnecessary *simultaneously*.

**Core principle**: "Everything is a special case of X" collapses complexity dramatically.

**Critical constraint**: Always present the cascade proposal and get user approval before making changes. Never restructure silently.

---

## Before You Start — Disqualifiers

Check these *disqualifiers* first. If any apply, stop and explain why a cascade won't work here:
- **Things are only superficially similar**. *Why?* Same name ≠ same concept.
- **The abstraction needs more config than what it replaces**. *Why?* Net complexity increase.
- **Unifying would lose type safety or meaningful errors**. *Why?* Cost exceeds benefit.
- **The result would be harder to understand**. *Why?* Cascade must be *obvious*.

A valid cascade makes code **obviously simpler**, not just shorter.

---

## Triggers — When to Apply This Skill

| Symptom | Signal |
|---------|--------|
| Same concept implemented 5+ ways | Abstract the common pattern |
| Growing special-case list | Find the general case |
| Complex rules with exceptions | Find the rule with no exceptions |
| Excessive config options | Find defaults that cover 95% |
| Refactoring breaks something else | Missing abstraction layer |
| "Don't touch that, it's complicated" | Complexity hiding a cascade |
| "Just one more case..." (repeating) | You need the general form |

---

## Process

### 1. Gather all variations
List every place the same concept appears differently. Don't analyze yet — just enumerate.

### 2. Find the unifying essence
Ask: *"What is the same underneath all of these?"*

Look for:
- "We need to handle A, B, C, D differently..." — maybe they're the same thing with different parameters
- Rules with many exceptions — find the rule that has no exceptions
- Components that exist only to compensate for another component's rigidity

Name it in one sentence:
> "All of these are just `___` with different `___`."

If you can't write that sentence cleanly, you haven't found the right abstraction yet.

### 3. Measure the cascade depth
Count how many files, functions, and systems become **unnecessary** — not just renamed.

| Cascade depth | Interpretation |
|---|---|
| 1–2 things eliminated | Refactor, not a cascade |
| 3–5 things eliminated | Solid cascade — worth pursuing |
| 6+ things eliminated | Major cascade — high impact, verify carefully |

### 4. Stress-test the abstraction
Do all existing cases fit cleanly? If you need carve-outs or special-case parameters to make the edge cases work, the abstraction is probably wrong. Go back to step 2.

### 5. Present the proposal (required)
Use the template below. Get approval before touching any code.

---

## Proposal Template

```
## Simplification Cascade Found

**Current complexity**: [X implementations / Y special cases / Z config flags]

**Insight**: "Everything is a special case of [unified concept]"

**Abstraction**: [One sentence describing the unified pattern]

**What gets eliminated**:
- [Component A] — replaced by [unified abstraction]
- [Component B] — replaced by [unified abstraction]
- [Component C] — no longer needed at all

**What remains**: [Describe the leaner result]

**Cascade depth**: [N files / functions / systems eliminated]

**Risk**: [Edge cases that need verification]

**Approach**: [How you'll implement — phased or all-at-once]
```

Wait for explicit approval before proceeding.

---

## Examples

### Stream Abstraction
**Before**: Separate handlers for batch / real-time / file / network data
**Insight**: "All inputs are streams — just different sources"
**After**: One stream processor, multiple pluggable sources
**Eliminated**: 4 separate implementations

### Resource Governance
**Before**: Session tracking, rate limiting, file validation, connection pooling (all separate)
**Insight**: "All are per-entity resource limits"
**After**: One `ResourceGovernor` with 4 resource types
**Eliminated**: 4 custom enforcement systems

### Immutability
**Before**: Defensive copying, locking, cache invalidation, temporal coupling (all separate)
**Insight**: "Treat everything as immutable data + transformations"
**After**: Functional programming patterns
**Eliminated**: Entire categories of synchronization bugs
