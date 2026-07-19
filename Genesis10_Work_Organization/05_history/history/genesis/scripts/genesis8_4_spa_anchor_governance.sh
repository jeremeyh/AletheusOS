#!/bin/bash

set -e

echo "=== Genesis 8.4 SPA Anchor Governance ==="


cp aletheus/runtime/spa.py \
aletheus/runtime/spa.py.genesis8_4_backup 2>/dev/null || true



mkdir -p aletheus/runtime/spa



cat > aletheus/runtime/spa/anchor_analysis.py <<'PY'
"""
SPA Anchor Governance Analyzer

Genesis 8.4

Analyzes Runtime Anchor Circuit health,
contracts, and expansion risk.
"""


class AnchorGovernanceAnalyzer:


    def __init__(self, runtime):

        self.runtime = runtime



    def analyze(self):

        registry = getattr(
            self.runtime,
            "anchor_registry",
            None
        )


        if registry is None:

            return {

                "status": "unavailable",
                "risk_count": 1,
                "risks": [
                    "Anchor registry missing"
                ]

            }



        contracts = (
            registry.validate_contracts()
        )


        violations = [

            name

            for name, result
            in contracts.items()

            if not result.get(
                "valid",
                False
            )

        ]


        return {

            "status":
                "healthy"
                if not violations
                else "warning",

            "anchor_count":
                len(registry.list()),

            "contract_violations":
                len(violations),

            "risks":
                violations,

            "drift_detected":
                len(violations) > 0

        }
PY




python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/spa/__init__.py"
)


if not path.exists():

    path.write_text("")


text = path.read_text()


if "AnchorGovernanceAnalyzer" not in text:

    text += """

from .anchor_analysis import AnchorGovernanceAnalyzer

"""


path.write_text(text)

PY





python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/core.py"
)


text = path.read_text()



# import

if "AnchorGovernanceAnalyzer" not in text:

    text=text.replace(

"""
from aletheus.runtime.anchors import (
    IntelligenceAnchorCircuit,
    MemoryAnchorCircuit,
    KnowledgeAnchorCircuit,
    ApplicationAnchorCircuit,
    AnchorRegistry,
)
""",

"""
from aletheus.runtime.anchors import (
    IntelligenceAnchorCircuit,
    MemoryAnchorCircuit,
    KnowledgeAnchorCircuit,
    ApplicationAnchorCircuit,
    AnchorRegistry,
)

from aletheus.runtime.spa.anchor_analysis import (
    AnchorGovernanceAnalyzer
)

"""

)



# initialize

needle="""
self.anchor_registry = AnchorRegistry(self)
"""


replacement="""
self.anchor_registry = AnchorRegistry(self)

self.anchor_governance_analyzer = (
    AnchorGovernanceAnalyzer(self)
)

"""


text=text.replace(
needle,
replacement
)



# add runtime method

if "anchor_governance_status" not in text:

    insert="""

    def anchor_governance_status(self):

        return (
            self.anchor_governance_analyzer
            .analyze()
        )

"""

    text += insert



path.write_text(text)

PY





python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


print({

"anchors":
runtime_core.anchor_registry.status(),

"anchor_governance":
runtime_core.anchor_governance_status(),

"commands":
runtime_core.commands.count(),

"genesis":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY



echo "=== Genesis 8.4 Complete ==="

