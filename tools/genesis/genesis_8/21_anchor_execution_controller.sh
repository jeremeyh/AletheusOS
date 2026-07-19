#!/bin/bash

set -e

echo "=== Genesis 8.21 Anchor Evolution Execution Controller ==="


mkdir -p aletheus/runtime/anchors


cat > aletheus/runtime/anchors/execution.py <<'PY'
"""
Anchor Evolution Execution Controller

Genesis 8.21

Executes governed runtime evolution.
"""


import time
import uuid



class AnchorEvolutionExecutionController:


    def __init__(
        self,
        negotiation,
        constitution,
        learning
    ):

        self.negotiation = negotiation
        self.constitution = constitution
        self.learning = learning

        self.executions = []



    def execute(
        self,
        anchor,
        proposal
    ):

        negotiation = (
            self.negotiation
            .negotiate(
                anchor,
                proposal
            )
        )


        selected = (
            negotiation["selected"]
        )


        governance = (
            self.constitution
            .evaluate(
                anchor,
                selected
            )
        )


        if not governance["approved"]:

            result = {

                "status":
                    "blocked",

                "reason":
                    "constitutional review failed"

            }

        else:

            result = {

                "status":
                    "executed",

                "strategy":
                    selected["option"]["strategy"]
                    if isinstance(
                        selected,
                        dict
                    )
                    and "option" in selected
                    else selected.get(
                        "strategy",
                        "unknown"
                    )

            }


        execution = {

            "execution_id":
                str(uuid.uuid4()),

            "anchor":
                anchor,

            "proposal":
                proposal,

            "result":
                result,

            "timestamp":
                time.time()

        }


        self.executions.append(
            execution
        )


        self.learning.record(

            anchor,

            "evolution_execution",

            "success"
            if result["status"] == "executed"
            else "failure",

            result

        )


        return execution



    def history(self):

        return self.executions



    def snapshot(self):

        return {

            "execution_count":
                len(self.executions)

        }
PY



python - <<'PY'

from pathlib import Path

path = Path(
"aletheus/runtime/anchors/__init__.py"
)

text = path.read_text()

if "AnchorEvolutionExecutionController" not in text:

    text += """

from .execution import AnchorEvolutionExecutionController

"""

path.write_text(text)

PY



python - <<'PY'

from pathlib import Path

path = Path(
"aletheus/runtime/core.py"
)

text = path.read_text()


text=text.replace(

"""
    AnchorEvolutionNegotiationEngine,
)
""",

"""
    AnchorEvolutionNegotiationEngine,
    AnchorEvolutionExecutionController,
)
"""
)


needle="""
self.anchor_negotiation = (
    AnchorEvolutionNegotiationEngine(
        self.anchor_simulation,
        self.anchor_intelligence,
        self.anchor_governance
    )
)
"""


replacement="""

self.anchor_negotiation = (
    AnchorEvolutionNegotiationEngine(
        self.anchor_simulation,
        self.anchor_intelligence,
        self.anchor_governance
    )
)


self.anchor_execution = (
    AnchorEvolutionExecutionController(
        self.anchor_negotiation,
        self.anchor_constitution,
        self.anchor_learning
    )
)

"""


text=text.replace(
needle,
replacement
)



if "anchor_execution_status" not in text:

    text += """

    def anchor_execution_status(self):

        return (
            self.anchor_execution
            .snapshot()
        )

"""


path.write_text(text)

PY



python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


execution = (
    runtime_core.anchor_execution
    .execute(
        "memory",
        {
            "action":
                "upgrade"
        }
    )
)


print({

"execution":
execution,

"status":
runtime_core.anchor_execution_status(),

"learning":
runtime_core.anchor_learning_status(),

"commands":
runtime_core.commands.count(),

"genesis":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY


echo "=== Genesis 8.21 Complete ==="

