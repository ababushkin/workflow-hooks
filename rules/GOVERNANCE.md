# Workflow governance

## Code reviews

- Read `rules/code-review.md` for the mandatory code-review workflow when you've completed coding
- Read `rules/graphite-stack-review.md` for how to stack PRs and get them ready for human-review

## Comments

- Comments explain what the code is (invariants, constraints, workarounds) — not how it got that way.
- Never put in comments: ticket/issue IDs, task labels, commit SHAs, PR numbers, or fix history ("added for…", "fixes bug where…"). That belongs in commit messages, PRs, or design docs.
- When fixing an offending comment: strip the reference, keep any useful explanation, reword if needed, or delete if nothing remains.
- Leave alone: test sample-data IDs, schema placeholders, in-repo file paths.
- If a special case only makes sense with a multi-line explanation, delete the special case instead — the comment is a signal the design is wrong.
- Don't reference README section numbers in code comments — they rot. File paths are fine; section numbers are not.

## Git

Commit subjects use a conventional-commit-ish prefix (`feat:`, `fix:`, `chore:`, `docs:`,
`refactor:`) and stay ≤ 70 chars; put any longer detail in the body. Never add
`Co-Authored-By` trailers.

## Linear lifecycle

- Read `rules/linear-workflow.md` for how to use Linear for tracking and working with tasks/projects; per-repo team and ops-project live in `.linear_config` at the repo root
