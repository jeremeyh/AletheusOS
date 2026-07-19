#!/bin/bash

set -e

echo "================================================"
echo " AletheusOS Runtime Anchor Import Restoration"
echo " Canonical Genesis 8 Anchor Surface"
echo "================================================"

FILE="aletheus/runtime/core.py"

cp "$FILE" "${FILE}.before_anchor_import_final"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


anchor_import = """
from aletheus.runtime.anchors import (
    AnchorRegistry,
    AnchorLifecycleController,
    AnchorDependencyGraph,
    AnchorGovernanceCouncil,
    IntelligenceAnchorCircuit,
    MemoryAnchorCircuit,
    KnowledgeAnchorCircuit,
    ApplicationAnchorCircuit,
)
"""


# Remove any previous bad injected block
start = text.find("from aletheus.runtime.anchors import (")

if start != -1:

    end = text.find(")\n", start)

    if end != -1:
        text = (
            text[:start]
            +
            anchor_import
            +
            text[end+2:]
        )

        print("Replaced existing anchor import block")

else:

    marker = "class AletheusRuntime:"

    text = text.replace(
        marker,
        anchor_import + "\n\n" + marker
    )

    print("Inserted canonical anchor imports")


path.write_text(text)

PY


python3 -m compileall aletheus/runtime/core.py


python3 - <<'PY'

import aletheus.runtime.core as core

print("AnchorRegistry:", core.AnchorRegistry)
print("AnchorLifecycleController:", core.AnchorLifecycleController)
print("AnchorDependencyGraph:", core.AnchorDependencyGraph)
print("AnchorGovernanceCouncil:", core.AnchorGovernanceCouncil)

print("Runtime core module loaded")

PY


echo "================================================"
echo " Anchor Import Restoration Complete"
echo "================================================"

