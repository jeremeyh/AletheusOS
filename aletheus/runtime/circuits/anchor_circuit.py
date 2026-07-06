from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class CircuitStatus(str, Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


@dataclass
class CircuitHealth:
    circuit_id: str
    status: CircuitStatus = CircuitStatus.READY
    score: int = 100
    message: str = "Ready"
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CircuitManifest:
    circuit_id: str
    name: str
    purpose: str
    dependencies: List[str] = field(default_factory=list)
    provides: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class RuntimeAnchorCircuit(ABC):
    """
    Base contract for AletheusOS Runtime Anchor Circuits.
    """

    @abstractmethod
    def manifest(self) -> CircuitManifest:
        pass

    @abstractmethod
    def boot(self, runtime: Any) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    @abstractmethod
    def health(self) -> CircuitHealth:
        pass
