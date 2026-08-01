from __future__ import annotations

from dataclasses import asdict

from .models import ConstitutionalState, ProjectionNode


class Engine:
    def create(
        self,
        *,
        intent: str,
        state: ConstitutionalState,
        root: ProjectionNode,
        governance: dict[str, object] | None = None,
    ) -> dict[str, object]:
        s = state.bounded()
        return {
            "runtimeProtocol": "AxiomUX-v1.0",
            "intentField": {"intent": intent},
            "governanceField": governance or {},
            "perceptionField": {"constitutionalState": asdict(s)},
            "interactionField": {
                "mutationAllowed": s.veracity < 0.98,
                "consentGateRequired": s.consensus >= 0.85,
            },
            "telemetryField": {},
            "rootProjection": root.to_dict(),
        }
