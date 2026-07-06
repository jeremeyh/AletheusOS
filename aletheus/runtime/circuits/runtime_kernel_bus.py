from __future__ import annotations

from typing import Dict, List, Optional

from aletheus.runtime.circuits.anchor_circuit import (
    CircuitHealth,
    RuntimeAnchorCircuit,
)


class RuntimeKernelBus:
    """
    Runtime Kernel Bus

    Stable attachment bus between the AletheusOS runtime core and
    Runtime Anchor Circuits.
    """

    def __init__(self) -> None:
        self._circuits: Dict[str, RuntimeAnchorCircuit] = {}

    def attach(
        self,
        circuit: RuntimeAnchorCircuit,
    ) -> None:
        manifest = circuit.manifest()
        circuit_id = manifest.circuit_id

        if circuit_id in self._circuits:
            raise ValueError(
                f"Runtime Anchor Circuit '{circuit_id}' is already attached."
            )

        self._circuits[circuit_id] = circuit

    def detach(
        self,
        circuit_id: str,
    ) -> None:
        circuit = self._circuits.get(circuit_id)

        if circuit:
            circuit.shutdown()

        self._circuits.pop(circuit_id, None)

    def circuit(
        self,
        circuit_id: str,
    ) -> Optional[RuntimeAnchorCircuit]:
        return self._circuits.get(circuit_id)

    def circuits(self) -> List[RuntimeAnchorCircuit]:
        return list(self._circuits.values())

    def manifests(self) -> list:
        return [
            circuit.manifest()
            for circuit in self._circuits.values()
        ]

    def boot(
        self,
        runtime,
    ) -> None:
        for circuit in self._circuits.values():
            circuit.boot(runtime)

    def shutdown(self) -> None:
        for circuit in reversed(
            list(self._circuits.values())
        ):
            circuit.shutdown()

    def health(self) -> List[CircuitHealth]:
        return [
            circuit.health()
            for circuit in self._circuits.values()
        ]

    def summary(self) -> dict:
        return {
            "bus": "Runtime Kernel Bus",
            "attached_circuits": len(self._circuits),
            "circuits": [
                {
                    "id": circuit.manifest().circuit_id,
                    "name": circuit.manifest().name,
                    "provides": circuit.manifest().provides,
                    "dependencies": circuit.manifest().dependencies,
                }
                for circuit in self._circuits.values()
            ],
        }

    def is_attached(
        self,
        circuit_id: str,
    ) -> bool:
        return circuit_id in self._circuits
