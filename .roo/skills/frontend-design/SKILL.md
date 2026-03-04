---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with exceptional design quality. Use this skill any time the user asks to build, design, style, or beautify a web UI — including components, pages, dashboards, landing pages, posters, HTML/CSS layouts, Flask/Jinja templates, React or Vue components, or any visual artifact. Trigger even for partial requests like "make this look better", "style this page", "add animations", "improve the layout", or "design a card". If the request involves any visual output for the web, use this skill.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Every output should feel genuinely designed — not assembled from defaults.

## Workflow

### 1. Understand context
Before touching code:
- **Purpose**: What problem does this solve? Who is the audience?
- **Stack**: HTML/CSS/JS? Flask/Jinja? React/Vue? Match the output to the project's tech.
- **Constraints**: Performance, accessibility, existing design system, color/brand requirements.

### 2. Commit to a bold aesthetic direction
Pick one and execute it with precision — don't blend generically:

| Direction | Character |
|---|---|
| Brutally minimal | Extreme whitespace, monochrome, one accent |
| Maximalist | Dense, layered, every surface textured |
| Retro-futuristic | CRT effects, scanlines, phosphor glows |
| Organic/natural | Earthy tones, irregular shapes, soft grain |
| Luxury/refined | Tight tracking, serif type, deep neutrals |
| Playful/toy-like | Rounded forms, saturated palettes, bounce |
| Editorial/magazine | Oversized type, ruled lines, offset grids |
| Industrial/utilitarian | Raw surfaces, monospace type, functional density |

**The one thing:** Identify what makes this design *unforgettable* — one surprising detail, layout break, or visual moment that anchors the whole piece.

### 3. Implement

Build working code that is production-grade, visually striking, and cohesive. For Flask/Jinja projects, output valid template syntax. For standalone work, output self-contained HTML/CSS/JS.

---

## Aesthetic Standards

### Typography
- Pair a distinctive **display font** (headings) with a refined **body font**.
- Source from Google Fonts, Adobe Fonts, or system variable fonts — never system-ui defaults.
- **Never use**: Inter, Roboto, Arial, Helvetica, system-ui, sans-serif as a primary choice.
- Vary weight, size, tracking dramatically. Let type carry visual weight.

### Color
- Use CSS custom properties (`--color-*`) for all palette values.
- Commit to a dominant color with **sharp accents** — avoid evenly distributed "tasteful" palettes.
- Light *and* dark themes are both valid — vary across designs, never default to one.
- **Never use**: purple-on-white gradients, generic blue CTAs, gray placeholder schemes.

### Motion
- CSS-only preferred for HTML; Motion library for React.
- One well-orchestrated **page load** (staggered reveals via `animation-delay`) beats scattered micro-interactions.
- Use scroll-triggered reveals and hover states that genuinely surprise.
- Match motion intensity to the aesthetic — minimalist designs get subtle easing, not bounces.

### Layout & Space
- Break the grid deliberately: asymmetry, overlap, diagonal flow, pinned elements.
- Generous negative space **or** controlled density — not the safe middle.
- Grid-breaking hero elements, offset section headers, bleed images.

### Backgrounds & Depth
- No solid flat backgrounds. Add atmosphere: gradient meshes, noise textures, geometric patterns, layered SVG, grain overlays.
- Dramatic shadows, glows, or depth via `backdrop-filter` and layered `box-shadow`.
- Match the texture to the aesthetic — don't apply grain to a clean luxury design.

---

## Anti-Patterns (Never Do)

- Generic font families as primary choices (Inter, Roboto, Arial, system fonts)
- Purple gradients on white — or any clichéd startup color scheme
- Predictable card → header → CTA layouts without intentional deviation
- Cookie-cutter component patterns that lack context-specific character
- Converging on the same aesthetic across different generations (Space Grotesk, glassmorphism, etc.)

---

## Output Checklist

Before finishing, verify:
- [ ] Aesthetic direction is clear and intentional — not a blend of defaults
- [ ] Typography uses distinctive, non-generic font choices
- [ ] Color scheme uses CSS variables with a dominant + accent structure
- [ ] At least one layout surprise or visual moment worth remembering
- [ ] Animations serve the aesthetic and don't feel scattered
- [ ] Code is production-ready and functional (no placeholder logic)
- [ ] For Flask/Jinja: template syntax is valid and extends the appropriate base
