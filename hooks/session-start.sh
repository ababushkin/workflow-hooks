#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOVERNANCE="$SCRIPT_DIR/../rules/GOVERNANCE.md"
RULES_DIR="$(cd "$SCRIPT_DIR/../rules" && pwd)"

python3 - "$GOVERNANCE" "$RULES_DIR" <<'EOF'
import json, sys, os
path, rules_dir = sys.argv[1], sys.argv[2]
try:
    with open(path) as f:
        content = f.read()
    content = content.replace('`rules/', f'`{rules_dir}/')
    context = ("IMPORTANT: the following workflow governance rules are always in "
               "effect this session.\n\n" + content)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
except Exception as e:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "workflow-hooks: rules/GOVERNANCE.md not found"}}))
EOF
