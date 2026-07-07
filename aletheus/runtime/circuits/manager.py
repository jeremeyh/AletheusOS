from datetime import datetime, UTC

from .models import RuntimeCircuit, CircuitActivationResult


class RuntimeCircuitManager:
    """
    Runtime Anchor Circuit Manager™

    Manages stable attachment pathways between the AletheusOS Runtime
    and bounded platform capabilities.

    Circuits do not implement capabilities.
    They attach, activate, detach, and report attachment health.
    """

    def __init__(self):
        self.circuits: dict[str, RuntimeCircuit] = {}
        self.activation_history: list[CircuitActivationResult] = []

    def register_circuit(
        self,
        name: str,
        capability: str,
        dependencies: list[str] | None = None,
        metadata: dict | None = None,
    ) -> RuntimeCircuit:
        circuit = RuntimeCircuit(
            name=name,
            capability=capability,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )

        self.circuits[name] = circuit
        return circuit

    def has_circuit(self, name: str) -> bool:
        return name in self.circuits

    def activate(self, name: str) -> CircuitActivationResult:
        circuit = self.circuits.get(name)

        if circuit is None:
            result = CircuitActivationResult(
                circuit=name,
                status="missing",
                message=f"Circuit '{name}' is not registered.",
            )
            self.activation_history.append(result)
            return result

        missing_dependencies = [
            dependency
            for dependency in circuit.dependencies
            if dependency not in self.circuits
        ]

        if missing_dependencies:
            result = CircuitActivationResult(
                circuit=name,
                status="blocked",
                message="Circuit dependencies are missing.",
                metadata={"missing_dependencies": missing_dependencies},
            )
            self.activation_history.append(result)
            return result

        circuit.status = "active"
        circuit.updated_at = datetime.now(UTC).isoformat()

        result = CircuitActivationResult(
            circuit=name,
            status="active",
            message=f"Circuit '{name}' activated.",
            metadata={"capability": circuit.capability},
        )

        self.activation_history.append(result)
        return result

    def detach(self, name: str) -> CircuitActivationResult:
        circuit = self.circuits.get(name)

        if circuit is None:
            result = CircuitActivationResult(
                circuit=name,
                status="missing",
                message=f"Circuit '{name}' is not registered.",
            )
            self.activation_history.append(result)
            return result

        circuit.status = "detached"
        circuit.updated_at = datetime.now(UTC).isoformat()

        result = CircuitActivationResult(
            circuit=name,
            status="detached",
            message=f"Circuit '{name}' detached.",
            metadata={"capability": circuit.capability},
        )

        self.activation_history.append(result)
        return result

    def active_circuits(self):
        return [
            circuit
            for circuit in self.circuits.values()
            if circuit.status == "active"
        ]

    def health(self):
        active = self.active_circuits()

        return {
            "status": "online",
            "registered_circuits": len(self.circuits),
            "active_circuits": len(active),
            "activation_events": len(self.activation_history),
            "circuits": {
                name: {
                    "capability": circuit.capability,
                    "status": circuit.status,
                    "dependencies": list(circuit.dependencies),
                }
                for name, circuit in self.circuits.items()
            },
        }
