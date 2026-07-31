from __future__ import annotations


class OverlayValidator:
    GENESIS = "21.5"
    VERSION = "0.1.0"

    RESERVED_TERMS = {
        "Principle X",
        "Constitutional Root Authority",
        "Founder Console",
    }

    def validate(self, definition, existing: list[dict] | None = None):
        errors = []

        if not definition.application:
            errors.append("Application is required.")

        if not definition.foundation_engine:
            errors.append("Foundation engine is required.")

        if not definition.display_name:
            errors.append("Display name is required.")

        if definition.display_name in self.RESERVED_TERMS:
            errors.append(f"Display name is reserved: {definition.display_name}")

        existing = existing or []

        for item in existing:
            if (
                item["display_name"] == definition.display_name
                and item["foundation_engine"] != definition.foundation_engine
            ):
                errors.append(
                    f"Duplicate display name in application overlay: {definition.display_name}"
                )

        return {
            "valid": not errors,
            "errors": errors,
        }


overlay_validator = OverlayValidator()
