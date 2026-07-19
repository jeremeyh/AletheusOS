#!/bin/bash

set -e

echo "================================================"
echo " Fix IntelligenceAnchorCircuit Base Contract"
echo "================================================"

FILE="aletheus/runtime/anchors/intelligence.py"

cp "$FILE" "${FILE}.before_contract_cleanup"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/anchors/intelligence.py")

text = path.read_text()


text = text.replace(
'''
        self.runtime = runtime
        self.name = "intelligence"
        self.scorer = None
''',
'''
        super().__init__()

        self.runtime = runtime
        self.scorer = None
'''
)


text = text.replace(
'''
        self.runtime = runtime
        self.name = "intelligence"
''',
'''
        super().__init__()

        self.runtime = runtime
'''
)


path.write_text(text)

print("Updated IntelligenceAnchorCircuit initialization")

PY


python3 -m compileall "$FILE"


echo "================================================"
echo " Intelligence Anchor Contract Fixed"
echo "================================================"

