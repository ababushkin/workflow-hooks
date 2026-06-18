#!/bin/bash
# PreToolUse gate on ExitPlanMode. Blocks plan finalization until a
# writing-refinement pass has run in this session. Set
# WORKFLOW_HOOKS_WRITING_GATE=off to disable. The Python sibling reads the hook
# payload from stdin and fails open on any error.

if [ "${WORKFLOW_HOOKS_WRITING_GATE:-}" = "off" ]; then
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/exit-plan-writing-gate.py"
