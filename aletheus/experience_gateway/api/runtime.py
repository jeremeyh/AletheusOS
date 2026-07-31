"""Runtime HTTP routes for the AletheusOS Experience Gateway."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, Protocol

from ..service import ExperienceGatewayService


class RouteApplication(Protocol):
    """Minimum application contract required to install HTTP routes."""

    def get(
        self,
        path: str,
        **kwargs: Any,
    ) -> Any: ...


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def build_runtime_health() -> dict[str, Any]:
    """Build the Nimble-compatible live runtime health contract."""

    root = _repository_root()
    checks: list[dict[str, Any]] = []

    repository_ok = (root / "aletheus").is_dir() and (root / "tests").is_dir()

    checks.append(
        {
            "id": "repository-structure",
            "name": "Repository structure",
            "state": "passing" if repository_ok else "failing",
            "message": (
                "Required repository directories are present."
                if repository_ok
                else "Required repository directories are missing."
            ),
        }
    )

    try:
        runtime_module = importlib.import_module("aletheus.runtime")
        runtime_ok = hasattr(runtime_module, "runtime_core")
    except Exception:
        runtime_ok = False

    checks.append(
        {
            "id": "runtime-import",
            "name": "Runtime import",
            "state": "passing" if runtime_ok else "failing",
            "message": (
                "Aletheus runtime imported successfully."
                if runtime_ok
                else "Aletheus runtime could not be imported."
            ),
        }
    )

    try:
        importlib.import_module("aletheus.experience_gateway")
        gateway_ok = True
    except Exception:
        gateway_ok = False

    checks.append(
        {
            "id": "experience-gateway-import",
            "name": "Experience Gateway import",
            "state": "passing" if gateway_ok else "failing",
            "message": (
                "Experience Gateway imported successfully."
                if gateway_ok
                else "Experience Gateway could not be imported."
            ),
        }
    )

    nimble_build_locations = (
        root / "nimble" / "dist",
        root / "apps" / "nimble" / "dist",
        root / "frontend" / "dist",
        root / "dist",
    )

    nimble_build_ok = any(path.exists() for path in nimble_build_locations)

    checks.append(
        {
            "id": "nimble-production-build",
            "name": "Nimble production build",
            "state": "passing" if nimble_build_ok else "warning",
            "message": (
                "A Nimble production build was detected."
                if nimble_build_ok
                else (
                    "No Nimble production build was detected; "
                    "the runtime API remains available."
                )
            ),
        }
    )

    passing_checks = sum(check["state"] == "passing" for check in checks)
    warning_count = sum(check["state"] == "warning" for check in checks)
    failing_count = sum(check["state"] == "failing" for check in checks)

    if failing_count == 0:
        state = "healthy" if warning_count == 0 else "degraded"
    elif passing_checks > 0:
        state = "degraded"
    else:
        state = "unavailable"

    return {
        "state": state,
        "totalChecks": len(checks),
        "passingChecks": passing_checks,
        "warningCount": warning_count,
        "checks": checks,
        "truth": {
            "state": "live_runtime_provider",
            "source": "aletheus-experience-gateway",
        },
    }


def load_missions(
    gateway: ExperienceGatewayService,
) -> list[Any]:
    """Load missions through the gateway or return the canonical fallback."""

    for method_name in (
        "list_missions",
        "get_missions",
        "missions",
    ):
        method = getattr(gateway, method_name, None)

        if not callable(method):
            continue

        try:
            result = method()
        except TypeError:
            continue

        if isinstance(result, list) and result:
            return result

        if isinstance(result, dict):
            missions = result.get("missions")

            if isinstance(missions, list) and missions:
                return missions

    return [
        {
            "id": "genesis-9",
            "name": "Platform Intelligence Fabric",
            "state": "active",
            "objective": (
                "Connect AletheusOS through constitutional platform intelligence."
            ),
        }
    ]


def install_runtime_routes(
    app: RouteApplication,
    gateway: ExperienceGatewayService,
) -> None:
    """
    Install runtime routes directly onto the application.

    Direct registration avoids the FastAPI 0.139 included-router candidate
    cache while preserving the bounded API module boundary.
    """

    @app.get(
        "/api/runtime/health",
        tags=["runtime"],
    )
    async def runtime_health() -> dict[str, Any]:
        return build_runtime_health()

    @app.get(
        "/api/runtime/overview",
        tags=["runtime"],
    )
    async def runtime_overview() -> dict[str, Any]:
        return {
            "health": build_runtime_health(),
            "missions": load_missions(gateway),
        }
