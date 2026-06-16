# Code review gate — completion requirement

Every coding task must pass this gate before it's considered done:

1. Review — Check your changes for correctness, readability, architecture, security, and performance.
2. Fix — Resolve all Critical/Required findings. Use your judgment on lower-severity ones (fix them or note them in your summary).
3. Commit & push — Commit and push to the remote branch. Local-only work is not done.

These steps must happen in order. No skipping, no reordering.

To run the review, use exec:review via agent-skills-shaper (or a preferred alternative if you have one installed). Launch it as a sub-agent.

## Caller responsibilities

After the gate completes, the caller (the issue workflow, the skill, the human) is responsible for:
- Posting a completion summary that states the count of findings by severity and what was fixed vs deferred.
- Transitioning the work item to its terminal state in the tracker.

These steps are tracker-specific and are documented in the tracker's workflow rules (e.g. `linear-workflow.md`). When Shaper is installed, `exec:finish` performs both.
