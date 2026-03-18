---
name: github-use
description: Any time github or git activity is required, including committing and pushing changes, creating or switching branches, merging, creating issues, checking status or logs, or reverting commits. Trigger whenever the user says "update", "commit", "push", "merge", "create branch", "checkout", "create issue", "git status", "revert", or any git/GitHub-related request — even if not framed explicitly as a "GitHub task."
---

# Command index
- **update**: Stage, commit, and push all changes. See "## Update".
- **merge to main**: Merge current branch into main. See "## Merge to main".
- **create issue**: Create a new GitHub issue. See "## Create issue".
- **create branch**: Create a new branch from current branch and switch to it. See "## Create branch".
- **checkout branch**: Switch to an existing branch. See "## Checkout branch".
- **list branches**: List all branches. See "## List branches".
- **revert**: Revert a specific commit by hash. See "## Revert".
- **status**: Show working tree state. See "## Status".
- **log**: Show recent commit history. See "## Log".
- **branch**: Show current branch name. See "## Branch".

# Environment
- **Shell**: Windows PowerShell in VS Code.
- **Virtual environment**: *If deactivated*, reactivate with `./activate` *before and separate from other commands*. *Only do this once, at the start and only if needed.*

# Response style
- Skip narration ("Now I will…"). Just act and report at the end.
- **Success**: One summary line + key details (branch, commit hash, sync status).
- **Failure**: One summary line + key error snippet + one or two concrete next steps.

> Example success: `Update complete: 3 files committed on branch feature/x, pushed to origin/feature/x; local and remote are in sync.`

# General rules (all workflows)

**Error handling**: Stop at the first error, capture the output, and give the user troubleshooting options rather than continuing blindly.

**Authority**: Run all git commands without asking permission. Just execute and report.

**Prohibited**:
- No `git push --force` or `--force-with-lease` on main.
- No `git rebase` on main.

**Remote**: Default to `origin` unless the user specifies otherwise.

**Command chaining**: Run each git command separately — never chain with `;` or `&&`.

**Backticks in commit messages**: PowerShell treats `` ` `` as an escape character, so never use backticks in commit message text. Write identifiers as plain text (e.g., `_derive_source`, not `` `_derive_source` ``).

# Command workflows

## Update
Stage, commit, and push all changes to the remote.

1. **Status check**: `git status` — see all modified, untracked, and staged files.
2. **Research changes**: Understand *what* changed and *why*, not just which files changed. Use `codebase_search`, `read_file`, or `search_files` as needed. A meaningful commit message describes the work, not just the filenames.
3. **Stage all changes**: `git add -A` (handle special cases as needed).
4. **Craft commit message**:
   - Concise subject line.
   - Short but complete body: what was done and why.
   - List affected file paths.
   - No backticks.
   - No carriage returns or line feeds within the message. Enclose the full message in quotes as a single `-m` argument.
      **Wrong** (has line feeds or carriage returns):
      ```
      git commit -m "Fix...

      - An item that was changed...
      - Another item that was changed...

      Files: file.py, another_file.py"
      ```

      **Right** (no line feeds or carriage returns):
      ```
      git commit -m "Fix...: (1) An item that was changed... (2) Another item that was changed... Files: file.py, another_file.py"
      ```
5. **Commit**: `git commit -m "[message]"` — no permission needed, just run it.
6. **Verify**: Confirm commit succeeded and note the hash.
7. **Push**: `git push origin <branch>`. If credentials are requested, check the `Critical Resources` section in `{base folder}/{scaffold folder}/rules/01-general.md`.
8. **Confirm sync**: Verify local and remote are in sync.

## Create branch
Create a new branch and switch to it.

1. **Branch name**: If not provided, stop and ask. Prefer `feature/<short-name>` or `fix/<short-name>`.
2. **Current state**: `git branch --show-current` then `git status -sb`. Note any uncommitted changes — they carry over to the new branch.
3. **Validate name**: `git check-ref-format --branch "<branch_name>"`. If invalid, stop and tell the user why.
4. **Existence check**: Confirm the branch doesn't already exist locally. If it does, suggest the **checkout branch** workflow.
5. **Create and switch**: `git switch -c <branch_name>`.
6. **Verify**: Confirm the active branch is now the new one.

## Checkout branch
Switch to an existing branch.

1. **Branch name**: If not provided, stop and ask (or show available branches with `git branch -a` first).
2. **Dirty check**: `git status -sb` — if uncommitted changes exist, warn the user they won't automatically carry over. Do not auto-stash; let the user decide.
3. **Switch**: `git switch <branch_name>`.
4. **Verify**: Confirm the active branch is the requested one.

## List branches
1. `git branch -a` — shows all local and remote-tracking branches.
2. Clearly indicate which branch is currently active.

## Create issue
Create a GitHub issue using the `gh` CLI.

1. **Collect info**: If title or body is missing, ask for them before proceeding.
2. **Create**: `gh issue create --title "<title>" --body "<body>"`.
   - If `gh` is not installed or not authenticated, stop and report that to the user.
3. **Confirm**: Share the new issue URL.

## Revert
Revert a specific commit by creating a new undo commit — history is preserved, nothing is deleted.

1. **Confirm hash**: If not provided, show `git log --oneline -n 10` to help the user identify the target commit, then ask.
2. **Revert**: `git revert <hash>`.
3. **Verify**: `git log --oneline -n 5` to confirm the revert commit was created.
4. **Push**: Ask the user if they want to push the revert to the remote.

## Merge to main
Merge the current branch into main.

1. **Identify branch**: `git branch --show-current` — store the name for later.
2. **Clean check**: `git status -sb` — if uncommitted changes exist, stop and run the **Update** workflow first. Do not auto-stash or discard anything.
3. **Fetch**: `git fetch origin` to sync remote state before merging.
4. **Switch to main**: `git checkout main`. If it doesn't exist locally, create it tracking `origin/main`.
5. **Pull main**: `git pull origin main` — ensure main is current.
6. **Merge**: `git merge --no-ff <branch_name> -m "<descriptive merge message>"`. Using `--no-ff` keeps an explicit merge commit in history, making it easier to trace what was introduced.
   - On conflicts: list conflicting files, stop, and summarize so the user can resolve manually. Do not attempt destructive auto-resolution.
7. **Verify**: `git log --oneline -n 5` — confirm the merge commit is present.
8. **Push main**: `git push origin main`. Handle credentials via `Critical Resources` in `{base folder}/{scaffold folder}/rules/01-general.md`.
9. **Confirm sync**: Verify local and remote main are in sync.
10. **Restore context**: Optionally switch back to the original branch so the user can continue working.

## Status
`git status -sb` → briefly state the working tree state (clean, changes pending, etc.).

## Log
`git log --oneline -n 10` → show recent history without excessive output.

## Branch
`git branch --show-current` → state the branch name plainly.
