from aletheus.runtime.capabilities import (
    RuntimeCapabilityRegistry,
    RuntimeCapabilitySynchronizer,
)
from aletheus.runtime.container import RuntimeContainer


container = RuntimeContainer()
registry = RuntimeCapabilityRegistry()

container.register("memory", object())
container.register("knowledge", object())
container.register("scheduler", object())

result = RuntimeCapabilitySynchronizer().sync(
    container,
    registry,
)

print("========================================================")
print("ALETHEUSOS CAPABILITY SYNCHRONIZER")
print("========================================================")
print()

print(f"Synced.........................{result['synced']}")

for capability in registry.names():
    print(capability)

print()
print("========================================================")
