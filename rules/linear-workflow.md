# Linear tracker binding

This file holds the two Linear-specific mechanics that the Shaper pack deliberately keeps out of itself to stay tracker-agnostic, and delegates here: the **cycle model** and the **capture recipe**. Shaper's `shape:project` skill points at this file (`skills/project/SKILL.md`: "Tracker capture and cycle model: owned by the Workflow pack when installed").

Everything about an initiative's *shape* — the six-field definition, the OKR form, the verification rubric, the size and lifecycle conventions, project naming — lives in `shape:project`, not here. Issue *execution* — pickup, breakdown, review, verify, finish — lives in `exec:pickup` and the skills it orchestrates. This file does not restate any of it.

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

The **backlog** is team issues with no project assigned, plus issues in the ops container project. Issues leave the backlog at cycle planning: assigned to an initiative project, pulled into the ops slot for the current cycle, or explicitly deferred. The backlog is not the idea bank — the idea bank holds unvalidated hypotheses (owned by `shape:idea`); the backlog holds concrete issues ready to work but not yet assigned.

### Cycle planning

On planning day:
1. Confirm 3 initiatives are in Ready state (six-field check passes for each — see `shape:project`).
2. Identify the ops slot: pull 2–5 issues from the team backlog (bugs, maintenance, one-offs) into the cycle as standalone issues.
3. For each initiative, confirm which issues in its backlog will be worked this cycle. Do not try to clear the entire initiative backlog in one cycle — prioritise by what moves a Key Result.
4. Assign all confirmed issues to the cycle.

### Cycle close

At cycle end, for each initiative:
- If all key results hold (or were definitively ruled out): mark initiative Done. Write one sentence in the Linear project description noting what was observed.
- If the work shipped but KRs didn't hold yet: note this; either carry the initiative into the next cycle (Active) or pause it for a retrospective.
- If the initiative is being killed: mark Cancelled with a one-sentence reason. This is a normal outcome, not a failure.

**Done = KRs observed, not issues closed.** An initiative whose issues all closed but whose KRs didn't hold is Paused for a retrospective, not Done.

---

## Capturing a shaped initiative in Linear

This is the tracker binding that `shape:project` calls as its final capture step.

**Precondition:** All six fields are complete and verified — `shape:project` enforces this before handing off. Do not call this procedure with partial fields.

### Steps

1. **Create the Linear project** via `mcp__claude_ai_Linear__save_project`:
   - `name`: the initiative goal name (a goal or problem name, not a repo name and not a solution name)
   - `description`: the full six-field block as confirmed by `shape:project`
   - `state`: `"planned"` (do not set to active until it enters a cycle)

2. **Create the seed issues** via `mcp__claude_ai_Linear__save_issue` for each issue identified during shaping:
   - Assign each to the project created in step 1
   - Leave cycle unset (cycle assignment happens at planning day)
   - Set status to `"Backlog"`

3. **Confirm** by reading back the project (`mcp__claude_ai_Linear__get_project`) and verifying the description persisted correctly.

### After capture

The project is in Draft or Planned state. It enters a cycle at planning day after the six-field check passes again at that time (context may have changed). Do not auto-assign to the current cycle on creation.
