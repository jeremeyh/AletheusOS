"""Factory for SPARTAN™."""

from __future__ import annotations

from .domains import DEFAULT_DOMAIN_NAMES, BaselineIntelligenceDomain
from .network import SPARTANNetwork
from .recursive import RecursiveIntelligenceCycle
from .registry import DomainRegistry


def build_spartan(
    enabled_domains: tuple[str, ...] | None = None,
) -> SPARTANNetwork:
    registry = DomainRegistry()

    for name in enabled_domains or DEFAULT_DOMAIN_NAMES:
        registry.register(BaselineIntelligenceDomain(name=name))

    return SPARTANNetwork(
        registry=registry,
        recursive_cycle=RecursiveIntelligenceCycle(),
    )
