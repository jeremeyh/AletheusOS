from .models import RuntimeComposition

from aletheus.runtime.boot_pipeline import RuntimeBootPipeline
from aletheus.runtime.lifecycle import RuntimeLifecycleManager
from aletheus.runtime.executive import ExecutiveKernel
from aletheus.runtime.registration import RuntimeRegistrationManager
from aletheus.runtime.commands_v2 import RuntimeCommandRegistry
from aletheus.runtime.circuits import RuntimeCircuitManager
from aletheus.runtime.service_mesh import RuntimeServiceMesh
from aletheus.runtime.relay import RelayNetwork
from aletheus.runtime.catalyst import CatalystOptimizer


class RuntimeCompositionRoot:
    """
    Runtime Composition Root™

    Builds the runtime.

    It owns wiring.

    It owns nothing else.
    """

    def build(self):

        runtime = RuntimeComposition()

        runtime.services["boot_pipeline"] = RuntimeBootPipeline()

        runtime.services["executive_kernel"] = ExecutiveKernel()

        runtime.services["lifecycle"] = RuntimeLifecycleManager()

        runtime.services["registration"] = RuntimeRegistrationManager()

        runtime.services["command_registry"] = RuntimeCommandRegistry()

        runtime.services["circuits"] = RuntimeCircuitManager()

        runtime.services["service_mesh"] = RuntimeServiceMesh()

        runtime.services["relay_network"] = RelayNetwork()

        runtime.services["catalyst"] = CatalystOptimizer()

        return runtime
