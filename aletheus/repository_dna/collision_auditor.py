from __future__ import annotations

from collections.abc import Iterable

from .audit_models import CollisionCandidate, SubsystemRecord


class RepositoryDNACollisionAuditor:
    """Detects likely concept overlap clusters from subsystem names."""

    KNOWN_CLUSTERS = {
        "kernel": [
            "kernel",
            "kernel_v2",
            "platform_kernel",
            "executive_kernel",
            "cognitive_kernel",
        ],
        "runtime": [
            "runtime",
            "application_runtime",
            "intent_runtime",
            "cognitive_runtime",
            "constitutional_runtime",
            "runtime_registry_v2",
        ],
        "memory": ["memory", "working_memory", "memory_mesh", "constitutional_memory"],
        "mesh": ["mesh", "cognitive_mesh", "memory_mesh"],
        "registry": [
            "platform_registry",
            "runtime_registry_v2",
            "engine_registry",
            "council_registry",
            "boot_registry",
        ],
        "planning": ["planning", "planning_v2"],
        "agents": ["agents", "agents_v2"],
    }

    def audit(self, records: Iterable[SubsystemRecord]) -> list[CollisionCandidate]:
        names = {r.name for r in records}
        findings: list[CollisionCandidate] = []

        for cluster, expected in self.KNOWN_CLUSTERS.items():
            members = [n for n in expected if n in names]
            if len(members) > 1:
                findings.append(
                    CollisionCandidate(
                        cluster=cluster,
                        members=members,
                        reason="Multiple related subsystem names exist; classify as canonical, transitional, or archived.",
                        severity="needs_adr",
                    )
                )

        return findings
