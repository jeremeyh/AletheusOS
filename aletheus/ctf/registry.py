from __future__ import annotations

from collections.abc import Callable

from .models import CTFPathway


class CTFRegistry:
    """
    Canonical registry for the Cognitive Transit Fabric.

    Responsibilities
    ----------------
    - Register destinations
    - Resolve destinations
    - Record cognitive pathways

    This class intentionally performs no routing,
    optimization, learning, or reasoning.
    """

    def __init__(self):

        self._routes: dict[str, Callable] = {}

        self._pathways: dict[str, CTFPathway] = {}

    # ---------------------------------------------------------
    # Route Registration
    # ---------------------------------------------------------

    def register_route(
        self,
        route_key: str,
        handler: Callable,
    ) -> None:

        if route_key in self._routes:
            raise ValueError(f"Route '{route_key}' already exists.")

        self._routes[route_key] = handler

    def unregister_route(
        self,
        route_key: str,
    ) -> None:

        self._routes.pop(route_key, None)

    # ---------------------------------------------------------
    # Route Lookup
    # ---------------------------------------------------------

    def resolve(
        self,
        route_key: str,
    ) -> Callable | None:

        return self._routes.get(route_key)

    def route_exists(
        self,
        route_key: str,
    ) -> bool:

        return route_key in self._routes

    def routes(self) -> list[str]:

        return sorted(self._routes.keys())

    # ---------------------------------------------------------
    # Pathways
    # ---------------------------------------------------------

    def register_pathway(
        self,
        pathway: CTFPathway,
    ) -> None:

        self._pathways[pathway.pathway_id] = pathway

    def pathway(
        self,
        pathway_id: str,
    ) -> CTFPathway | None:

        return self._pathways.get(pathway_id)

    def pathways(self) -> list[CTFPathway]:

        return list(self._pathways.values())

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(self) -> dict[str, int]:

        return {
            "routes": len(self._routes),
            "pathways": len(self._pathways),
        }

    # ---------------------------------------------------------
    # Maintenance
    # ---------------------------------------------------------

    def clear_routes(self) -> None:

        self._routes.clear()

    def clear_pathways(self) -> None:

        self._pathways.clear()

    def clear(self) -> None:

        self.clear_routes()
        self.clear_pathways()
