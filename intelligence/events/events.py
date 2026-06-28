"""
CardHawk OS™
Canonical Platform Events
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PlatformEvent:

    name: str

    payload: dict

    created: str = datetime.utcnow().isoformat()


# Asset Lifecycle

ASSET_CREATED = "asset.created"

ASSET_UPDATED = "asset.updated"

ASSET_DELETED = "asset.deleted"

DNA_COMPLETED = "dna.completed"

OCR_COMPLETED = "ocr.completed"

IMAGE_ANALYZED = "image.analyzed"


# Intelligence

THORX_COMPLETED = "thorx.completed"

QDEF_COMPLETED = "qdef.completed"

DDEF_COMPLETED = "ddef.completed"

SCOUT_COMPLETED = "scout.completed"

FOUNDER_UPDATED = "founder.updated"

DIGITAL_TWIN_UPDATED = "digital_twin.updated"

LIVE_DATA_UPDATED = "live_data.updated"

PORTFOLIO_UPDATED = "portfolio.updated"
