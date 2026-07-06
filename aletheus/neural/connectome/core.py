from __future__ import annotations

from collections import deque
from typing import Any


class Connectome:
    """
    Connectome™

    Graph intelligence layer for the Neural Envelope.

    It does not execute cognition.
    It maps relationships between neurons and synapses.
    """

    GENESIS = "6.4"
    VERSION = "0.1.0"

    def __init__(self, brain):
        self.brain = brain

    def neurons(self):
        return self.brain.neurons.list()

    def synapses(self):
        return self.brain.synapses.list()

    def neighbors(self, neuron_id: str) -> list[str]:
        linked = []

        for synapse in self.synapses():
            if synapse.source == neuron_id:
                linked.append(synapse.target)
            elif synapse.target == neuron_id:
                linked.append(synapse.source)

        return sorted(set(linked))

    def outgoing(self, neuron_id: str):
        return [
            synapse
            for synapse in self.synapses()
            if synapse.source == neuron_id
        ]

    def incoming(self, neuron_id: str):
        return [
            synapse
            for synapse in self.synapses()
            if synapse.target == neuron_id
        ]

    def path(self, source: str, target: str) -> list[str]:
        if source == target:
            return [source]

        visited = {source}
        queue = deque([[source]])

        while queue:
            current_path = queue.popleft()
            current = current_path[-1]

            for neighbor in self.neighbors(current):
                if neighbor in visited:
                    continue

                next_path = current_path + [neighbor]

                if neighbor == target:
                    return next_path

                visited.add(neighbor)
                queue.append(next_path)

        return []

    def isolated_neurons(self) -> list[str]:
        isolated = []

        for neuron in self.neurons():
            if not self.neighbors(neuron.id):
                isolated.append(neuron.id)

        return sorted(isolated)

    def strongest_synapses(self, limit: int = 10):
        return sorted(
            self.synapses(),
            key=lambda synapse: synapse.strength,
            reverse=True,
        )[:limit]

    def statistics(self) -> dict[str, Any]:
        return {
            "name": "Connectome",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "neurons": len(self.neurons()),
            "synapses": len(self.synapses()),
            "isolated_neurons": len(self.isolated_neurons()),
        }

    def health(self) -> dict[str, Any]:
        return {
            "name": "Connectome",
            "status": "online",
            **self.statistics(),
        }
