from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ComponentDescriptor:
    """
    Canonical description of a discoverable AletheusOS component.
    """

    component_id: str

    name: str

    package: str

    category: str

    owner: str

    version: str

    genesis: str

    enabled: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)
