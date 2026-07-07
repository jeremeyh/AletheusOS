from aletheus.runtime.capabilities import RuntimeCapabilityRegistry
from aletheus.runtime.container import RuntimeContainer
from aletheus.runtime.health import RuntimeHealthMonitor
from aletheus.runtime.lifecycle import RuntimeLifecycleManager
from aletheus.runtime.orchestration import RuntimeOrchestrator
from aletheus.runtime.providers import RuntimeServiceProvider
from aletheus.runtime.recovery import RuntimeRecoveryManager


class DummyRuntime:

    def __init__(self):

        class Services(dict):

            def register(self, name, service):
                self[name] = service

        self.services = Services()

        self.commands = object()
        self.events = object()
        self.metrics = object()
        self.compat = object()
        self.kernel = object()
        self.governance = object()
        self.runtime_doctor = object()
        self.boot_validator = object()
        self.runtime_invariants = object()


runtime = DummyRuntime()

container = RuntimeContainer()
registry = RuntimeCapabilityRegistry()

orchestrator = RuntimeOrchestrator(
    lifecycle=RuntimeLifecycleManager(),
    service_provider=RuntimeServiceProvider(),
    health_monitor=RuntimeHealthMonitor(),
    recovery_manager=RuntimeRecoveryManager(),
    capability_registry=registry,
)

orchestrator.boot(runtime)

print("========================================================")
print("ALETHEUSOS RUNTIME ORCHESTRATOR")
print("========================================================")
print()

print("Lifecycle:", orchestrator.lifecycle.state.value)
print("Services :", len(runtime.services))

print()
print("========================================================")
