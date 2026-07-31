from __future__ import annotations


class HealthService:
    VERSION = "0.1.0"

    def __init__(self, brain):
        self.brain = brain

    def report(self):

        return {
            "name": "Neural Envelope",
            "status": self.brain.state.get().name,
            "genesis": self.brain.GENESIS,
            "version": self.brain.VERSION,
            "cortices": self.brain.cortex.count(),
            "neurons": self.brain.neurons.count(),
            "synapses": self.brain.synapses.count(),
            "connectome": self.brain.connectome.health(),
        }
