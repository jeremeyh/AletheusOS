from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import EvidenceNode, MarketObservation


class Engine:
    def build(
        self,
        observations: tuple[MarketObservation, ...],
    ) -> dict[str, Any]:
        nodes: list[EvidenceNode] = []
        groups: dict[str, list[str]] = defaultdict(list)

        for index, observation in enumerate(observations):
            topology = (
                "CRYSTALLINE_SOLID"
                if observation.verified and observation.reliability >= 0.98
                else (
                    "QUASI_CRYSTALLINE"
                    if observation.reliability >= 0.85
                    else (
                        "FLUID_REACTIVE"
                        if observation.reliability >= 0.60
                        else "NEBULAR_PROBABILITY"
                    )
                )
            )
            node = EvidenceNode(
                node_id=f"market:{index}:{observation.source_id}",
                category=observation.observation_type,
                value=observation.amount,
                confidence=min(1.0, max(0.0, observation.reliability)),
                provenance=(observation.source_id,),
                temporal_class="PRESENT" if observation.verified else "OBSERVED",
                topology=topology,
            )
            nodes.append(node)
            groups[node.category].append(node.node_id)

        return {
            "nodes": [node.__dict__ for node in nodes],
            "groups": dict(groups),
            "provenancePreserved": True,
            "claimLevelTopology": True,
        }
