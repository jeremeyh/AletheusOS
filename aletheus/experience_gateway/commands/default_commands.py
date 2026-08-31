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


    # ---------------------------------------------------------------------
    # Admin Terminal bounded read-only runtime bindings
    #
    # Constitutional authority:
    # ADMIN_TERMINAL_UNIFIED_ADJUDICATION_PACKAGE_III_GATES_28_32
    #
    # These gateway definitions expose existing runtime command authority.
    # They do not create replacement runtime handlers, registries, buses,
    # services, APIs, or result protocols.
    # ---------------------------------------------------------------------

    def _admin_runtime_read_handler(command_id: str):
        def _handler(arguments):
            if arguments:
                raise ValueError(f"{command_id} does not accept gateway arguments")

            runtime = getattr(registry, "runtime", None)
            if runtime is None:
                raise RuntimeError("Admin Terminal runtime authority is unavailable")

            command_bus = getattr(runtime, "command_bus", None)
            if command_bus is None:
                raise RuntimeError("Admin Terminal runtime command bus is unavailable")

            execute = getattr(command_bus, "execute", None)
            if not callable(execute):
                raise RuntimeError("Admin Terminal runtime command execution authority is unavailable")

            return execute(command_id, {})

        return _handler

    registry.register(
        CommandDefinition(
            id='application.health',
            name='Application health',
            description='Return the current bounded application health observation.',
            risk="read_only",
            handler=_admin_runtime_read_handler('application.health'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded application health state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='cluster.status',
            name='Cluster status',
            description='Return the current bounded cluster status observation.',
            risk="read_only",
            handler=_admin_runtime_read_handler('cluster.status'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded cluster status', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='enterprise.list',
            name='List enterprises',
            description='Return the currently observable enterprise collection.',
            risk="read_only",
            handler=_admin_runtime_read_handler('enterprise.list'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded enterprise state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='executive.snapshot',
            name='Executive snapshot',
            description='Return the current bounded executive runtime snapshot.',
            risk="read_only",
            handler=_admin_runtime_read_handler('executive.snapshot'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded executive runtime state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='executive.status',
            name='Executive status',
            description='Return the current bounded executive runtime status.',
            risk="read_only",
            handler=_admin_runtime_read_handler('executive.status'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded executive runtime state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='executive.system_report',
            name='Executive system report',
            description='Return the current bounded executive system report.',
            risk="read_only",
            handler=_admin_runtime_read_handler('executive.system_report'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded executive system state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='kernel.snapshot',
            name='Kernel snapshot',
            description='Return the current bounded kernel snapshot.',
            risk="read_only",
            handler=_admin_runtime_read_handler('kernel.snapshot'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded kernel state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='registry.health',
            name='Registry health',
            description='Return the current bounded runtime registry health observation.',
            risk="read_only",
            handler=_admin_runtime_read_handler('registry.health'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded runtime registry state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='registry.snapshot',
            name='Registry snapshot',
            description='Return the current bounded runtime registry snapshot.',
            risk="read_only",
            handler=_admin_runtime_read_handler('registry.snapshot'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded runtime registry state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='telemetry.health',
            name='Telemetry health',
            description='Return the current bounded telemetry health observation.',
            risk="read_only",
            handler=_admin_runtime_read_handler('telemetry.health'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded telemetry state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='tenant.health',
            name='Tenant health',
            description='Return the current bounded tenant health observation.',
            risk="read_only",
            handler=_admin_runtime_read_handler('tenant.health'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded tenant state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    registry.register(
        CommandDefinition(
            id='tenant.list',
            name='List tenants',
            description='Return the currently observable tenant collection.',
            risk="read_only",
            handler=_admin_runtime_read_handler('tenant.list'),
            reversible=False,
            reversal_handler=None,
            required_arguments=(),
            effects=('Reads bounded tenant state', 'Does not mutate runtime state'),
            authorization_required=True,
            required_entitlements=("runtime.read",),
        )
    )

    return registry
