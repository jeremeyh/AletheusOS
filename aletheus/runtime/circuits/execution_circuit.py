from __future__ import annotations

from typing import Any, Dict

from aletheus.ctf.engine import CognitiveTransitFabric
from aletheus.runtime.circuits.anchor_circuit import (
    CircuitHealth,
    CircuitManifest,
    CircuitStatus,
    RuntimeAnchorCircuit,
)


class ExecutionCircuit(RuntimeAnchorCircuit):
    """
    Execution Circuit

    Stable runtime attachment point for cognitive execution.

    The circuit receives CTF from the Runtime Composition Root.
    """

    CIRCUIT_ID = "execution"

    def __init__(
        self,
        ctf: CognitiveTransitFabric,
    ) -> None:
        self.ctf = ctf
        self._ready = False

    def manifest(self) -> CircuitManifest:
        return CircuitManifest(
            circuit_id=self.CIRCUIT_ID,
            name="Execution Circuit",
            purpose=(
                "Provides the runtime attachment point for cognitive "
                "execution through the Cognitive Transit Fabric."
            ),
            dependencies=[
                "registry",
            ],
            provides=[
                "ctf",
                "route_execution",
                "cognitive_pathways",
            ],
        )

    def boot(self, runtime: Any) -> None:
        runtime.ctf = self.ctf
        runtime.execution_circuit = self

        if hasattr(runtime, "registry"):
            runtime.registry.register(
                self.ctf.runtime_component()
            )

        self._ready = True

    def shutdown(self) -> None:
        self._ready = False

    def health(self) -> CircuitHealth:
        if not self._ready:
            return CircuitHealth(
                circuit_id=self.CIRCUIT_ID,
                status=CircuitStatus.INITIALIZING,
                score=50,
                message="Execution Circuit has not completed boot.",
            )

        stats = self.ctf.statistics()

        return CircuitHealth(
            circuit_id=self.CIRCUIT_ID,
            status=CircuitStatus.READY,
            score=100,
            message="Execution Circuit ready.",
            metrics={
                "registered_routes": len(stats["routes"]),
                "recorded_pathways": stats["pathways"],
            },
        )

    def register_route(
        self,
        route_key: str,
        handler,
    ) -> None:
        self.ctf.register(route_key, handler)

    def execute(
        self,
        route_key: str,
        payload: Dict[str, Any],
        *,
        intent_id: str | None = None,
        source: str = "runtime",
    ):
        return self.ctf.execute(
            route_key=route_key,
            payload=payload,
            intent_id=intent_id,
            source=source,
        )
