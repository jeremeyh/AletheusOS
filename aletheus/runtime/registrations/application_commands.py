"""
Native Application Command Registration.

Binds application lifecycle commands directly to the bounded
AletheusApplicationManager.
"""

from __future__ import annotations

from typing import Any


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def register_application_commands(runtime):
    commands = runtime.commands
    applications = runtime.applications

    def register(payload=None):
        payload = payload or {}

        application = applications.register_application(
            name=payload.get("name", "Untitled Application"),
            version=payload.get("version", "1.0.0"),
            description=payload.get("description", ""),
            services=payload.get("services"),
            dependencies=payload.get("dependencies"),
            commands=payload.get("commands"),
        )

        return _serialize(application)

    def list_applications(payload=None):
        return applications.list_applications()

    def start(payload=None):
        payload = payload or {}

        return applications.start_application(
            app_id=payload.get("app_id", ""),
            application_id=payload.get("application_id", ""),
            name=payload.get("name", ""),
        )

    def stop(payload=None):
        payload = payload or {}

        return applications.stop_application(
            app_id=payload.get("app_id", ""),
            application_id=payload.get("application_id", ""),
            name=payload.get("name", ""),
        )

    def restart(payload=None):
        payload = payload or {}

        return applications.restart_application(
            app_id=payload.get("app_id", ""),
            application_id=payload.get("application_id", ""),
            name=payload.get("name", ""),
        )

    def health(payload=None):
        payload = payload or {}

        return applications.health(
            app_id=payload.get("app_id", ""),
            application_id=payload.get("application_id", ""),
            name=payload.get("name", ""),
        )

    def statistics(payload=None):
        return applications.stats()

    def install(payload=None):
        payload = payload or {}

        application = applications.install_application(
            app_id=payload.get("app_id", ""),
            name=payload.get("name", "Untitled Application"),
            version=payload.get("version", "1.0.0"),
            author=payload.get(
                "author",
                "6th Dimension Multimedia",
            ),
            description=payload.get("description", ""),
            autostart=payload.get("autostart", False),
            permissions=payload.get("permissions"),
            dependencies=payload.get("dependencies"),
            commands=payload.get("commands"),
            services=payload.get("services"),
        )

        return _serialize(application)

    def uninstall(payload=None):
        payload = payload or {}

        return applications.uninstall_application(
            app_id=payload.get("app_id", ""),
            name=payload.get("name", ""),
        )

    def manifest(payload=None):
        payload = payload or {}

        return applications.manifest(
            app_id=payload.get("app_id", ""),
            application_id=payload.get("application_id", ""),
            name=payload.get("name", ""),
        )

    def events(payload=None):
        payload = payload or {}

        return applications.events(
            app_id=payload.get("app_id", ""),
            application_id=payload.get("application_id", ""),
            name=payload.get("name", ""),
        )

    def bootstrap_defaults(payload=None):
        return applications.install_default_applications()

    def cardhawk_start(payload=None):
        result = applications.start_application(
            app_id="cardhawk.foundation",
        )
        return result

    def cardhawk_status(payload=None):
        result = applications.health(
            app_id="cardhawk.foundation",
        )

        if isinstance(result, dict):
            result.setdefault("health", "healthy")

        return result

    commands.register(
        "application.register",
        register,
        replace=True,
    )
    commands.register(
        "application.list",
        list_applications,
        replace=True,
    )
    commands.register(
        "application.start",
        start,
        replace=True,
    )
    commands.register(
        "application.stop",
        stop,
        replace=True,
    )
    commands.register(
        "application.restart",
        restart,
        replace=True,
    )
    commands.register(
        "application.health",
        health,
        replace=True,
    )
    commands.register(
        "application.stats",
        statistics,
        replace=True,
    )
    commands.register(
        "application.install",
        install,
        replace=True,
    )
    commands.register(
        "application.uninstall",
        uninstall,
        replace=True,
    )
    commands.register(
        "application.manifest",
        manifest,
        replace=True,
    )
    commands.register(
        "application.events",
        events,
        replace=True,
    )
    commands.register(
        "application.bootstrap.defaults",
        bootstrap_defaults,
        replace=True,
    )
    commands.register(
        "cardhawk.start",
        cardhawk_start,
        replace=True,
    )
    commands.register(
        "cardhawk.status",
        cardhawk_status,
        replace=True,
    )
