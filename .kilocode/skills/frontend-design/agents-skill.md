# Front-end Specifics to this application

- Templates:
    - Ensure VS Code uses `jinja-html` mode when editing Jinja/HTML templates.
    - Maintain or improve semantic HTML and accessibility (labels, alt text, headings; follow existing patterns).
    - Keep template logic minimal; do not add backend-like logic into templates.
- CSS:
    - Consolidate all styles in `static/css/main.css`.
    - Follow existing spacing, typography, and color tokens where present.
    - Prefer utility/class-based patterns that are already used across the app.
    - Add new tokens/utilities only when necessary and ensure they are consistent with the existing design system.
- Client-side JS:
    - Use progressive enhancement: pages should degrade gracefully if JS is disabled.
    - Keep JS modular and located under `static/js/`, not inline in templates unless explicitly justified.
    - Align JS structure with Core vs Presentation patterns described in `agents.md` (avoid mixing backend concerns in JS).
- Cross-file impact:
    - When editing a template, evaluate related CSS and JS for consistency and possible regressions.
    - When changing CSS, identify all templates affected by modified selectors.
- Consistency over novelty:
    - Prefer aligning with existing page layouts and patterns rather than introducing completely new layout paradigms.
