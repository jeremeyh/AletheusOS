from __future__ import annotations

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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Content-Type",
            "Authorization",
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

    @app.get("/api/auth/config")
    def authentication_metadata() -> dict:
        return {
            "mode": authentication_config.mode,
            "issuer": authentication_config.issuer,
            "audience": authentication_config.audience,
            "algorithms": list(
                authentication_config.algorithms
            ),
            "localIdentityAllowed": (
                authentication_config
                .allow_local_identity
            ),
        }

    @app.get("/api/identity/me")
    def current_identity(
        principal: Principal = Depends(
            principal_resolver.dependency
        ),
    ) -> dict:
        return {
            "subjectId": principal.subject_id,
            "displayName": principal.display_name,
            "roles": list(principal.roles),
            "entitlements": list(
                principal.entitlements
            ),
            "authenticationMethod": (
                principal.authentication_method
            ),
            "authenticated": (
                principal.authenticated
            ),
        }

    @app.get("/api/commands")
    def list_commands() -> list[dict]:
        return command_gateway.list_commands()

    @app.post("/api/commands/preview")
    def preview_command(
        payload: CommandPreviewRequestModel,
        principal: Principal = Depends(
            principal_resolver.dependency
        ),
    ) -> dict:
        try:
            preview = command_gateway.preview(
                CommandRequest(
                    command_id=payload.command_id,
                    arguments=payload.arguments,
                    requested_by=principal.subject_id,
                    idempotency_key=(
                        payload.idempotency_key
                    ),
                ),
                principal=principal,
            )
        except KeyError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error),
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error),
            ) from error
        except PermissionError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error),
            ) from error

        return asdict(preview)

    @app.post("/api/commands/authorize")
    def authorize_command(
        payload: CommandAuthorizationRequestModel,
        principal: Principal = Depends(
            principal_resolver.dependency
        ),
    ) -> dict:
        try:
            authorization = (
                command_gateway.authorize(
                    preview_id=payload.preview_id,
                    authorized_by=(
                        principal.subject_id
                    ),
                )
            )
        except KeyError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error),
            ) from error
        except TimeoutError as error:
            raise HTTPException(
                status_code=410,
                detail=str(error),
            ) from error

        return asdict(authorization)

    @app.post("/api/commands/execute")
    def execute_command(
        payload: CommandExecutionRequestModel,
    ) -> dict:
        try:
            execution = command_gateway.execute(
                preview_id=payload.preview_id,
                authorization_id=(
                    payload.authorization_id
                ),
                idempotency_key=(
                    payload.idempotency_key
                ),
            )
        except KeyError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error),
            ) from error
        except PermissionError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error),
            ) from error
        except TimeoutError as error:
            raise HTTPException(
                status_code=410,
                detail=str(error),
            ) from error

        return asdict(execution)

    @app.post("/api/commands/reverse")
    def reverse_command(
        payload: CommandReversalRequestModel,
    ) -> dict:
        try:
            execution = command_gateway.reverse(
                execution_id=(
                    payload.execution_id
                ),
                reversal_token=(
                    payload.reversal_token
                ),
            )
        except KeyError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error),
            ) from error
        except PermissionError as error:
            raise HTTPException(
                status_code=403,
                detail=str(error),
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=409,
                detail=str(error),
            ) from error

        return asdict(execution)

    @app.get("/api/commands/history")
    def command_history() -> list[dict]:
        return [
            asdict(execution)
            for execution in (
                command_gateway.history()
            )
        ]

    @app.get("/api/commands/persistence")
    def command_persistence() -> dict:
        return {
            "mode": "sqlite",
            "databasePath": str(
                command_store.database_path
            ),
            "counts": command_store.counts(),
            "durable": True,
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
