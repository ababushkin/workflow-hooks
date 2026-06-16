# Delivery-issue adapter — on-pickup surfacing

The workflow-hooks pack is the tracker-binding adapter for delivery
plans authored under the agent-skills-shaper contract
(`docs/delivery-shape-contract.md` in that repo). The contract is
tool-agnostic by rule and names no tracker; the binding lives here.

This module discharges **one obligation** of that contract:

> `delegates_to` names the discipline that owns a node, but it **fires at
> issue-pickup (build time)**, not during plan emission. The adapter binding
> nodes to a concrete tracker must surface each node's `delegates_to` on the
> emitted artefact — explicit on-pickup instruction naming the delegate skill
> the picking-up agent must invoke before writing code. A `ktlo` node surfaces
> "no breakdown step" (roadmap A5 carve-out).
>
> — `docs/delivery-shape-contract.md` § *Delegation — timing & surfacing*

The consumer side is enforced by `rules/linear-workflow.md` § *On start*:
when an issue carries a delegate, the picking-up agent invokes that skill
**before writing code**.

## The seam

```
walk-delivery-plan <plan-dir> --json     (producer, agent-skills-shaper)
        │
        ▼
render-delivery-issues  --out <dir>      (adapter, this repo)
        │
        ▼
<dir>/D<n>-N<nn>-<slug>.md               one markdown body per issue
        │
        ▼
check-rendered-issues <dir>              fails loudly if a non-ktlo issue
                                         lacks the ▶ On pickup line
```

`render-delivery-issues` reads the JSON manifest the walk-script emits and
writes one markdown file per issue. It does not push to Linear directly: the
output is a renderable representation; a separate slice wires it to the
tracker API.

## On-pickup line templates

The renderer keys off the node `type` and the `delegates_to` string carried
by every node:

- **Non-ktlo nodes** — bare skill name + parenthetical purpose:
  ```
  > **▶ On pickup — before writing code:** invoke `<skill>` (<purpose>)
    to expand this node before building.
  ```
  e.g. `delegates_to: exec:breakdown (per-node task breakdown)`
  becomes ``invoke `exec:breakdown` (per-node task breakdown)…``.

- **`ktlo` nodes** — carve-out wording, no delegate to fire:
  ```
  > **▶ On pickup:** KTLO housekeeping — no task-breakdown step
    (ops slot carve-out; roadmap A5). Delegate: <delegates_to verbatim>.
  ```

A `delegates_to` value with no parenthetical (`<skill>` alone) drops the
parenthetical from the rendered line.

## The check

`check-rendered-issues <dir>` walks the rendered output and exits non-zero
when:

- A non-ktlo issue's body is missing the `▶ On pickup` marker (exit 2).
- An issue file's front-matter has no `type:` key (exit 2).
- The directory contains no rendered issue files (exit 64).

It is the adapter's stop-the-line gate: a hand-edit that strips the on-pickup
line from a non-ktlo issue will be caught before the issue is opened in the
tracker.

## End-to-end (worked example)

The shaper repo carries a worked-example delivery plan. Running the adapter
over it:

```bash
SHAPER=/path/to/agent-skills-shaper
$SHAPER/bin/walk-delivery-plan \
    $SHAPER/examples/delivery-plans/top-down-delivery-planning --json \
  > /tmp/manifest.json

bin/render-delivery-issues /tmp/manifest.json --out /tmp/rendered
bin/check-rendered-issues /tmp/rendered    # exits 0
```

Hand-breaking one non-ktlo issue (strip the `▶ On pickup` line) makes the
check exit 2 with the offending path listed on stderr.

## What this module does *not* do

- It does not author the plan. The shaper's `delivery-shape` skill emits the
  file-set.
- It does not enforce that `delegates_to` is present on every node — that is
  the walk-script's job (exit 2 if missing).
- It does not call the Linear API. That is a separate slice.
