#!/bin/bash

set -e

FILE="aletheus/runtime/core.py"

echo "================================================"
echo " Fix Prediction/Governance Initialization Order"
echo "================================================"

cp "$FILE" "${FILE}.before_prediction_governance_fix"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


old = """        self.anchor_governance_analyzer = (
            AnchorGovernanceCouncil(
                self.prediction,
                self.intelligence
            )
        )

        self.prediction = prediction_core
"""


new = """        self.prediction = prediction_core

        self.anchor_governance_analyzer = (
            AnchorGovernanceCouncil(
                self.prediction,
                self.intelligence
            )
        )
"""


if old not in text:
    raise Exception(
        "Expected governance/prediction block not found"
    )


text = text.replace(old, new)

path.write_text(text)

print("Prediction moved before governance initialization")

PY


python3 -m compileall "$FILE"

echo "================================================"
echo " Complete"
echo "================================================"

