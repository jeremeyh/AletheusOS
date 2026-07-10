"""
Founder Workspace Command Registration.

Binds workspace, objective, journal, and notification commands directly to
the bounded AletheusFounderWorkspace component.
"""

from __future__ import annotations

from typing import Any


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def register_workspace_commands(runtime):
    commands = runtime.commands
    workspace = runtime.workspace

    def overview(payload=None):
        return {
            "objectives": workspace.list_objectives(),
            "journal": workspace.list_journal(),
            "notifications": workspace.list_notifications(),
            "statistics": statistics(),
        }

    def statistics(payload=None):
        objectives = workspace.list_objectives()
        journal = workspace.list_journal()
        notifications = workspace.list_notifications()

        return {
            "objectives": len(objectives),
            "journal_entries": len(journal),
            "notifications": len(notifications),
            "unread_notifications": sum(
                1
                for notification in notifications
                if not notification.get("read", False)
            ),
            "status": "operational",
        }

    def create_journal(payload=None):
        payload = payload or {}

        entry = workspace.create_journal_entry(
            title=payload.get("title", "Untitled Entry"),
            body=payload.get("body", ""),
            category=payload.get("category", "general"),
            tags=payload.get("tags"),
        )

        return _serialize(entry)

    def list_journal(payload=None):
        return workspace.list_journal()

    def create_objective(payload=None):
        payload = payload or {}

        objective = workspace.create_objective(
            title=payload.get("title", "Untitled Objective"),
            description=payload.get("description", ""),
            priority=payload.get("priority", "medium"),
            application=payload.get("application", "system"),
        )

        return _serialize(objective)

    def list_objectives(payload=None):
        payload = payload or {}

        return workspace.list_objectives(
            status=payload.get("status"),
        )

    def create_notification(payload=None):
        payload = payload or {}

        notification = workspace.create_notification(
            title=payload.get("title", "Notification"),
            message=payload.get("message", ""),
            severity=payload.get("severity", "info"),
            source=payload.get("source", "aletheus"),
        )

        return _serialize(notification)

    def list_notifications(payload=None):
        payload = payload or {}

        return workspace.list_notifications(
            unread_only=payload.get("unread_only", False),
        )

    commands.register(
        "workspace.overview",
        overview,
        replace=True,
    )
    commands.register(
        "workspace.stats",
        statistics,
        replace=True,
    )
    commands.register(
        "founder.journal.create",
        create_journal,
        replace=True,
    )
    commands.register(
        "founder.journal.list",
        list_journal,
        replace=True,
    )
    commands.register(
        "objective.create",
        create_objective,
        replace=True,
    )
    commands.register(
        "objective.list",
        list_objectives,
        replace=True,
    )
    commands.register(
        "notification.create",
        create_notification,
        replace=True,
    )
    commands.register(
        "notification.list",
        list_notifications,
        replace=True,
    )
