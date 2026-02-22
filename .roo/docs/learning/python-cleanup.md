## Remove unused imports.
<!-- meta: date=2026-02-21, tier=2, status=active -->
- **Trigger/Symptom**: A Python utility script has imports that are never referenced.
- **Cause/Mistake**: Leftover imports from prior iterations (often from planned exception handling) that no longer match the code.
- **Fix/Correct**: Remove unused imports promptly; validate quickly with `py_compile` or `py -m compileall`.
- **Why**: Prevents misleading dependency signals and keeps scripts easier to maintain.
