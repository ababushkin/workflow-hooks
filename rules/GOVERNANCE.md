# Workflow governance

The always-on index for the `workflow` pack. The SessionStart hook injects this file every
session; the bulky governance modules are not injected — this index points to them. Inline
below are the short rules that must hold at all times. Linear is one module among several
in this pack, not the whole of governance. If this index and a module ever disagree, the
module is canonical and the drift is a bug — fix the index.

## Completion gate — always on

No work is done until, in order: **review** the working-tree changes → **fix** every Critical
and Required finding → **commit + push**. The steps are sequential; reordering or skipping is
not permitted. Work that exists only locally is not done. After the gate, the caller posts a
completion summary and transitions the work item to its terminal state — these steps are
tracker-specific (for Linear, see below).

This gate is owned by Shaper's `exec:review` (review) and `exec:finish` (summary + transition)
skills, orchestrated by `exec:pickup`; defer to them. Read `rules/code-review.md` for the full
tracker-agnostic gate and its rationale.

## Comments — always on

A comment explains the code *as it stands* — an invariant, a non-obvious constraint, a
workaround the next reader would otherwise trip on. It never narrates how the code came to
look this way. Never put in a comment: ticket / issue IDs (`ABA-NNN`), story or task labels,
commit SHAs, PR numbers, or fix-history narration ("added for…", "fixes the bug where…",
"previously this…"). That context belongs in the commit message, the PR, the Linear issue,
or a durable design record (an ADR under `docs/adrs/`, or `docs/design-decisions.md`). Fixing
an offending comment: strip the reference and keep the explanatory prose; reword if the label
was the grammatical subject; inline the explanation if it lived inside a parenthetical; delete
the comment if nothing of value remains. Leave alone: sample-data IDs in tests, schema placeholders
(`"issue_identifier": "ABA-NNN"`), and in-repo file paths (`README.md`).

- **Comment-as-smell.** If the only justification for a special-case branch or constant is a
  multi-line explanatory comment, prefer deleting the special case. A comment that explains
  *why this hack is needed* signals the design is wrong; remove the hack and the comment
  together.
- **No README §N refs in code.** Code comments must not point at README section numbers — the
  two artefacts evolve independently and the reference rots silently. References to other
  in-repo files by path are fine; section numbers are not.

## Git — always on

Commit subjects use a conventional-commit-ish prefix (`feat:`, `fix:`, `chore:`, `docs:`,
`refactor:`) and stay ≤ 70 chars; put any longer detail in the body. Never add
`Co-Authored-By` trailers.

## Linear lifecycle — always on

- An initiative is Ready only when all **six** fields are filled: Goal; Key results (3–5,
  each with baseline / target / window / source and a committed|aspirational tag); Affected
  repos; Appetite; Kill condition; Project type. Six fields, not four.
- Every cycle is **3 initiatives + 1 ops slot**. The ops slot is not a fourth initiative.
- **Done = KRs observed, not issues closed.** An initiative whose issues all closed but whose
  KRs didn't hold is Paused for a retrospective, not Done.
- On completion, after the gate: post a review-summary comment on the issue, then transition
  it to Done.
Read `rules/linear-workflow.md` for the full cycle / backlog / capture / issue-workflow rubric.
Read `rules/graphite-stack-review.md` for the runbook on handling reviewer comments across a Graphite-stacked PR series.

## Shaper pack — authoring and execution

Defer to the Shaper pack for initiative *authoring* and issue *execution*. The canonical
six-field shape definition and verification rubric live in its `shape:project` skill (with
`shape:idea` as the intake gate); the completion gate is owned by `exec:review` / `exec:finish`,
orchestrated end-to-end by `exec:pickup`; and the product and engineering principles live in
`PRODUCT_RULES.md` and `eng-principles-*.md`. Use `rules/linear-workflow.md` here for the
tracker mechanics — the cycle model, backlog, issue workflow, and Linear capture binding the
Shaper skills hand off to.
