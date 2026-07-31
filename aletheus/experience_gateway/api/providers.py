"""Provider registry HTTP routes for the Experience Gateway."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Protocol

from ..providers import create_default_provider_registry
from ..service import ExperienceGatewayService


class RouteApplication(Protocol):
    """Minimum application contract required to install GET routes."""

    def get(
        self,
        path: str,
        **kwargs: Any,
    ) -> Any: ...


def _serialize(value: Any) -> Any:
    """Convert provider registry values into JSON-compatible data."""

    if value is None:
        return None

    if isinstance(value, Enum):
        return value.value

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, Mapping):
        return {str(key): _serialize(item) for key, item in value.items()}

    if isinstance(value, (list, tuple, set, frozenset)):
        return [_serialize(item) for item in value]

    if is_dataclass(value):
        return _serialize(asdict(value))

    for method_name in (
        "model_dump",
        "to_dict",
        "to_snapshot",
        "snapshot",
    ):
        method = getattr(value, method_name, None)

        if callable(method):
            try:
                return _serialize(method())
            except TypeError:
                continue

    if hasattr(value, "__dict__"):
        return {
            key: _serialize(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }

    return str(value)


def _resolve_registry(
    gateway: ExperienceGatewayService,
) -> Any:
    for attribute_name in (
        "provider_registry",
        "_provider_registry",
        "providers",
        "_providers",
    ):
        registry = getattr(
            gateway,
            attribute_name,
            None,
        )

        if registry is not None:
            return registry

    return create_default_provider_registry()


def build_provider_registry_payload(
    gateway: ExperienceGatewayService,
) -> dict[str, Any]:
    """Describe provider sources without exposing private implementation."""

    registry = _resolve_registry(gateway)

    result: Any = None

    for method_name in (
        "describe",
        "statistics",
        "snapshot",
        "list_providers",
        "providers",
        "all",
    ):
        method = getattr(registry, method_name, None)

        if not callable(method):
            continue

        try:
            result = method()
            break
        except TypeError:
            continue

    if result is None:
        for attribute_name in (
            "_providers",
            "providers",
            "_probes",
            "probes",
        ):
            candidate = getattr(
                registry,
                attribute_name,
                None,
            )

            if candidate is not None:
                result = candidate
                break

    payload: dict[str, Any] = {
        "mode": "provider_registry",
        "truth": {
            "state": "live_provider_registry",
        },
    }

    serialized = _serialize(result)

    if serialized is not None:
        payload["providers"] = serialized
    else:
        payload["providers"] = []

    return payload


def install_provider_routes(
    app: RouteApplication,
    gateway: ExperienceGatewayService,
) -> None:
    """Install the bounded provider-disclosure API."""

    @app.get(
        "/api/experience/providers",
        tags=["experience"],
    )
    async def providers() -> dict[str, Any]:
        return build_provider_registry_payload(gateway)
