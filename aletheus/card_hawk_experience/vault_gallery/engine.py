from __future__ import annotations

from typing import ClassVar

from .models import ExperienceAction, ExperienceSurface, HydrationSource, SurfaceKind


class Engine:
    VAULT: ClassVar[ExperienceSurface] = ExperienceSurface(
        "vault",
        "Vault™",
        "Canonical collection inventory and digital-twin ownership environment.",
        SurfaceKind.ROOM,
        (
            HydrationSource("Asset Vault"),
            HydrationSource("Mammoth"),
            HydrationSource("Collectibles Evidence Graph"),
            HydrationSource("Valuation Determination Engine"),
            HydrationSource("A•3ye Perception"),
        ),
        ("A•3ye", "Evidence", "Memory", "Truth", "Knowledge"),
        (
            ExperienceAction("add_asset", "Add Asset", "ADD_ASSET"),
            ExperienceAction("open_asset", "Open Asset", "OPEN_ASSET"),
            ExperienceAction(
                "export_inventory", "Export Inventory", "EXPORT_INVENTORY"
            ),
        ),
        metadata={
            "regions": (
                "inventory",
                "images",
                "certificates",
                "grades",
                "receipts",
                "insurance",
                "storage",
                "condition",
                "valuation",
                "provenance",
                "history",
            )
        },
    )
    GALLERY: ClassVar[ExperienceSurface] = ExperienceSurface(
        "gallery",
        "Gallery™",
        "Emotion-forward visual showcase for collections, themes, stories, and exhibitions.",
        SurfaceKind.ROOM,
        (
            HydrationSource("Asset Vault"),
            HydrationSource("Memory Engine"),
            HydrationSource("Nimble"),
            HydrationSource("AxiomUX Projection Protocol"),
        ),
        ("A•3ye", "Memory", "Knowledge"),
        (
            ExperienceAction("create_exhibit", "Create Exhibit", "CREATE_EXHIBIT"),
            ExperienceAction("present", "Presentation Mode", "OPEN_PRESENTATION_MODE"),
            ExperienceAction("share", "Share Showcase", "SHARE_SHOWCASE", True),
        ),
        metadata={
            "regions": (
                "favorites",
                "themes",
                "stories",
                "exhibitions",
                "virtual_shelf",
                "wall_display",
                "tv_mode",
                "presentation_mode",
            )
        },
    )

    def vault(self):
        return self.VAULT

    def gallery(self):
        return self.GALLERY
