#!/usr/bin/env python3
"""PreToolUse gate on ExitPlanMode.

Reads the hook payload on stdin, scans the session transcript for a
writing-refinement pass, and denies the call when none is found. Fails open on
any missing input, unreadable transcript, or parse error.
"""
import json, re, sys


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return  # fail open on unparseable payload

    transcript = payload.get("transcript_path")
    if not transcript:
        return

    # A refinement pass shows up as a sub-agent dispatch (Agent/Task) or a Skill
    # call whose input mentions writing-refinement. Matching the serialized input
    # catches every dispatch shape: subagent_type, prompt text, or skill name.
    pattern = re.compile(r"writing[-_ ]?refinement", re.I)
    tool_names = {"Agent", "Task", "Skill"}

    found = False
    try:
        with open(transcript) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                message = obj.get("message")
                content = message.get("content") if isinstance(message, dict) else None
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    if block.get("name") not in tool_names:
                        continue
                    if pattern.search(json.dumps(block.get("input", {}))):
                        found = True
                        break
                if found:
                    break
    except Exception:
        return  # fail open if the transcript can't be read

    if found:
        return

    reason = (
        "Writing-review gate: finalize a plan only after a writing-refinement pass. "
        "This session records no writing-refinement run. Launch the writing-refinement "
        "skill as a sub-agent over the plan (dispatch an Agent whose prompt invokes "
        "/writing-refinement, or call the writing-refinement Skill), apply its findings to "
        "the plan file, then call ExitPlanMode again. To bypass — for example when using an "
        "alternative refiner — set WORKFLOW_HOOKS_WRITING_GATE=off."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


if __name__ == "__main__":
    main()
