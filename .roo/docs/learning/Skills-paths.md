# Skills — Paths

## Skill script paths must be relative to project root, not to the skill folder
<!-- meta: date=2026-02-21, tier=1, status=active -->
- **Trigger/Symptom**: Agent gets "file not found" when trying to run a script referenced in a SKILL.md
- **Cause/Mistake**: SKILL.md wrote paths relative to the skill's own folder (e.g., `python scripts/with_server.py`) — works only if the agent first `cd`s into the skill folder, which it won't do
- **Fix/Correct**: Always write full paths from project root in SKILL.md examples → `python .roo/skills/browser-use/scripts/with_server.py`
- **Why**: Agents execute terminal commands from the project root; relative paths in docs must match that CWD
