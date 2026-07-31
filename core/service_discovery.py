"""
Automatic Service Discovery
"""

import importlib
import pkgutil

from core.service_adapter import ServiceAdapter
from core.service_registry import service_registry


class ServiceDiscovery:
    def discover(self, package):

        package = importlib.import_module(package)

        discovered = []

        registered = []

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            full = f"{package.__name__}.{module_name}"

            try:
                module = importlib.import_module(full)

                discovered.append(full)

                if hasattr(module, "SERVICE"):
                    service = module.SERVICE

                else:
                    service = ServiceAdapter(module)

                service_registry.register(service.name, service)

                registered.append(service.name)

            except Exception as exc:
                print("Service skipped:", full, exc)

        return discovered, registered


service_discovery = ServiceDiscovery()
