"""
AletheusOS Application Runtime Registry

Canonical registry for applications available to the AletheusOS
application runtime.
"""

from __future__ import annotations

from typing import Any

from aletheus.card_hawk.runtime import CardHawkApplication


APPLICATIONS: dict[str, Any] = {
    "cardhawk": CardHawkApplication(),
}


def register_application(
    name: str,
    application: Any,
    *,
    replace: bool = False,
) -> Any:
    """
    Register an application with the application runtime.

    Existing registrations are protected unless ``replace`` is enabled.
    """

    normalized_name = name.strip().lower()

    if not normalized_name:
        raise ValueError("Application name cannot be empty.")

    if normalized_name in APPLICATIONS and not replace:
        raise ValueError(
            f"Application already registered: {normalized_name}"
        )

    APPLICATIONS[normalized_name] = application
    return application


def get_application(name: str) -> Any:
    """
    Return a registered application by name.
    """

    normalized_name = name.strip().lower()

    try:
        return APPLICATIONS[normalized_name]
    except KeyError as exc:
        raise KeyError(
            f"Application is not registered: {normalized_name}"
        ) from exc


def has_application(name: str) -> bool:
    """
    Return whether an application is registered.
    """

    return name.strip().lower() in APPLICATIONS


def list_applications() -> list[str]:
    """
    Return registered application names.
    """

    return sorted(APPLICATIONS)


__all__ = [
    "APPLICATIONS",
    "get_application",
    "has_application",
    "list_applications",
    "register_application",
]
