"""Platform Service Registry public API."""

from .exceptions import (
    PlatformServiceRegistryError,
    ServiceAlreadyRegisteredError,
    ServiceDependencyError,
    ServiceInUseError,
    ServiceNotFoundError,
)
from .models import (
    PlatformServiceDefinition,
    PlatformServiceRegistryStatistics,
)
from .registry import PlatformServiceRegistry

__all__ = [
    "PlatformServiceDefinition",
    "PlatformServiceRegistry",
    "PlatformServiceRegistryError",
    "PlatformServiceRegistryStatistics",
    "ServiceAlreadyRegisteredError",
    "ServiceDependencyError",
    "ServiceInUseError",
    "ServiceNotFoundError",
]
