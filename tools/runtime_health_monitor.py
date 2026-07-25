from aletheus.runtime.capabilities import RuntimeCapabilityRegistry
from aletheus.runtime.container import RuntimeContainer
from aletheus.runtime.health import RuntimeHealthMonitor
from aletheus.runtime.lifecycle import (
    RuntimeLifecycleManager,
)

lifecycle = RuntimeLifecycleManager()
container = RuntimeContainer()
registry = RuntimeCapabilityRegistry()

container.register("memory", object())
container.register("knowledge", object())
container.register("scheduler", object())

registry.register("memory", object())
registry.register("knowledge", object())
registry.register("scheduler", object())

lifecycle.online()

health = RuntimeHealthMonitor().collect(
    lifecycle,
    container,
    registry,
)

print("========================================================")
print("ALETHEUSOS RUNTIME HEALTH")
print("========================================================")
print()

for k, v in health.items():
    print(f"{k:<15}: {v}")

print()
print("========================================================")
