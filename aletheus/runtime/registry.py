"""
AletheusOS Runtime Registry Compatibility Module

Provides backwards-compatible access to the canonical
ServiceRegistry implementation.

Canonical implementation:
aletheus.runtime.services.service_registry.ServiceRegistry
"""

from __future__ import annotations

from aletheus.runtime.services.service_registry import ServiceRegistry

__all__ = [
    "ServiceRegistry",
]
