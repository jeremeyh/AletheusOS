from __future__ import annotations

from dataclasses import replace
from typing import ClassVar

from .models import ExperienceSession, ExperienceSurface, SurfaceState


class Engine:
    VERSION: ClassVar[str] = "28.0.0"

    def activate(
        self, session: ExperienceSession, surface: ExperienceSurface
    ) -> ExperienceSession:
        return replace(
            session,
            active_surface_id=surface.surface_id,
            state=SurfaceState.HYDRATING,
            surface_stack=session.surface_stack + (surface.surface_id,),
        )

    def mark_ready(self, session: ExperienceSession) -> ExperienceSession:
        return replace(session, state=SurfaceState.READY)
