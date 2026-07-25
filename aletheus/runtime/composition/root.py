from aletheus.runtime.boot_pipeline import (
    build_runtime_boot_pipeline,
)
from aletheus.runtime.capabilities import (
    RuntimeCapabilityRegistry,
)
from aletheus.runtime.health import (
    RuntimeHealthMonitor,
)
from aletheus.runtime.kernel import (
    RuntimeKernel,
)
from aletheus.runtime.lifecycle import (
    RuntimeLifecycleManager,
)
from aletheus.runtime.orchestration import (
    RuntimeOrchestrator,
)
from aletheus.runtime.policy import (
    RuntimePolicyEngine,
)
from aletheus.runtime.providers import (
    RuntimeServiceProvider,
)
from aletheus.runtime.recovery import (
    RuntimeRecoveryManager,
)


class RuntimeCompositionRoot:
    """
    Runtime Composition Root™

    Assembles the runtime.
    """

    def build_kernel(self):

        orchestrator = RuntimeOrchestrator(
            lifecycle=RuntimeLifecycleManager(),
            service_provider=RuntimeServiceProvider(),
            health_monitor=RuntimeHealthMonitor(),
            recovery_manager=RuntimeRecoveryManager(),
            capability_registry=RuntimeCapabilityRegistry(),
            policy_engine=RuntimePolicyEngine(),
        )

        return RuntimeKernel(
            orchestrator=orchestrator,
            boot_pipeline=build_runtime_boot_pipeline(),
        )

    def boot(self, runtime):

        runtime.kernel = self.build_kernel()

        runtime.kernel.boot(runtime)

        return runtime
