from aletheus.runtime.capabilities import RuntimeCapabilityRegistry
from aletheus.runtime.health import RuntimeHealthMonitor
from aletheus.runtime.kernel import RuntimeKernel
from aletheus.runtime.lifecycle import RuntimeLifecycleManager
from aletheus.runtime.orchestration import RuntimeOrchestrator
from aletheus.runtime.providers import RuntimeServiceProvider
from aletheus.runtime.recovery import RuntimeRecoveryManager


orchestrator = RuntimeOrchestrator(
    lifecycle=RuntimeLifecycleManager(),
    service_provider=RuntimeServiceProvider(),
    health_monitor=RuntimeHealthMonitor(),
    recovery_manager=RuntimeRecoveryManager(),
    capability_registry=RuntimeCapabilityRegistry(),
)

kernel = RuntimeKernel(orchestrator)

print("========================================================")
print("ALETHEUSOS RUNTIME KERNEL")
print("========================================================")
print()
print("Kernel..........................ONLINE")
print("Lifecycle.......................", kernel.orchestrator.lifecycle.state.value)
print("========================================================")
