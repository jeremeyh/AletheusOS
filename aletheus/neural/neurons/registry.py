from __future__ import annotations

from typing import Any

from .models import Neuron


class NeuronRegistry:
    """
    Neuron Registry™

    Registers functional intelligence units inside the Neural Envelope.
    """

    GENESIS = "6.2"
    VERSION = "0.1.0"

    def __init__(self):
        self._neurons: dict[str, Neuron] = {}

    def register(
        self,
        id: str,
        name: str,
        cortex: str,
        package: str,
        role: str,
        status: str = "inactive",
        metadata: dict[str, Any] | None = None,
    ) -> Neuron:
        neuron = Neuron(
            id=id,
            name=name,
            cortex=cortex,
            package=package,
            role=role,
            status=status,
            metadata=metadata or {},
        )
        self._neurons[id] = neuron
        return neuron

    def get(self, id: str) -> Neuron | None:
        return self._neurons.get(id)

    def list(self) -> list[Neuron]:
        return list(self._neurons.values())

    def by_cortex(self, cortex: str) -> list[Neuron]:
        return [
            neuron
            for neuron in self._neurons.values()
            if neuron.cortex == cortex
        ]

    def count(self) -> int:
        return len(self._neurons)

    def health(self) -> dict:
        return {
            "name": "Neuron Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "neurons": self.count(),
        }

    def statistics(self) -> dict:
        return {
            "name": "Neuron Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "neurons": self.count(),
            "cortices": sorted({n.cortex for n in self._neurons.values()}),
        }
