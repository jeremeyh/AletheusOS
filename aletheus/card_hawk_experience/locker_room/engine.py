from __future__ import annotations

from typing import ClassVar

from .models import ExperienceAction, ExperienceSurface, HydrationSource, SurfaceKind


class Engine:
    SURFACE: ClassVar[ExperienceSurface] = ExperienceSurface(
        surface_id="locker_room",
        display_name="Locker Room™",
        description="Private collector workspace for preparation, organization, planning, and collection building.",
        kind=SurfaceKind.ROOM,
        hydration_sources=(
            HydrationSource("Memory Engine"),
            HydrationSource("Asset Vault"),
            HydrationSource("Knowledge Engine"),
            HydrationSource("Identity and Permissions"),
        ),
        overlays=(
            "A•3ye",
            "Memory",
            "Knowledge",
            "Truth",
        ),
        actions=(
            ExperienceAction(
                "open_collection", "Open Collection", "OPEN_COLLECTION", False, None
            ),
            ExperienceAction(
                "create_wishlist", "Create Wishlist", "CREATE_WISHLIST", False, None
            ),
            ExperienceAction(
                "draft_offer", "Draft Offer", "CREATE_DRAFT_OFFER", False, "war_room"
            ),
        ),
        metadata={
            "regions": (
                "collections",
                "wishlists",
                "saved_searches",
                "draft_offers",
                "personal_notes",
                "acquisition_plans",
                "journal",
            )
        },
    )

    def surface(self) -> ExperienceSurface:
        return self.SURFACE
