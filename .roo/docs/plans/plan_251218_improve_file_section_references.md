# File & Section Reference Standardization

Standardize file/section references in Roo Code Custom Mode files.

## Plan to follow

**Goal**: For each file listed below, modify file/section references:
- `.roo/rules/01-general.md`
- `.roo/rules/02-database.md`
- `.roo/rules/03-planning.md`
- `.roo/rules-architect/01-architect.md`
- `.roo/rules-planner-a/01-planner-a.md`
- `.roo/rules-planner-b/01-planner-b.md`
- `.roo/rules-planner-c/01-planner-c.md`
- `.roo/rules-orchestrator/01-orchestrator.md`
- `.roo/rules-code/01-code.md`
- `.roo/rules-code-monkey/01-code-monkey.md`
- `.roo/rules-front-end/01-front-end.md`
- `.roo/rules-tester/01-tester.md`
- `.roo/rules-debug/01-debug.md`
- `.roo/rules-githubber/01-githubber.md`
- `.roo/rules-task-simple/01-task-simple.md`
- `.roo/rules-ask/01-ask.md`
- `.roo/rules-ask/02-ask-health.md`
- `.roo/rules-ask/03-ask-flora-growing.md`

## Instructions for Standardizing References

For every file, run all applicable parts of the file through the following checklist:

### 1) File References
**Always use backticks without markdown links:**
- Good: `` `agents.md` ``
- Good: `` `.roo/rules/01-general.md` ``
- Bad: `[agents.md](agents.md)`
- Bad: `agents.md` (no backticks)

### 2) Section References
**Use "in" not ">" for section references:**
- Good: `See Critical Resources in .roo/rules/01-general.md`
- Good: `See Testing Guidance in agents.md`
- Bad: `` `agents.md` > Testing Guidance``
- Bad: `` `.roo/rules/01-general.md` > Critical Resources``

### 3) Combined Reference Pattern
**Format:** `See <Section Name> in <file.md>`
```markdown
See `Database` section in `.roo/rules/02-database.md`
coordinate per `Testing Guidance` in `agents.md`
Follow `Browser Testing` section in `.roo/rules/01-general.md`
```

### 4) Find & Replace Pattern
**Search for:** `<file.md> > <Section>`
**Replace with:** `<Section> in <file.md>`

**Example:**
- Before: `` `agents.md` > Testing Guidance``
- After: `` `Testing Guidance` in `agents.md` ``

## Execution Steps
1) Open target file
2) Search for patterns containing " > " between file and section
3) Reformat to use " in " pattern
4) Verify backticks surround both file paths and section names
5) Save file
