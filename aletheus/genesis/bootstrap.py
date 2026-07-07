from __future__ import annotations

from .service import GenesisService


def bootstrap_genesis_service() -> GenesisService:
    return GenesisService()
