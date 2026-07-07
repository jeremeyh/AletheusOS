from aletheus.runtime.capabilities import RuntimeCapabilityRegistry
from aletheus.runtime.container import RuntimeContainer
from aletheus.runtime.health import RuntimeHealthMonitor
from aletheus.runtime.lifecycle import RuntimeLifecycleManager
from aletheus.runtime.orchestration import RuntimeOrchestrator
from aletheus.runtime.providers import RuntimeServiceProvider
from aletheus.runtime.recovery import RuntimeRecoveryManager


def main():
    orchestrator = RuntimeOrchestrator(
        lifecycle=RuntimeLifecycleManager(),
        service_provider=RuntimeServiceProvider(),
        health_monitor=RuntimeHealthMonitor(),
        recovery_manager=RuntimeRecoveryManager(),
        capability_registry=RuntimeCapabilityRegistry(),
    )

    container = RuntimeContainer()

    print("========================================================")
    print("ALETHEUSOS RUNTIME ORCHESTRATION CHECKPOINT")
    print("========================================================")
    print()
    print(f"Lifecycle.......................{orchestrator.lifecycle.state.value}")
    print(f"Container Services..............{len(container.services())}")
    print(f"Capabilities....................{orchestrator.capability_registry.count()}")
    print()
    print("Status..........................READY FOR RUNTIME INTEGRATION")
    print("========================================================")


if __name__ == "__main__":
    main()
