"""
Anchor Evolution Execution Controller

Genesis 8.21

Executes governed runtime evolution.
"""

import time
import uuid


class AnchorEvolutionExecutionController:
    def __init__(self, negotiation, constitution, learning):

        self.negotiation = negotiation
        self.constitution = constitution
        self.learning = learning

        self.executions = []

    def execute(self, anchor, proposal):

        negotiation = self.negotiation.negotiate(anchor, proposal)

        selected = negotiation["selected"]

        governance = self.constitution.evaluate(anchor, selected)

        if not governance["approved"]:
            result = {"status": "blocked", "reason": "constitutional review failed"}

        else:
            result = {
                "status": "executed",
                "strategy": selected["option"]["strategy"]
                if isinstance(selected, dict) and "option" in selected
                else selected.get("strategy", "unknown"),
            }

        execution = {
            "execution_id": str(uuid.uuid4()),
            "anchor": anchor,
            "proposal": proposal,
            "result": result,
            "timestamp": time.time(),
        }

        self.executions.append(execution)

        self.learning.record(
            anchor,
            "evolution_execution",
            "success" if result["status"] == "executed" else "failure",
            result,
        )

        return execution

    def history(self):

        return self.executions

    def snapshot(self):

        return {"execution_count": len(self.executions)}
