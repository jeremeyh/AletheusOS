from __future__ import annotations

import uuid
from typing import Any

from aletheus.runtime_registry_v2.models import (
    ComponentHealth,
    RuntimeCharacteristic,
    RuntimeComponent,
    RuntimeLayer,
)

from .models import CTFRouteRequest
from .registry import CTFRegistry
from .router import CTFRouter


class CognitiveTransitFabric:
    """
    Cognitive Transit Fabric (CTF)

    Constitutional Responsibility
    -----------------------------
    Route cognition throughout AletheusOS.

    CTF is infrastructure.

    It does not:
        - reason
        - learn
        - optimize
        - govern

    It simply moves cognition efficiently.
    """

    COMPONENT_ID = "ctf"

    def __init__(self):

        self.registry = CTFRegistry()
        self.router = CTFRouter(self.registry)

    # ---------------------------------------------------------
    # Runtime Registration
    # ---------------------------------------------------------

    def runtime_component(self) -> RuntimeComponent:

        return RuntimeComponent(
            component_id=self.COMPONENT_ID,
            name="Cognitive Transit Fabric",
            layer=RuntimeLayer.INFRASTRUCTURE,
            purpose="Routes cognition between platform capabilities.",
            version="1.0.0",
            health=ComponentHealth.HEALTHY,
            runtime_characteristics=[
                RuntimeCharacteristic.NIMBLE,
                RuntimeCharacteristic.ELASTIC,
                RuntimeCharacteristic.OBSERVABLE,
                RuntimeCharacteristic.EFFICIENT,
            ],
            provides=[
                "routing",
                "pathway_registry",
            ],
            dependencies=[],
        )

    # ---------------------------------------------------------
    # Route Registration
    # ---------------------------------------------------------

    def register(
        self,
        route_key: str,
        handler,
    ):

        self.registry.register_route(
            route_key,
            handler,
        )

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    def execute(
        self,
        route_key: str,
        payload: dict[str, Any],
        *,
        intent_id: str | None = None,
        source: str = "runtime",
    ):

        request = CTFRouteRequest(
            request_id=str(uuid.uuid4()),
            intent_id=intent_id,
            route_key=route_key,
            payload=payload,
            source=source,
        )

        return self.router.route(request)

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def statistics(self):

        return {
            "routes": self.registry.routes(),
            "pathways": len(self.registry.pathways()),
        }

    def boot_summary(self):

        stats = self.statistics()

        return {
            "component": "CTF",
            "registered_routes": len(stats["routes"]),
            "recorded_pathways": stats["pathways"],
        }
