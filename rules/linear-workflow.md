# Linear workflow — tracker mechanics

This document is the canonical model for how work is tracked in Linear when using the workflow-hooks pack. It applies to any repo in the workspace that loads this pack. It owns the **tracker mechanics** — cycle model, backlog, issue workflow, project conventions, and the Linear capture binding.

> **Cross-pack note:** Initiative *authoring* — the six-field shape definition and its verification rubric — is owned by the Shaper pack's `shape:project` skill (with `shape:idea` as the intake gate). This document does not restate the field definitions; refer to `shape:project` for what a valid field is. Use this document for the tracker mechanics either way.

---

## The initiative model

An **initiative** is a time-bounded, goal-oriented body of work with a stated success criterion and a bounded appetite. It is not a repo alias, not a backlog, and not a feature list.

An initiative is ready to enter a cycle when all **six** fields are filled and verified: Goal; Key results (3–5, each with baseline / target / window / source and a committed|aspirational tag); Affected repos; Appetite; Kill condition; Project type. The canonical definition of each field, the OKR shape, and the verification rubric live in Shaper's `shape:project` skill — author the initiative there. If any of the six fields can't be filled, the initiative is not ready: create it as a Draft in Linear but don't assign it to a cycle.

### Initiative size

| Size | Issue count | Notes |
|---|---|---|
| Too small | < 5 | Not an initiative — create a standalone issue or put it in the ops slot |
| Small | 5–8 | One cycle slot with room left for other initiatives |
| Medium | 9–12 | One full cycle slot |
| Large | 13–15 | Full cycle slot; very little room for anything else |
| Too large | > 15 | Split into two initiatives before committing |

### Initiative lifecycle

| State | Meaning |
|---|---|
| **Draft** | Idea exists; goal or criterion not yet written |
| **Ready** | All six fields confirmed — Goal + Key results (with sub-fields + tags) + Affected repos + Appetite + Kill condition + Project type; can enter a cycle |
| **Active** | Assigned to the current cycle; work in progress |
| **Done** | Success criterion observed (or definitively ruled out) — not just issues closed |
| **Paused** | Deprioritised mid-cycle; carries over with a note on why |
| **Canceled** | Kill condition triggered, or initiative definitively ruled out mid-cycle; one-sentence reason recorded |

**Done ≠ all issues closed.** An initiative closes when the key results are observed (or definitively ruled out) — not when its issue list reaches zero. An initiative that shipped everything but the KRs didn't hold is not Done; it is Paused for a retrospective.

### Creating an initiative

Use Shaper's `shape:project` skill — it enforces the six-field check (including the verification rubric gate) and hands the confirmed shape to the [Capturing a shaped initiative in Linear](#capturing-a-shaped-initiative-in-linear) procedure below.

Direct creation without filling all six fields is permitted only for: maintenance buckets, ops slots, and one-off standalone issue groupings.

---

## Cycle model

A cycle is 3–4 working days of focused work plus 1 planning day.

### Cycle composition

Every cycle has **exactly four slots**:

| Slot | Type | Goal/criterion required? |
|---|---|---|
| Initiative 1 | Goal-oriented | Yes |
| Initiative 2 | Goal-oriented | Yes |
| Initiative 3 | Goal-oriented | Yes |
| Ops slot | Maintenance | No |

The ops slot is not an initiative. It exists for: bug fixes, compliance items, emergent issues, one-offs, and KTLO work. Ops slot issues either have no project assigned, or live in the team's **ops container project** — a perpetual Backlog-state project named e.g. "Ops — bugs, maintenance, emergent" that holds ops work. The container project carries no Goal and no Key Results because it is not an initiative — it exists only because MCP tooling can't clear an issue's project assignment, so issues created via Claude Code need a non-initiative home.

**Do not add a 4th initiative.** The ops slot is not a buffer for overflow from the three initiative slots; it is a deliberate reservation for non-initiative work that would otherwise eat into initiative time unplanned. The ops container project is not an initiative either — it doesn't get a Goal, KRs, or appetite, and it never enters the Done state.

### Cycle planning

On planning day:
1. Confirm 3 initiatives are in Ready state (six-field check passes for each: Goal + Key results with sub-fields + Affected repos + Appetite + Kill condition + Project type).
2. Identify the ops slot: pull 2–5 issues from the team backlog (bugs, maintenance, one-offs) into the cycle as standalone issues.
3. For each initiative, confirm which issues in its backlog will be worked this cycle. Do not try to clear the entire initiative backlog in one cycle — prioritise by what moves a Key Result.
4. Assign all confirmed issues to the cycle.

### Cycle close

At cycle end, for each initiative:
- If all key results hold (or were definitively ruled out): mark initiative Done. Write one sentence in the Linear project description noting what was observed.
- If the work shipped but KRs didn't hold yet: note this; either carry the initiative into the next cycle (Active) or pause it for a retrospective.
- If the initiative is being killed: mark Cancelled with a one-sentence reason. This is a normal outcome, not a failure.

---

## Backlog

**Backlog = team issues with no project assigned, plus issues in the ops container project.**

Issues enter the backlog when:
- They don't belong to any current initiative
- They surface mid-flight as non-initiative work (bugs, one-offs)
- An initiative is killed and its remaining issues are descoped

Issues leave the backlog at cycle planning: either assigned to an initiative project, pulled into the ops slot for the current cycle, or explicitly deferred to a future cycle.

The backlog is not the idea bank. The idea bank holds unvalidated product hypotheses. The backlog holds concrete issues that are ready to be worked but not yet assigned.

---

## Issue workflow

Linear is authoritative for issue status. Local task lists are fine for within-session bookkeeping; they never replace updating the Linear issue itself.

### On start

- When picking up work, prefer issues already in the current cycle. If you start something not in the cycle, decide explicitly whether to pull it in or defer — don't silently expand cycle scope.
- Move to **In Progress** via `mcp__claude_ai_Linear__save_issue`.
- If the issue isn't yet in the current cycle and you intend to ship it this cycle, assign it to the current cycle.
- Every issue must be either (a) assigned to an initiative project, or (b) explicitly in the ops slot — meaning either no project assigned, or in the ops container project. An issue with neither an initiative nor an ops home is untracked — don't let this happen.
- If the issue names a delegate (a `Delegates to` / `▶ On pickup` line), invoke that skill **before writing code** to expand the node into its build tasks — `exec:breakdown` for build stories, the named skill otherwise. Issues with no delegate, and `ktlo` issues, carry no breakdown step.

Shaper's `exec:pickup` skill owns this whole path end-to-end — pickup, breakdown, build, review, verify, finish. Invoke it to drain an issue; the rules here are the tracker-side invariants it satisfies.

### On completion

Before an issue moves to **Done**, the completion gate runs (Review → Fix → Commit + push; see `rules/code-review.md`). When Shaper is installed, `exec:finish` performs the gate's tracker steps: it posts the review-summary comment via `mcp__claude_ai_Linear__save_comment` (count of findings by severity, fixed vs deferred) and transitions the issue to Done via `mcp__claude_ai_Linear__save_issue`.

Status updates happen at the moment of state change — not batched at the end of a session.

### Blocked

Leave In Progress. Add a blocker comment naming the blocker explicitly. Don't silently park work.

### New work surfaced mid-flight

Two cases:

- **Initiative-shaped** (5+ issues, clear goal): create a new Linear project with Shaper's `shape:project`. Slot it into the next cycle explicitly — don't silently expand the current cycle's scope.
- **Bug or one-off** (< 5 issues, no sustained goal): create the issue on the team backlog. If it's urgent, pull it into the current cycle's ops slot.

---

## Linear project conventions

- **Project name**: goal or problem name, not a solution name and not a repo name.
  - Good: "Equity analysis report — usability for non-analysts"
  - Bad: "stock-review", "stock-explain feature", "agent-skills-workflow v2"
- **Project description**: always uses the six-field initiative format (goal / key results with sub-fields / affected repos / appetite / kill condition / project type).
- **Project state**: Planned until it enters a cycle; In Progress when active; Completed or Cancelled on close.

---

## Capturing a shaped initiative in Linear

This procedure records a fully shaped initiative in Linear. It is the tracker binding that Shaper's `shape:project` skill calls as its final capture step.

**Precondition:** All six fields are complete and verified (Goal, Key results with sub-fields, Affected repos, Appetite, Kill condition, Project type) — `shape:project` enforces this before handing off. Do not call this procedure with partial fields.

### Steps

1. **Create the Linear project** via `mcp__claude_ai_Linear__save_project`:
   - `name`: the initiative goal name (not a repo name, not a solution name)
   - `description`: the full six-field block as confirmed by `shape:project`
   - `state`: `"planned"` (do not set to active until it enters a cycle)

2. **Create the seed issues** via `mcp__claude_ai_Linear__save_issue` for each issue identified during shaping:
   - Assign each to the project created in step 1
   - Leave cycle unset (cycle assignment happens at planning day)
   - Set status to `"Backlog"`

3. **Confirm** by reading back the project (`mcp__claude_ai_Linear__get_project`) and verifying the description persisted correctly.

### After capture

The project is in Draft or Planned state. It enters a cycle at planning day after the six-field check passes again at that time (context may have changed). Do not auto-assign to the current cycle on creation.
