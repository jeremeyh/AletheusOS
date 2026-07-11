from __future__ import annotations

import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import asdict

from fastapi import Depends, HTTPException

from .command_api_models import (
    CommandAuthorizationRequestModel,
    CommandExecutionRequestModel,
    CommandPreviewRequestModel,
    CommandReversalRequestModel,
)
from .commands.contracts import CommandRequest
from .commands.default_commands import (
    create_default_command_registry,
)
from .commands.config import (
    command_database_path,
)
from .commands.service import (
    CommandGatewayService,
)
from .commands.sqlite_store import (
    SQLiteCommandAuditStore,
)

from .providers import create_default_provider_registry
from .security import (
    Principal,
    PrincipalResolver,
    create_default_authorization_policy,
    create_principal_authenticator,
    load_authentication_config,
)
from .service import ExperienceGatewayService


def evaluate_readiness(
    environment: dict[str, str] | None = None,
) -> dict[str, object]:
    """Evaluate deployment configuration without constructing the app."""
    values = environment if environment is not None else os.environ

    auth_mode = values.get(
        "ALETHEUS_AUTH_MODE",
        "local",
    ).strip().lower()

    checks: dict[str, bool] = {
        "auth_mode_supported": auth_mode
        in {"local", "oidc"},
    }

    if auth_mode == "oidc":
        required_oidc = (
            "ALETHEUS_OIDC_ISSUER",
            "ALETHEUS_OIDC_AUDIENCE",
            "ALETHEUS_OIDC_JWKS_URL",
        )

        checks["oidc_configuration_present"] = all(
            bool(values.get(name))
            for name in required_oidc
        )

    ready = all(checks.values())

    return {
        "status": "ready" if ready else "not_ready",
        "service": "nimble-experience-gateway",
        "auth_mode": auth_mode,
        "checks": checks,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }



def create_app(
    service: ExperienceGatewayService | None = None,
    command_service: CommandGatewayService | None = None,
) -> FastAPI:
    gateway = service or ExperienceGatewayService(
        provider_registry=(
            create_default_provider_registry()
        )
    )

    command_store = SQLiteCommandAuditStore(
        command_database_path()
    )

    authentication_config = (
        load_authentication_config()
    )

    principal_authenticator = (
        create_principal_authenticator(
            authentication_config
        )
    )

    principal_resolver = PrincipalResolver(
        principal_authenticator
    )

    command_gateway = (
        command_service
        or CommandGatewayService(
            create_default_command_registry(),
            store=command_store,
            authorization_policy=(
                create_default_authorization_policy()
            ),
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

    @app.get(
        "/healthz",
        tags=["platform"],
        summary="Process liveness probe",
    )
    async def healthz() -> dict[str, object]:
        """Report whether the Experience Gateway process is alive."""
        return {
            "status": "alive",
            "service": "nimble-experience-gateway",
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }

    @app.get(
        "/readyz",
        tags=["platform"],
        summary="Deployment readiness probe",
    )
    async def readyz() -> dict[str, object]:
        """Report whether required runtime configuration is valid."""
        return evaluate_readiness()





    return app

app = create_app()
