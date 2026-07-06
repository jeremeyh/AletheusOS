class Kernel:
    def __init__(self):
        self.services = {}

    def register_service(self, name: str, service):
        self.services[name] = service
        return service

    def resolve_service(self, name: str):
        if name not in self.services:
            raise KeyError(f"Service not registered: {name}")
        return self.services[name]

    def has_service(self, name: str) -> bool:
        return name in self.services
