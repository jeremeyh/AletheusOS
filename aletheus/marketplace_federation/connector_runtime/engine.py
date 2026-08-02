from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import ClassVar


class Engine:
    CONNECTORS: ClassVar[Mapping[str, tuple[str, ...]]] = MappingProxyType(
        {
            "CARD_HAWK_NATIVE": ("INVENTORY", "BUY", "SELL", "TRADE", "EVENTS"),
            "GENERIC_READ_ONLY": ("INVENTORY", "PRICING", "EVENTS"),
        }
    )

    def capabilities(self, connector_id: str) -> tuple[str, ...]:
        return self.CONNECTORS[connector_id.strip().upper()]
