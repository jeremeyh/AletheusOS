from aletheus.runtime.capabilities import RuntimeCapabilityRegistry

registry = RuntimeCapabilityRegistry()

registry.register("memory", object())
registry.register("knowledge", object())
registry.register("scheduler", object())
registry.register("agents", object())
registry.register("applications", object())

print("========================================================")
print("ALETHEUSOS CAPABILITY REGISTRY")
print("========================================================")
print()

for capability in registry.names():
    print(capability)

print()
print(f"Capability Count...............{registry.count()}")
print("========================================================")
