"""Platform-service resolution for hosted applications."""

from __future__ import annotations

from typing import Any


class MissingApplicationServiceError(KeyError):
    pass


class ApplicationServiceResolver:
    """
    Resolve stable Platform Surface services for hosted applications.

    Applications receive public surfaces, never internal engines.
    """

    SERVICE_NAMES = {
        "runtime",
        "security",
        "cases",
        "missions",
        "ledger",
        "cognition",
        "instrumentation",
        "scenarios",
    }

    def __init__(
        self,
        *,
        platform,
    ) -> None:
        self.platform = platform

    def available(self) -> tuple[str, ...]:
        return tuple(
            sorted(name for name in self.SERVICE_NAMES if hasattr(self.platform, name))
        )

    def resolve(
        self,
        service_name: str,
    ) -> Any:
        if service_name not in self.SERVICE_NAMES:
            raise MissingApplicationServiceError(
                f"Unknown platform service: {service_name!r}."
            )

        if not hasattr(
            self.platform,
            service_name,
        ):
            raise MissingApplicationServiceError(
                f"Platform service {service_name!r} is unavailable."
            )

        return getattr(
            self.platform,
            service_name,
        )

    def resolve_many(
        self,
        service_names: tuple[str, ...],
    ) -> dict[str, Any]:
        return {
            service_name: self.resolve(service_name) for service_name in service_names
        }
