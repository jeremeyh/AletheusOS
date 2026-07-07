class RuntimeContainer:
    """
    Runtime Dependency Injection Container™

    Registers and resolves runtime services.
    """

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service
        return service

    def resolve(self, name):
        return self._services[name]

    def contains(self, name):
        return name in self._services

    def services(self):
        return tuple(sorted(self._services.keys()))
