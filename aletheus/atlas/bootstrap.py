from __future__ import annotations

from .service import AtlasService


def bootstrap_atlas_service() -> AtlasService:
    return AtlasService()
