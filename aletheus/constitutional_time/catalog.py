"""Canonical TIME™ mission phase graphs."""

from __future__ import annotations

from .graph import MissionPhaseGraph
from .models import MissionPhaseContract


def security_containment_phase_graph(
) -> MissionPhaseGraph:
    graph = MissionPhaseGraph()

    graph.add(
        MissionPhaseContract(
            phase_id="detect",
            canonical_name="Detect",
            purpose=(
                "Establish the initial constitutional integrity finding."
            ),
            participating_institutions=(
                "aletheus.watch_tower",
            ),
            required_evidence_types=(
                "integrity_finding",
            ),
            produces=(
                "integrity_finding",
            ),
            completion_criteria=(
                "A governed integrity finding exists.",
            ),
            failure_criteria=(
                "No valid integrity finding was produced.",
            ),
        )
    )

    graph.add(
        MissionPhaseContract(
            phase_id="classify",
            canonical_name="Classify",
            purpose=(
                "Classify the defensive significance of the finding."
            ),
            dependencies=("detect",),
            participating_institutions=(
                "aletheus.guardian",
            ),
            required_evidence_types=(
                "threat_classification",
            ),
            produces=(
                "threat_classification",
            ),
            completion_criteria=(
                "Guardian produced a threat classification.",
            ),
            failure_criteria=(
                "The finding could not be classified.",
            ),
        )
    )

    graph.add(
        MissionPhaseContract(
            phase_id="contain",
            canonical_name="Contain",
            purpose=(
                "Establish a governed isolation boundary."
            ),
            dependencies=("classify",),
            participating_institutions=(
                "aletheus.conclave",
            ),
            required_evidence_types=(
                "containment_result",
            ),
            produces=(
                "containment_result",
            ),
            completion_criteria=(
                "The affected entity is quarantined.",
            ),
            failure_criteria=(
                "Containment could not be established.",
            ),
        )
    )

    graph.add(
        MissionPhaseContract(
            phase_id="preserve",
            canonical_name="Preserve Evidence",
            purpose=(
                "Preserve forensic evidence and chain of custody."
            ),
            dependencies=("contain",),
            participating_institutions=(
                "aletheus.containment_vault",
            ),
            required_evidence_types=(
                "forensic_preservation",
            ),
            produces=(
                "forensic_preservation",
            ),
            completion_criteria=(
                "Evidence was durably preserved.",
            ),
            failure_criteria=(
                "Forensic evidence preservation failed.",
            ),
        )
    )

    graph.add(
        MissionPhaseContract(
            phase_id="stabilize",
            canonical_name="Stabilize",
            purpose=(
                "Confirm that the active runtime incident is stable."
            ),
            dependencies=("preserve",),
            participating_institutions=(
                "aletheus.sentinel",
            ),
            required_evidence_types=(
                "stabilization_result",
            ),
            produces=(
                "stabilization_result",
            ),
            completion_criteria=(
                "Sentinel confirmed operational stabilization.",
            ),
            failure_criteria=(
                "Runtime stability could not be confirmed.",
            ),
        )
    )

    graph.validate()
    return graph
