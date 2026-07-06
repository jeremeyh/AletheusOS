from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OverlayDefinition:
    overlay_id: str
    application: str
    foundation_engine: str
    display_name: str
    description: str = ""
    category: str = ""
    icon: str = ""
    color: str = ""
    visible: bool = True
    version: str = "1.0.0"
    locale: str = "en-US"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "overlay_id": self.overlay_id,
            "application": self.application,
            "foundation_engine": self.foundation_engine,
            "display_name": self.display_name,
            "description": self.description,
            "category": self.category,
            "icon": self.icon,
            "color": self.color,
            "visible": self.visible,
            "version": self.version,
            "locale": self.locale,
            "metadata": self.metadata,
        }
