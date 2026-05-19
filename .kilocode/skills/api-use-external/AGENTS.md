# Skill-local agent guidance: api-use-external

This project is a Python file synchronization utility. It does not currently define external API providers.

## Project guidance
- Treat this skill as generic unless a task introduces a concrete external API.
- Keep API credentials out of skill files; use project configuration or environment files only when the application adds such integration.
- Prefer reusable provider abstractions over one-off HTTP calls if an external API integration is added later.

