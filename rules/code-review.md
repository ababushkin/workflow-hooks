# Code review gate — completion requirement

This rule applies to every issue, regardless of tracker. Before any piece of work is declared done, the work must be reviewed, every blocking finding fixed, and the result committed and pushed — in that order.

---

## The gate

1. **Review** — Review the working-tree changes for correctness, readability, architecture, security, and performance.
2. **Fix** — Address any Critical or Required findings. Lower-severity findings are at the agent's discretion (fix inline or note in the completion summary).
3. **Commit + push** — Commit the reviewed version and push to the remote branch. Work that exists only locally is not done.

The gate is sequential: Review → Fix → Commit + push. Skipping or reordering is not permitted.

The review step is owned by Shaper's `exec:review` skill (multi-persona spec-compliance / security / code-quality fan-out to a single GO/NO-GO verdict); `exec:finish` owns the post-gate completion summary and tracker transition; `exec:pickup` orchestrates the whole sequence end-to-end. Defer to those skills — this rule is the tracker-agnostic statement of the invariant they enforce.

---

## Rationale

The gate exists because "compiles and tests pass" is not the same as "correct, maintainable, and safe to merge." Critical findings left unaddressed become production incidents; unreviewed pushes bypass the only asymmetric-judgement checkpoint in an agentic workflow. The gate makes the review step non-negotiable and its output visible (via the completion summary posted by the caller).

---

## Caller responsibilities

After the gate completes, the caller (the issue workflow, the skill, the human) is responsible for:
- Posting a completion summary that states the count of findings by severity and what was fixed vs deferred.
- Transitioning the work item to its terminal state in the tracker.

These steps are tracker-specific and are documented in the tracker's workflow rules (e.g. `linear-workflow.md`). When Shaper is installed, `exec:finish` performs both.
