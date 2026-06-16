# Linear workflow

## Working on tasks

If a task is tracked in Linear, follow this workflow (unless instructed otherwise):

1. Move to **In Progress** via `mcp__claude_ai_Linear__save_issue`.
2. If your work consists of slices that are written up as tasks in the Linear issue, then cross off those tasks as you go in the Linear issue and drop a comment with your progress as you go.
3. When you're done coding, move the issue to In Review and then proceed ahead with any other steps in your queue (eg. a code-review or any other review tasks in your queue).
4. Do not merge immediately, instead open a PR and follow any specific PR workflow you've been given. Keep the issue In Review.

## Creating a project

1. **Create the Linear project** via `mcp__claude_ai_Linear__save_project`:
   - `name`: the project/initiative goal name (a goal or problem name, not a repo name and not a solution name)
   - `description`: the full description you've been given
   - `state`: `"planned"`

2. **Create the seed issues** via `mcp__claude_ai_Linear__save_issue` for each issue identified during shaping:
   - Assign each to the project created in step 1
   - Leave cycle unset (cycle assignment happens at planning day)
   - Set status to `"Backlog"`

3. **Confirm** by reading back the project (`mcp__claude_ai_Linear__get_project`) and verifying the description persisted correctly.
