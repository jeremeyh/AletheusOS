from __future__ import annotations


class StatisticsService:

    VERSION = "0.1.0"

    def __init__(self, brain):
        self.brain = brain

    def report(self):

        return {

            "brain": self.brain.state.statistics(),

            "cortex": self.brain.cortex.health(),

            "neurons": self.brain.neurons.statistics(),

            "synapses": self.brain.synapses.statistics(),

            "connectome": self.brain.connectome.statistics(),
        }
