#!/bin/bash

set -e

echo "================================================"
echo " Fixing Anchor Governance Runtime Reference"
echo "================================================"


FILE="aletheus/runtime/core.py"


cp "$FILE" "${FILE}.before_governance_reference_fix"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


old = "AnchorGovernanceAnalyzer(self)"

new = "AnchorGovernanceCouncil(self)"


if old in text:

    text = text.replace(
        old,
        new
    )

    print(
        "Replaced AnchorGovernanceAnalyzer with AnchorGovernanceCouncil"
    )

else:

    print(
        "No AnchorGovernanceAnalyzer runtime reference found"
    )


path.write_text(text)

PY


python3 -m compileall aletheus/runtime/core.py


echo "================================================"
echo " Governance Reference Repair Complete"
echo "================================================"

