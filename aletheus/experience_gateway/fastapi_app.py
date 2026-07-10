from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .providers import create_default_provider_registry
from .service import ExperienceGatewayService


def create_app(
    service: ExperienceGatewayService | None = None,
) -> FastAPI:
    gateway = service or ExperienceGatewayService(
        provider_registry=(
            create_default_provider_registry()
        )
    )

    app = FastAPI(
        title="AletheusOS Experience Gateway",
        description=(
            "Bounded Principle X API for Nimble™ and "
            "AletheusOS applications."
        ),
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=False,
        allow_methods=["GET", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Content-Type",
        ],
    )

    @app.get("/api/runtime/health")
    def runtime_health() -> dict:
        response = gateway.health()

        # Nimble's current query contract expects the data
        # object directly rather than the outer metadata envelope.
        return response.to_dict()["data"]

    @app.get("/api/missions")
    def runtime_missions() -> list:
        response = gateway.missions()
        return response.to_dict()["data"]

    @app.get("/api/runtime/overview")
    def runtime_overview() -> dict:
        response = gateway.overview()
        return response.to_dict()["data"]

    @app.get("/api/experience/providers")
    def experience_providers() -> dict:
        registry = gateway.provider_registry

        if registry is None:
            return {
                "healthProbes": [],
                "missionSources": [],
                "mode": "legacy_provider",
            }

        return {
            **registry.describe(),
            "mode": "provider_registry",
        }

    @app.get("/api/experience/meta")
    def experience_metadata() -> dict:
        response = gateway.overview()

        return {
            "name": "AletheusOS Experience Gateway",
            "version": response.schema_version,
            "principleX": True,
            "requestId": response.request_id,
            "generatedAt": response.generated_at,
        }

    return app


app = create_app()
