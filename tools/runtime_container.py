from aletheus.runtime.container import RuntimeContainer

container = RuntimeContainer()

container.register("memory", object())
container.register("knowledge", object())
container.register("scheduler", object())

print("========================================================")
print("ALETHEUSOS RUNTIME CONTAINER")
print("========================================================")
print()

for service in container.services():
    print(service)

print()
print("Registered Services............", len(container.services()))
print("========================================================")
