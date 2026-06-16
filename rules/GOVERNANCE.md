# Workflow governance

## Code reviews

- Read `rules/code-review.md` for the mandatory code-review workflow when you've completed coding
- Read `rules/graphite-stack-review.md` for how to stack PRs and get them ready for human-review

## Writing

Apply these prose rules to everything you write - chat replies, commit messages, docs, tickets. They override default phrasing habits. The goal is to write using plain English, with simple words and maximum clarity.

### Writing review gate — for persisted artifacts

Before you finalize any writing of substance, run a writing-refinement pass as a sub-agent and apply its findings. "Of substance" means a persisted artifact: a design doc, RFC, plan, PR/MR description, ticket or issue, README, or a commit message body, any artefact that you've written in planning mode or anything written to a file or an external system.

- Use writing-refinement via agent-skills-shaper (the `writing-refinement` skill, i.e. `/writing-refinement`), or a preferred alternative if you have one installed. Launch it as a sub-agent.
- The gate does not apply to ordinary chat replies or code comments — hold those to the prose rules below directly, without a sub-agent.
- Apply the refinement's changes before posting or committing the artifact. If you reject a suggestion, note why in your summary.

### Prose rules

- **Voice.** Write like a professional talking to a colleague. No AI filler ("It's worth noting that…", "In today's fast-paced world…", "I hope this helps!"). No throat-clearing ("It should be noted that…", "It is important to…") — start with the point.

- **Name the actor, use a verb.** Make the doer (the system, the user, you) the grammatical subject and its action a specific verb. Prefer active voice.
  Bad: "Request dropping occurs at high utilization." Good: "The load balancer drops requests above 1k RPS."

- **Reverse nominalizations.** utilization→use, implementation→implement, optimization→optimize, investigation→investigate, facilitation→help/enable, determination→decide, reduction→cut.

- **Old before new.** Start a sentence with what the reader already knows; put the newest or most important term last, where it lands hardest.
  Bad: "Edge Workers, which intercept requests at the CDN layer, will cut load time."
  Good: "To cut load time, we'll intercept requests at the CDN layer with Edge Workers."

- **Cut clutter.** Delete little qualifiers (basically, actually, quite, virtually, a bit) and redundant pairs (full and complete, each and every). "in order to"→"to", "at this point in time"→"now".

- **Vocabulary watchlist.** leverage(v)→use, impact(v)→affect, interface with→talk to, bottleneck→the specific shortage/delay, blueprint→plan/spec, target→goal, load-bearing→essential. Decorative jargon → the literal mechanism: bet→approach/the assumption being tested, gate→check/the required condition, brake→limit/what stops it, blast radius→the modules a change touches, north-star→goal/target metric, keystone→the part the rest depends on, spine→the structure, seam→the boundary/integration point, shepherd(v)→guide/route, lever→the control/input, surface(v)→show/expose/report, cap/drift(figurative)→limit / it grew.

- **Plain English, no metaphors.** This is technical writing, not a story — no metaphor, analogy, or figurative jargon unless the user asked for one. Write the literal mechanism. Tell two look-alikes apart: a *conventional technical term* is the field's only ordinary name for the thing — keep `mutex`, `queue`, `thread`, `stream`, `cache`, `branch`, `handshake`. A *live decorative metaphor* is a sport/war/building/finance/nature word standing in for an idea you could name directly — replace it. Test: would a new engineer search the codebase for the word? They'd search `mutex`, not `north-star` or `blast radius`.

- **Say it once.** State each fact, number, or decision in one place. Repetition is not emphasis; a point already made, restated, is clutter — replace the second mention with a back-reference.

- **No jargon-as-rigor.** Reject formal phrasing that obscures a simple idea: "operationalise"→do, "structured placement act"→putting it on the list. If a plainer phrasing exists, use it.

- **Headings are achievements, not labels.** A heading carries a verb or a result ("Cut checkout latency to under 1.5s"), not a category ("Phase 2", "Data").

- **Never invent numbers.** If a figure is needed but unknown, use a bracketed placeholder or ask. Don't fabricate the number that makes a claim look good.

- **Prune without amputating.** Concision serves clarity, never the reverse. Compress a wordy sentence that carries a risk, dependency, assumption, or constraint — never delete it.

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
