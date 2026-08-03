from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AccessibilityProfile:
    reduced_motion: bool = False
    high_contrast: bool = False
    large_text: bool = False
    screen_reader: bool = False
    input_mode: str = "pointer"


class Engine:
    def adapt(
        self, profile: AccessibilityProfile, *, viewport_width: int
    ) -> dict[str, object]:
        density = (
            "compact"
            if viewport_width < 640
            else "comfortable"
            if viewport_width < 1024
            else "expansive"
        )
        return {
            "density": density,
            "motion": "reduced" if profile.reduced_motion else "full",
            "contrast": "high" if profile.high_contrast else "standard",
            "text_scale": 1.25 if profile.large_text else 1.0,
            "screen_reader": profile.screen_reader,
            "input_mode": profile.input_mode,
        }
