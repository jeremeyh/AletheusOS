from __future__ import annotations

from typing import Any

from aletheus.time_utils import utc_now_iso

from .contracts import (
    CommandDefinition,
    CommandRegistry,
)

_shell_preferences: dict[str, Any] = {
    "inspectorOpen": True,
}


def _describe_runtime(
    arguments: dict[str, Any],
) -> dict[str, Any]:
    return {
        "summary": ("AletheusOS is available through bounded experience providers."),
        "scope": arguments.get(
            "scope",
            "platform",
        ),
        "generatedAt": utc_now_iso(),
        "mutated": False,
    }


def _set_inspector_state(
    arguments: dict[str, Any],
) -> dict[str, Any]:
    previous = bool(_shell_preferences["inspectorOpen"])

    next_value = bool(arguments["open"])

    _shell_preferences["inspectorOpen"] = next_value

    return {
        "previous": previous,
        "current": next_value,
        "mutated": True,
    }


def _reverse_inspector_state(
    context: dict[str, Any],
) -> dict[str, Any]:
    execution_result = context["executionResult"]

    previous = bool(execution_result["previous"])

    _shell_preferences["inspectorOpen"] = previous

    return {
        "restored": previous,
        "mutated": True,
    }


def _refresh_provider_state(
    arguments: dict[str, Any],
) -> dict[str, Any]:
    return {
        "refreshed": True,
        "scope": arguments.get(
            "scope",
            "all",
        ),
        "generatedAt": utc_now_iso(),
        "mutated": False,
    }


def create_default_command_registry() -> CommandRegistry:
    registry = CommandRegistry()

    registry.register(
        CommandDefinition(
            id="runtime.describe",
            name="Describe runtime state",
            description=("Return a bounded explanation of current runtime state."),
            risk="read_only",
            handler=_describe_runtime,
            reversible=False,
            required_arguments=(),
            effects=(
                "Reads bounded runtime status",
                "Does not mutate runtime state",
            ),
            authorization_required=False,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id="experience.inspector.set",
            name="Set truth inspector state",
            description=("Change the persisted Nimble truth inspector preference."),
            risk="low",
            handler=_set_inspector_state,
            reversible=True,
            reversal_handler=(_reverse_inspector_state),
            required_arguments=("open",),
            effects=(
                "Changes one experience preference",
                "Does not modify runtime services",
            ),
            authorization_required=True,
            required_entitlements=("experience.preferences.write",),
        )
    )

    registry.register(
        CommandDefinition(
            id="providers.refresh",
            name="Refresh provider state",
            description=("Request a fresh bounded provider observation."),
            risk="read_only",
            handler=_refresh_provider_state,
            reversible=False,
            required_arguments=(),
            effects=(
                "Refreshes provider observations",
                "Does not modify runtime state",
            ),
            authorization_required=False,
            required_entitlements=("providers.refresh",),
        )
    )

    return registry
