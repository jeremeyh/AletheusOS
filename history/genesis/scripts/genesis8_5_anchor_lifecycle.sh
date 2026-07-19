#!/bin/bash

set -e

echo "=== Genesis 8.5 Anchor Lifecycle Management ==="


cp aletheus/runtime/anchors/registry.py \
aletheus/runtime/anchors/registry.py.genesis8_5_backup


cat > aletheus/runtime/anchors/lifecycle.py <<'PY'
"""
Anchor Lifecycle Controller

Genesis 8.5

Controls bounded capability lifecycle.
"""


import time



class AnchorLifecycleController:


    def __init__(self, registry):

        self.registry = registry
        self.history = []



    def attach(self, name):

        anchor = self.registry.get(name)

        if not anchor:

            return {
                "success": False,
                "error": "Anchor not found"
            }


        result = anchor.attach()

        self.record(
            "attach",
            name
        )

        return result



    def detach(self, name):

        anchor = self.registry.get(name)

        if not anchor:

            return {
                "success": False,
                "error": "Anchor not found"
            }


        result = anchor.detach()

        self.record(
            "detach",
            name
        )

        return result



    def restart(self, name):

        self.detach(name)

        time.sleep(0.01)

        return self.attach(name)



    def health(self, name=None):

        if name:

            anchor = self.registry.get(name)

            return (
                anchor.health()
                if anchor
                else None
            )


        return {

            key:
                anchor.health()

            for key, anchor
            in self.registry.anchors.items()

        }



    def record(self, action, anchor):

        self.history.append({

            "action":
                action,

            "anchor":
                anchor,

            "timestamp":
                time.time()

        })



    def history_snapshot(self):

        return self.history
PY




python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/anchors/__init__.py"
)


text = path.read_text()


if "AnchorLifecycleController" not in text:

    text += """

from .lifecycle import AnchorLifecycleController

"""


path.write_text(text)

PY





python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/core.py"
)


text = path.read_text()



if "AnchorLifecycleController" not in text:

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
    AnchorLifecycleController,
)
"""

)



needle="""
self.anchor_registry = AnchorRegistry(self)

self.anchor_governance_analyzer = (
    AnchorGovernanceAnalyzer(self)
)
"""


replacement="""

self.anchor_registry = AnchorRegistry(self)


self.anchor_lifecycle = (
    AnchorLifecycleController(
        self.anchor_registry
    )
)


self.anchor_governance_analyzer = (
    AnchorGovernanceAnalyzer(self)
)

"""


text=text.replace(
needle,
replacement
)



if "anchor_lifecycle_status" not in text:

    text += """

    def anchor_lifecycle_status(self):

        return {

            "anchors":
                self.anchor_registry.list(),

            "health":
                self.anchor_lifecycle.health(),

            "history":
                self.anchor_lifecycle.history_snapshot()

        }

"""



path.write_text(text)

PY





python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


print({

"anchors":
runtime_core.anchor_registry.list(),

"lifecycle":
runtime_core.anchor_lifecycle_status(),

"governance":
runtime_core.anchor_governance_status(),

"commands":
runtime_core.commands.count(),

"genesis":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY



echo "=== Genesis 8.5 Complete ==="

