from __future__ import annotations

from dataclasses import dataclass

from aletheus.ctf.engine import CognitiveTransitFabric
from aletheus.runtime.circuits import (
    ExecutionCircuit,
    RegistryCircuit,
    RuntimeKernelBus,
)
from aletheus.runtime.managers import RegistryManager
from aletheus.runtime_registry_v2.core import RuntimeRegistry
from aletheus.runtime_registry_v2.health import HealthMonitor


@dataclass
class RuntimeComposition:
    """
    Fully assembled runtime object graph.

    The composition root owns construction.
    Runtime Core owns orchestration.
    Circuits expose stable kernel attachment points.
    Managers coordinate services.
    Services own behavior and state.
    """

    kernel_bus: RuntimeKernelBus
    registry: RuntimeRegistry
    health_monitor: HealthMonitor
    registry_manager: RegistryManager
    ctf: CognitiveTransitFabric
    registry_circuit: RegistryCircuit
    execution_circuit: ExecutionCircuit


class RuntimeCompositionRoot:
    """
    Runtime Composition Root

    Sole responsibility:
        Build and return the runtime object graph.
    """

    def build(self) -> RuntimeComposition:
        registry = RuntimeRegistry()
        health_monitor = HealthMonitor()

        registry_manager = RegistryManager(
            registry=registry,
            health_monitor=health_monitor,
        )

        ctf = CognitiveTransitFabric()

        registry_circuit = RegistryCircuit(
            manager=registry_manager,
        )

        execution_circuit = ExecutionCircuit(
            ctf=ctf,
        )

        kernel_bus = RuntimeKernelBus()

        kernel_bus.attach(registry_circuit)
        kernel_bus.attach(execution_circuit)

        return RuntimeComposition(
            kernel_bus=kernel_bus,
            registry=registry,
            health_monitor=health_monitor,
            registry_manager=registry_manager,
            ctf=ctf,
            registry_circuit=registry_circuit,
            execution_circuit=execution_circuit,
        )
