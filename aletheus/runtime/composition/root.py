from aletheus.runtime.boot_pipeline import build_runtime_boot_pipeline
from aletheus.runtime.capabilities import RuntimeCapabilityRegistry
from aletheus.runtime.health import RuntimeHealthMonitor
from aletheus.runtime.lifecycle import RuntimeLifecycleManager
from aletheus.runtime.orchestration import RuntimeOrchestrator
from aletheus.runtime.providers import RuntimeServiceProvider
from aletheus.runtime.recovery import RuntimeRecoveryManager


class RuntimeCompositionRoot:
    """
    Runtime Composition Root™

    Owns runtime startup handoff and orchestration wiring.
    """

    def build_orchestrator(self):
        return RuntimeOrchestrator(
            lifecycle=RuntimeLifecycleManager(),
            service_provider=RuntimeServiceProvider(),
            health_monitor=RuntimeHealthMonitor(),
            recovery_manager=RuntimeRecoveryManager(),
            capability_registry=RuntimeCapabilityRegistry(),
        )

    def boot(self, runtime):
        runtime.orchestrator = self.build_orchestrator()

        build_runtime_boot_pipeline().run(runtime)

        return runtime
