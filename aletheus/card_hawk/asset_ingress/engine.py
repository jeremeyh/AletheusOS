from __future__ import annotations

from typing import Any

from .models import CardIdentity


class Engine:
    REQUIRED = frozenset({"asset_id", "player", "sport", "year", "product"})

    def ingest(self, payload: dict[str, Any]) -> CardIdentity:
        missing = sorted(self.REQUIRED.difference(payload))
        if missing:
            raise ValueError(f"Missing required card fields: {missing}")
        return CardIdentity(
            asset_id=str(payload["asset_id"]),
            player=str(payload["player"]),
            sport=str(payload["sport"]),
            year=int(payload["year"]),
            product=str(payload["product"]),
            card_number=payload.get("card_number"),
            serial_number=payload.get("serial_number"),
            grade=payload.get("grade"),
            autograph=bool(payload.get("autograph", False)),
            patch=bool(payload.get("patch", False)),
        )
