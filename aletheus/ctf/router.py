from __future__ import annotations

import time
import uuid
from collections.abc import Callable

from .models import (
    CTFPathway,
    CTFRouteRequest,
    CTFRouteResult,
    CTFRouteStatus,
)
from .registry import CTFRegistry


class CTFRouter:
    """
    Cognitive Transit Fabric Router

    Responsibilities
    ----------------
    - Accept route requests
    - Resolve destinations
    - Execute handlers
    - Measure execution latency
    - Record cognitive pathways

    The router deliberately performs no reasoning,
    optimization, caching, or learning.
    """

    def __init__(self, registry: CTFRegistry):

        self.registry = registry

    # ---------------------------------------------------------
    # Route Execution
    # ---------------------------------------------------------

    def route(
        self,
        request: CTFRouteRequest,
    ) -> CTFRouteResult:

        handler: Callable | None = self.registry.resolve(
            request.route_key
        )

        if handler is None:

            return CTFRouteResult(
                request_id=request.request_id,
                route_key=request.route_key,
                destination=None,
                status=CTFRouteStatus.FAILED,
                error=f"No route registered for '{request.route_key}'.",
            )

        start = time.perf_counter()

        try:

            result = handler(request.payload)

            elapsed_ms = (
                time.perf_counter() - start
            ) * 1000.0

            pathway = CTFPathway(
                pathway_id=str(uuid.uuid4()),
                route_key=request.route_key,
                nodes=[
                    request.source,
                    "ctf",
                    request.route_key,
                ],
                success_count=1,
                average_latency_ms=round(
                    elapsed_ms,
                    3,
                ),
            )

            self.registry.register_pathway(pathway)

            return CTFRouteResult(
                request_id=request.request_id,
                route_key=request.route_key,
                destination=request.route_key,
                status=CTFRouteStatus.COMPLETED,
                result=result,
                pathway_id=pathway.pathway_id,
                metadata={
                    "latency_ms": round(
                        elapsed_ms,
                        3,
                    )
                },
            )

        except Exception as ex:

            elapsed_ms = (
                time.perf_counter() - start
            ) * 1000.0

            pathway = CTFPathway(
                pathway_id=str(uuid.uuid4()),
                route_key=request.route_key,
                nodes=[
                    request.source,
                    "ctf",
                    request.route_key,
                ],
                failure_count=1,
                average_latency_ms=round(
                    elapsed_ms,
                    3,
                ),
            )

            self.registry.register_pathway(pathway)

            return CTFRouteResult(
                request_id=request.request_id,
                route_key=request.route_key,
                destination=request.route_key,
                status=CTFRouteStatus.FAILED,
                error=str(ex),
                pathway_id=pathway.pathway_id,
                metadata={
                    "latency_ms": round(
                        elapsed_ms,
                        3,
                    )
                },
            )

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def available_routes(self):

        return self.registry.routes()

    def pathway_count(self):

        return len(self.registry.pathways())