from aletheus.strategic.runtime import (
    RuntimeCapabilityStatus,
    install_span_runtime,
)


class Registry:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service


def test_install_registers_and_starts_span():
    registry = Registry()

    service = install_span_runtime(registry)

    assert registry.services["span"] is service
    assert service.status is RuntimeCapabilityStatus.RUNNING


def test_install_can_leave_service_initialized():
    registry = Registry()

    service = install_span_runtime(registry, auto_start=False)

    assert service.status is RuntimeCapabilityStatus.INITIALIZED
