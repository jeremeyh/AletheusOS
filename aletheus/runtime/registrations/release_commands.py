"""
Release Command Registration.

Binds the Genesis release manifest and runtime validation surface directly
to the bounded AletheusReleaseCore.
"""

from __future__ import annotations


def register_release_commands(runtime):
    commands = runtime.commands
    release = runtime.release

    def status(context):
        context.add_result(
            "release",
            release.status(),
        )
        return context

    def validate(context):
        context.add_result(
            "validation",
            release.validate_runtime(runtime),
        )
        return context

    commands.register(
        "release.status",
        status,
        replace=True,
    )

    commands.register(
        "release.validate",
        validate,
        replace=True,
    )
