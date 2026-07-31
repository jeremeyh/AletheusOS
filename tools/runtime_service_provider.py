from aletheus.runtime.providers import RuntimeServiceProvider


class DummyRegistry(dict):
    def register(self, name, service):
        self[name] = service


class DummyRuntime:
    def __init__(self):

        self.services = DummyRegistry()

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

RuntimeServiceProvider().register(runtime)

print("========================================================")
print("ALETHEUSOS SERVICE PROVIDER")
print("========================================================")
print()

for service in runtime.services:
    print(service)

print()
print("Registered Services............", len(runtime.services))
print("========================================================")
