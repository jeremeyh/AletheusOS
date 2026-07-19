"""Exceptions for the Platform Service Registry."""

from __future__ import annotations


class PlatformServiceRegistryError(Exception):
    """Base exception for Platform Service Registry failures."""


class ServiceAlreadyRegisteredError(
    PlatformServiceRegistryError
):
    """Raised when a service address is registered more than once."""


class ServiceNotFoundError(
    PlatformServiceRegistryError
):
    """Raised when a requested service is not registered."""


class ServiceDependencyError(
    PlatformServiceRegistryError
):
    """Raised when service dependencies violate registry policy."""


class ServiceInUseError(
    PlatformServiceRegistryError
):
    """Raised when removing a service would break dependents."""
