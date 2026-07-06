from __future__ import annotations

from typing import Any

from aletheus.neural.connectome import Connectome
from aletheus.neural.cortex import CortexRegistry
from aletheus.neural.neurons import NeuronRegistry
from aletheus.neural.state import BrainStateManager
from aletheus.neural.synapses import SynapseRegistry

from .bootstrap import Bootstrap
from .configuration import Configuration
from .health import HealthService
from .lifecycle import Lifecycle
from .statistics import StatisticsService


class NeuralEnvelope:
    """
    Neural Envelope™

    Genesis 6.4

    The bounded intelligence architecture of AletheusOS.

    Core is intentionally thin.

    It coordinates services.

    It owns no business logic.
    """

    GENESIS = "6.4"

    VERSION = "0.5.0"

    def __init__(self):

        #
        # Brain Components
        #

        self.configuration = Configuration()

        self.state = BrainStateManager()

        self.cortex = CortexRegistry()

        self.neurons = NeuronRegistry()

        self.synapses = SynapseRegistry()

        self.connectome = Connectome(self)

        #
        # Services
        #

        self.bootstrap = Bootstrap(self)

        self.lifecycle = Lifecycle(self)

        self.health_service = HealthService(self)

        self.statistics_service = StatisticsService(self)

    #
    # Public API
    #

    def boot(self):

        self.lifecycle.boot()

        return True

    def shutdown(self):

        self.lifecycle.shutdown()

    def sleep(self):

        self.lifecycle.sleep()

    def wake(self):

        self.lifecycle.wake()

    def set_state(self, state: str):

        return self.state.set(state)

    def register_neuron(
        self,
        id: str,
        name: str,
        cortex: str,
        package: str,
        role: str,
        status: str = "online",
        metadata: dict[str, Any] | None = None,
    ):

        return self.neurons.register(
            id=id,
            name=name,
            cortex=cortex,
            package=package,
            role=role,
            status=status,
            metadata=metadata,
        )

    def connect(
        self,
        id: str,
        source: str,
        target: str,
        purpose: str,
        status: str = "active",
        metadata: dict[str, Any] | None = None,
    ):

        return self.synapses.register(
            id=id,
            source=source,
            target=target,
            purpose=purpose,
            status=status,
            metadata=metadata,
        )

    def health(self):

        return self.health_service.report()

    def statistics(self):

        return self.statistics_service.report()


neural_envelope = NeuralEnvelope()

brain = neural_envelope
