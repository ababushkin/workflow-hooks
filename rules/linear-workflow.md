# Linear workflow

Tracker instance metadata lives in `.linear_config` at the repo root — `team` (required) and
`ops_project`, where `team` accepts a Linear team name or ID. **Read it before any create or
capture call** and use its values in the calls below. If the file is absent, ask the operator
for the team and offer to create it.

## Working on tasks

If a task is tracked in Linear, follow this workflow (unless instructed otherwise):

1. Move to **In Progress** via `mcp__claude_ai_Linear__save_issue` (`state: "In Progress"` resolves by name; if a name doesn't resolve, `mcp__claude_ai_Linear__list_issue_statuses` lists the team's exact status names).
2. If your work consists of slices written up as tasks in the issue, cross them off as you go and drop a progress comment via `mcp__claude_ai_Linear__save_comment` (`issueId` + `body`). Crossing off a task edits the issue description, and `save_issue`'s `description` **overwrites the whole body** — so `mcp__claude_ai_Linear__get_issue` first, flip `- [ ]` → `- [x]` in the returned markdown, then save the full body back, or you will clobber the rest.
3. When you're done coding, move the issue to In Review and then proceed with any other steps in your queue (e.g. a code-review or other review tasks).
4. Do not merge immediately; open a PR and follow any specific PR workflow you've been given. Keep the issue In Review.

## Creating a project

1. **Create the Linear project** via `mcp__claude_ai_Linear__save_project`:
   - `name`: the project/initiative goal name (a goal or problem name, not a repo name and not a solution name)
   - `description`: the full description you've been given
   - `state`: `"planned"`
   - `addTeams`: `["<team from .linear_config>"]` — a team is **required** on create

2. **Create the seed issues** via `mcp__claude_ai_Linear__save_issue` for each issue identified during shaping:
   - `title` and `team` (from `.linear_config`) are required on create
   - `project`: the project from step 1 (name, ID, or slug) — this attaches the issue
   - `state`: `"Backlog"`
   - Omit `cycle` (cycle assignment happens at planning day)

3. **Confirm** by reading back the project (`mcp__claude_ai_Linear__get_project`) and verifying the description persisted correctly.

## Loose / ops issues

A one-off bug, KTLO item, or other issue not tied to an initiative is created with `project` set to
the `ops_project` named in `.linear_config`. The MCP cannot clear a project assignment, so loose issues
need a standing home rather than being left project-less.
