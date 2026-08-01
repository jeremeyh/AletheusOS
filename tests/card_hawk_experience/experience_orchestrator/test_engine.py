from aletheus.card_hawk_experience.experience_orchestrator.engine import Engine
from aletheus.card_hawk_experience.experience_orchestrator.models import (
    ExperienceSession,
    ExperienceSurface,
    HydrationSource,
    SurfaceKind,
    SurfaceState,
)


def test_x():
    s = ExperienceSession("s", "vault", SurfaceState.READY)
    v = ExperienceSurface(
        "vault",
        "Vault",
        "x",
        SurfaceKind.ROOM,
        (HydrationSource("Asset Vault"),),
        ("A•3ye",),
    )
    assert Engine().compose(s, v).resolved_overlays == ("A•3ye",)
