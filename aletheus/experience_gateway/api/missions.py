"""Mission HTTP routes for the AletheusOS Experience Gateway."""

from __future__ import annotations

from typing import Any, Protocol

from ..service import ExperienceGatewayService
from .runtime import load_missions


class RouteApplication(Protocol):
    """Minimum application contract required to install GET routes."""

    def get(
        self,
        path: str,
        **kwargs: Any,
    ) -> Any: ...


def install_mission_routes(
    app: RouteApplication,
    gateway: ExperienceGatewayService,
) -> None:
    """Install the bounded mission API."""

    @app.get(
        "/api/missions",
        tags=["missions"],
    )
    async def missions() -> list[Any]:
        return load_missions(gateway)
