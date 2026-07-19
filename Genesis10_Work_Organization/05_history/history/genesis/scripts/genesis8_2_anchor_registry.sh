#!/bin/bash

set -e

echo "=== Genesis 8.2 Anchor Registry ==="


cp aletheus/runtime/core.py \
aletheus/runtime/core.py.genesis8_2_backup



mkdir -p aletheus/runtime/anchors



cat > aletheus/runtime/anchors/registry.py <<'PY'
"""
Runtime Anchor Registry

Genesis 8.2

Owns lifecycle and discovery of runtime anchor circuits.
"""


class AnchorRegistry:


    def __init__(self, runtime):

        self.runtime = runtime
        self.anchors = {}



    def register(self, name, anchor):

        self.anchors[name] = anchor

        return anchor.status()



    def attach_all(self):

        results = {}

        for name, anchor in self.anchors.items():

            results[name] = anchor.attach()

        return results



    def get(self, name):

        return self.anchors.get(name)



    def list(self):

        return sorted(
            self.anchors.keys()
        )



    def status(self):

        return {

            "count":
                len(self.anchors),

            "anchors":
            {
                name:
                anchor.status()

                for name, anchor
                in self.anchors.items()
            },

            "healthy":
                all(
                    anchor.connected
                    for anchor
                    in self.anchors.values()
                )

        }
PY



python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/anchors/__init__.py"
)


text = path.read_text()


if "AnchorRegistry" not in text:

    text += """

from .registry import AnchorRegistry

"""


path.write_text(text)

PY




python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/core.py"
)


text = path.read_text()



# add import

if "AnchorRegistry" not in text:

    text=text.replace(

"""
from aletheus.runtime.anchors import (
    IntelligenceAnchorCircuit,
    MemoryAnchorCircuit,
    KnowledgeAnchorCircuit,
    ApplicationAnchorCircuit,
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
"""

)



old="""
self.anchor_circuits = [

    IntelligenceAnchorCircuit(self),
    MemoryAnchorCircuit(self),
    KnowledgeAnchorCircuit(self),
    ApplicationAnchorCircuit(self),

]


for anchor in self.anchor_circuits:

    anchor.attach()
"""

new="""

self.anchor_registry = AnchorRegistry(self)


self.anchor_registry.register(
    "intelligence",
    IntelligenceAnchorCircuit(self)
)

self.anchor_registry.register(
    "memory",
    MemoryAnchorCircuit(self)
)

self.anchor_registry.register(
    "knowledge",
    KnowledgeAnchorCircuit(self)
)

self.anchor_registry.register(
    "application",
    ApplicationAnchorCircuit(self)
)


self.anchor_registry.attach_all()

"""


text=text.replace(
old,
new
)



path.write_text(text)

PY





python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


print({

"anchors":
runtime_core.anchor_registry.status(),

"commands":
runtime_core.commands.count(),

"genesis":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY



echo "=== Genesis 8.2 Complete ==="

