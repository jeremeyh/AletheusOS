from aletheus.card_hawk_experience.overlay_runtime.engine import Engine
from aletheus.card_hawk_experience.overlay_runtime.models import (
    ExperienceSession,
    SurfaceState,
)


def test_x():
    assert (
        "A•3ye"
        in Engine()
        .open_overlay(ExperienceSession("s", "vault", SurfaceState.READY), "A•3ye")
        .overlay_stack
    )
