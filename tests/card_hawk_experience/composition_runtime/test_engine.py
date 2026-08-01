from aletheus.card_hawk_experience.composition_runtime.engine import Engine
from aletheus.card_hawk_experience.composition_runtime.models import (
    ExperienceSession,
    ExperienceSurface,
    SurfaceKind,
    SurfaceState,
)


def test_x():
    s = ExperienceSession("s", "none", SurfaceState.DORMANT)
    v = ExperienceSurface("vault", "Vault", "x", SurfaceKind.ROOM)
    assert Engine().activate(s, v).active_surface_id == "vault"
