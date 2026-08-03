from __future__ import annotations

from .equations import (
    consensus_pressure,
    contradiction_shear,
    informational_mass,
)
from .models import EvidenceNode, RuntimeHealth, RuntimeProfile, TelemetryFrame


class RuntimeRealizationEngine:
    """Control-plane synthesis for the Genesis 37 high-performance runtimes."""

    def score_nodes(self, nodes: list[EvidenceNode]) -> list[dict[str, float | str]]:
        pressure = consensus_pressure(nodes)
        scored = [
            {
                "node_id": node.node_id,
                "mass": informational_mass(node),
                "shear": contradiction_shear(node),
                "consensus_pressure": pressure,
                "veracity": max(0.0, min(1.0, node.veracity)),
            }
            for node in nodes
        ]
        return sorted(
            scored, key=lambda item: (-float(item["mass"]), str(item["node_id"]))
        )

    def runtime_health(
        self,
        frame: TelemetryFrame,
        profile: RuntimeProfile,
    ) -> RuntimeHealth:
        bottlenecks: list[str] = []
        recommendations: list[str] = []

        target_frame_ms = 1000.0 / max(1, profile.target_fps)
        frame_score = min(
            1.0, target_frame_ms / max(target_frame_ms, frame.frame_time_ms)
        )
        queue_score = 1.0 / (1.0 + max(0, frame.gpu_queue_depth) / 8.0)
        wasm_score = 1.0 / (1.0 + max(0.0, frame.wasm_step_ms) / 4.0)

        if frame.frame_time_ms > target_frame_ms * 1.25:
            bottlenecks.append("frame-time")
            recommendations.append("reduce visible-node budget or shader complexity")
        if frame.gpu_queue_depth > 8:
            bottlenecks.append("gpu-queue")
            recommendations.append("coalesce GPU submissions and use compute batching")
        if frame.wasm_step_ms > 4.0:
            bottlenecks.append("wasm-step")
            recommendations.append(
                "increase structure-of-arrays batching or lower physics Hz"
            )

        governance_score = (
            max(0.0, min(1.0, frame.mission_health))
            + max(0.0, min(1.0, frame.constitutional_compliance))
            + max(0.0, min(1.0, frame.security_posture))
        ) / 3.0
        score = (
            0.30 * frame_score
            + 0.20 * queue_score
            + 0.20 * wasm_score
            + 0.30 * governance_score
        )
        status = (
            "healthy" if score >= 0.85 else "degraded" if score >= 0.65 else "critical"
        )
        return RuntimeHealth(
            status=status,
            score=round(score, 4),
            bottlenecks=tuple(bottlenecks),
            recommendations=tuple(recommendations),
        )
