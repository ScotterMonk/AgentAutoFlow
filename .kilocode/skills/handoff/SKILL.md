---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use this skill whenever the user asks for a handoff, continuation note, session summary for another agent, compacted context, or a document that lets a fresh agent continue the work.
argument-hint: What will the next session be used for?
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to a path produced by `mktemp -t handoff-XXXXXX.md` and read the file before you write to it.

Suggest the skills to be used, if any, by the next session.

Do not duplicate content already captured in other artifacts such as PRDs, plans, ADRs, issues, commits, or diffs. Reference them by path or URL instead.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the document accordingly.

## Handoff document guidance

Include only context that helps the next agent continue efficiently:

- **Purpose**: What the next session is meant to accomplish.
- **Current state**: What has already been done in this conversation.
- **Key decisions**: Decisions made, constraints accepted, and rationale that is not already captured elsewhere.
- **Relevant paths or URLs**: References to files, plans, issues, commits, diffs, or external resources the next agent should read.
- **Open tasks**: Concrete remaining work, blockers, risks, and verification steps.
- **Suggested skills**: Skills that the next agent should consider loading, with brief reasons.

Keep the handoff concise, factual, and action-oriented. Do not include unrelated transcript detail, speculation, or duplicated long-form artifacts.
