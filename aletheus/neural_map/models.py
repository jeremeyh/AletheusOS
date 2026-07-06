from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class NeuralNode:
    id: str
    name: str
    package: str
    cortex: str
    role: str
    status: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NeuralSynapse:
    id: str
    source: str
    target: str
    purpose: str
    status: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)
