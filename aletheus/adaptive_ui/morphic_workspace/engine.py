from dataclasses import replace

from .models import *


class Engine:
    def mutate(self, node, state):
        if state == CognitiveState.OVERLOADED:
            return replace(
                node,
                opacity=min(node.opacity, 0.75),
                metadata={**node.metadata, "morphology": "SUMMARY"},
            )
        if state == CognitiveState.CRITICAL:
            return replace(
                node,
                topological_state=TopologicalState.CRYSTALLINE_SOLID,
                metadata={**node.metadata, "morphology": "FOCUS_LOCK"},
            )
        if state == CognitiveState.EXPLORING:
            return replace(
                node, metadata={**node.metadata, "morphology": "FLUID_EXPLORATION"}
            )
        return node
