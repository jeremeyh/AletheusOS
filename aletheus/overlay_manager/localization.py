from __future__ import annotations


class OverlayLocalizationService:
    GENESIS = "21.5"
    VERSION = "0.1.0"

    def localize(self, definition: dict, locale: str = "en-US"):
        localized = dict(definition)
        localized["locale"] = locale
        return localized


overlay_localization_service = OverlayLocalizationService()
