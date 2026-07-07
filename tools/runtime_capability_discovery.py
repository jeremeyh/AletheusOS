from aletheus.runtime.container import RuntimeContainer
from aletheus.runtime.discovery import RuntimeCapabilityDiscovery

container = RuntimeContainer()

container.register("memory", object())
container.register("knowledge", object())
container.register("scheduler", object())
container.register("agents", object())
container.register("applications", object())

caps = RuntimeCapabilityDiscovery().discover(container)

print("========================================================")
print("ALETHEUSOS CAPABILITY DISCOVERY")
print("========================================================")
print()

for capability in caps:
    print(capability)

print()
print(f"Capabilities...................{len(caps)}")
print("========================================================")
