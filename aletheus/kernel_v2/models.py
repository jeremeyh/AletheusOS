from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aletheus.time_utils import utc_now_iso


def now() -> str:
    return utc_now_iso()


@dataclass
class KernelEvent:
    event_type: str
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class KernelState:
    version: str = "2.0.0-alpha"
    codename: str = "Autonomous Kernel"
    status: str = "online"
    booted_at: str = field(default_factory=now)
    events: int = 0
    services: int = 0
    applications: int = 0
    missions: int = 0
    agents: int = 0

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class KernelRegistryItem:
    name: str
    item_type: str
    status: str = "registered"
    metadata: dict[str, Any] = field(default_factory=dict)
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
