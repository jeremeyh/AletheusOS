from __future__ import annotations

from .models import CouncilMember
from .registry import CouncilRegistry


class CouncilEngineRegistry:
    GENESIS = "16.6"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = CouncilRegistry()
        self._bootstrapped = False

    def bootstrap_defaults(self):
        if self._bootstrapped:
            return self.statistics()

        defaults = [
            CouncilMember(
                member_id="council.aerie",
                name="AERIE™",
                role="Council Chairman",
                domain="coordination",
                authority="Council coordination, deliberation flow, and consensus orchestration.",
                metadata={
                    "type": "constitutional_intelligence",
                    "votes": True,
                    "chair": True,
                },
            ),
            CouncilMember(
                member_id="council.thorx",
                name="THORᵡ™",
                role="Constitutional Evaluation and Grading Engine",
                domain="evaluation",
                authority="Evaluation, grading, recommendation, enforcement, and Relix profile execution under Principle X.",
                metadata={
                    "type": "constitutional_intelligence",
                    "foundation_engine": "foundation.evaluation",
                    "principle": "Principle X",
                    "votes": True,
                },
            ),
            CouncilMember(
                member_id="council.sentinel",
                name="Sentinel™",
                role="Operational Integrity Engine",
                domain="operations",
                authority="Runtime health, operational stability, resilience, anomaly detection, and degradation evidence.",
                metadata={
                    "type": "constitutional_intelligence",
                    "votes": True,
                },
            ),
            CouncilMember(
                member_id="council.watch_tower",
                name="Watch Tower™",
                role="Architectural Integrity Engine",
                domain="architecture",
                authority="Architecture, dependency integrity, observability, system structure, and design-risk evidence.",
                metadata={
                    "type": "constitutional_intelligence",
                    "votes": True,
                },
            ),
            CouncilMember(
                member_id="council.atlas",
                name="Atlas™",
                role="Knowledge and Topology Engine",
                domain="knowledge",
                authority="Knowledge mapping, topology, system relationships, context, and semantic structure.",
                metadata={
                    "type": "constitutional_intelligence",
                    "votes": True,
                },
            ),
            CouncilMember(
                member_id="council.conclave",
                name="Conclave™",
                role="Constitutional Security Authority",
                domain="security",
                authority="Security posture, trust boundaries, containment, isolation, and constitutional security review.",
                metadata={
                    "type": "constitutional_authority",
                    "votes": False,
                    "consulted_by_council": True,
                },
            ),
        ]

        for member in defaults:
            self.registry.register(member)

        self._bootstrapped = True
        return self.statistics()

    def members(self):
        return self.registry.list()

    def health(self):
        return {
            "name": "Council Engine Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "bootstrapped": self._bootstrapped,
            "registry": self.registry.health(),
        }

    def statistics(self):
        return {
            "name": "Council Engine Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "members": self.registry.count(),
            "member_ids": self.registry.statistics()["member_ids"],
        }


council_engine_registry = CouncilEngineRegistry()
