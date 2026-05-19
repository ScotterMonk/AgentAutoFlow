---
name: login-using-querystring
description: For debugging, testing, or any purpose a mode may have for browsing the app's web site.
---

# Login instructions

Read local `AGENTS.md` in this skill folder if it exists for project-specific login URL, host restrictions, and credential lookup.

Generic workflow:
- Confirm the target app supports querystring login before using this shortcut.
- Confirm the shortcut is restricted to safe local or test hosts.
- Retrieve credentials from the project's approved secret source; never hard-code them.
- Use `browser-use` skill for browsing and verification.
