#!/bin/bash

set -e

FILE="aletheus/runtime/core.py"

echo "================================================"
echo " Fixing Anchor Governance Initialization Order"
echo "================================================"

cp "$FILE" "${FILE}.before_governance_order_fix"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


block = """self.anchor_governance_analyzer = (
    AnchorGovernanceCouncil(
        self.prediction,
        self.intelligence
    )
)"""


if block in text:

    text = text.replace(
        block,
        "# Anchor governance deferred until intelligence services initialize\n"
    )

    marker = "self.intelligence = intelligence_core"

    replacement = marker + """



        self.anchor_governance_analyzer = (
            AnchorGovernanceCouncil(
                self.prediction,
                self.intelligence
            )
        )
"""


    text = text.replace(
        marker,
        replacement
    )

    print("Moved governance initialization after intelligence setup")

else:

    print("Governance block not found")


path.write_text(text)

PY


python3 -m compileall aletheus/runtime/core.py

python3 - <<'PY'
from aletheus.runtime.core import runtime_core

print("SUCCESS")
print(runtime_core)

PY


echo "================================================"
echo " Governance Order Repair Complete"
echo "================================================"

