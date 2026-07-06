from __future__ import annotations


class OverlayThemeService:
    GENESIS = "21.5"
    VERSION = "0.1.0"

    def theme(self, application: str):
        return {
            "application": application,
            "theme": "default",
            "status": "planned",
        }


overlay_theme_service = OverlayThemeService()
