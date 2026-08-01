from aletheus.card_hawk_experience.surface_framework.engine import Engine
from aletheus.card_hawk_experience.surface_framework.models import (
    ExperienceSurface,
    HydrationSource,
    SurfaceKind,
)


def test_x():
    s = ExperienceSurface(
        "vault", "Vault", "x", SurfaceKind.ROOM, (HydrationSource("Asset Vault"),)
    )
    assert Engine().validate(s)["valid"] is True
