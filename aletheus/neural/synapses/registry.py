from __future__ import annotations

from .models import Synapse


class SynapseRegistry:
    """
    Synapse Registry™

    Maintains adaptive neural pathways.
    """

    GENESIS = "6.3"

    VERSION = "0.2.0"

    def __init__(self):

        self._synapses: dict[str, Synapse] = {}

    def register(
        self,
        id: str,
        source: str,
        target: str,
        purpose: str,
        status: str = "inactive",
        metadata: dict | None = None,
    ):

        synapse = Synapse(
            id=id,
            source=source,
            target=target,
            purpose=purpose,
            status=status,
            metadata=metadata or {},
        )

        self._synapses[id] = synapse

        return synapse

    def fire(self, id: str):

        if id in self._synapses:

            self._synapses[id].fire()

    def decay_all(self):

        for synapse in self._synapses.values():

            synapse.decay()

    def get(self, id: str):

        return self._synapses.get(id)

    def list(self):

        return list(self._synapses.values())

    def count(self):

        return len(self._synapses)

    def health(self):

        return {
            "name": "Synapse Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "synapses": self.count(),
        }

    def statistics(self):

        return {
            "name": "Synapse Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "synapses": self.count(),
            "average_strength": (
                round(
                    sum(
                        s.strength
                        for s in self._synapses.values()
                    ) / len(self._synapses),
                    3,
                )
                if self._synapses
                else 0
            ),
            "total_activations": sum(
                s.activations
                for s in self._synapses.values()
            ),
        }
