# Workflow

Hook-injected workflow governance for Claude Code teams — code review gate, writing review gate, Linear lifecycle, and delivery-issue adapter.

Delivered entirely via hooks: a `SessionStart` hook injects `rules/GOVERNANCE.md` into every session, making the governance rules always-on without any skill invocation. The rules files (`rules/code-review.md`, `rules/linear-workflow.md`) are referenced from the index and loaded on demand.

## Writing-review gate

The `SessionStart` injection makes the governance rules always-on, but injected text is advisory — the model can still skip a step. One step is enforced by machinery instead: a `PreToolUse` hook on `ExitPlanMode` (`hooks/exit-plan-writing-gate.sh`) blocks plan finalization until a writing-refinement pass has run in the session.

The hook reads the session transcript and looks for a sub-agent (`Agent`/`Task`) or `Skill` call whose input mentions `writing-refinement`. If none is found, it denies `ExitPlanMode` with a reason telling the model to run the refinement pass and retry. The model dispatches the refiner, applies its findings, and calls `ExitPlanMode` again — this time it passes.

- **Alternative refiners** must carry the `writing[-_ ]?refinement` marker in the dispatching call (the sub-agent prompt, `subagent_type`, or skill name) to satisfy the gate.
- **Bypass:** set `WORKFLOW_HOOKS_WRITING_GATE=off` to disable the gate without uninstalling.
- The hook fails open — a missing or unreadable transcript allows the call through rather than wedging plan mode.

The gate covers `ExitPlanMode` only. The broader rule ("anything written to a file or an external system") stays on the soft `SessionStart` injection.

## Install

### Recommended — marketplace install

Add the marketplace, then install the `workflow-hooks` plugin:

```
/plugin marketplace add ababushkin/workflow-hooks
/plugin install workflow-hooks@workflow-hooks
```

Or with the `claude` CLI:

```bash
claude plugin marketplace add ababushkin/workflow-hooks
claude plugin install workflow-hooks@workflow-hooks
```

After install, run `/reload-plugins` to activate. The governance rules take effect at the next session start.

### Alternative — direct GitHub install

Install from GitHub without adding the marketplace:

```
/plugin install github@ababushkin/workflow-hooks
```

## Iterate loop (developers)

After cloning the repo and making changes:

1. **Edit** — modify rules in `rules/`, hooks in `hooks/hooks.json`, or bin scripts in `bin/`.
2. **Bump version** — increment the `version` field in `.claude-plugin/plugin.json` (semver: `0.1.1` → `0.1.2`).
3. **Push** — `git push` to the `main` branch.
4. **Update** — users pick up the new version by running:

```
/plugin marketplace update workflow-hooks
/reload-plugins
```

Or with the CLI (then restart Claude Code):

```bash
claude plugin marketplace update workflow-hooks
```

Auto-update is supported — users can enable it via the `/plugin` → Marketplaces tab to receive updates automatically at session start.

## License

MIT
