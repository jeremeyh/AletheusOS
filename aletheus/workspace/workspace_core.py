from __future__ import annotations

from typing import Any

from aletheus.workspace.models import (
    FounderJournalEntry,
    FounderNotification,
    StrategicObjective,
)


class AletheusFounderWorkspace:
    def __init__(self) -> None:
        self.version = "0.8.0-genesis"
        self.journal: list[FounderJournalEntry] = []
        self.objectives: list[StrategicObjective] = []
        self.notifications: list[FounderNotification] = []

    def create_journal_entry(
        self,
        title: str,
        body: str,
        category: str = "general",
        tags: list[str] | None = None,
    ) -> FounderJournalEntry:
        entry = FounderJournalEntry(
            title=title,
            body=body,
            category=category,
            tags=tags or [],
        )
        self.journal.append(entry)
        return entry

    def list_journal(self) -> list[dict[str, Any]]:
        return [entry.to_dict() for entry in self.journal]

    def create_objective(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        application: str = "system",
    ) -> StrategicObjective:
        objective = StrategicObjective(
            title=title,
            description=description,
            priority=priority,
            application=application,
        )
        self.objectives.append(objective)
        return objective

    def list_objectives(self, status: str | None = None) -> list[dict[str, Any]]:
        results = self.objectives
        if status:
            results = [item for item in results if item.status == status]
        return [item.to_dict() for item in results]

    def create_notification(
        self,
        title: str,
        message: str,
        severity: str = "info",
        source: str = "aletheus",
    ) -> FounderNotification:
        notification = FounderNotification(
            title=title,
            message=message,
            severity=severity,
            source=source,
        )
        self.notifications.append(notification)
        return notification

    def list_notifications(self, unread_only: bool = False) -> list[dict[str, Any]]:
        results = self.notifications
        if unread_only:
            results = [item for item in results if not item.read]
        return [item.to_dict() for item in results]

    def overview(self, runtime: Any) -> dict[str, Any]:
        health = runtime.commands.dispatch("runtime.health").results.get("health", {})
        diagnostics = runtime.commands.dispatch("runtime.diagnostics").results

        return {
            "workspace_version": self.version,
            "runtime": health,
            "memory": diagnostics.get("memory", {}),
            "cognition": diagnostics.get("cognition", {}),
            "knowledge": diagnostics.get("knowledge", {}),
            "mission": diagnostics.get("mission", {}),
            "objectives": len(self.objectives),
            "active_objectives": len([item for item in self.objectives if item.status == "active"]),
            "journal_entries": len(self.journal),
            "notifications": len(self.notifications),
            "unread_notifications": len([item for item in self.notifications if not item.read]),
        }

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "objectives": len(self.objectives),
            "active_objectives": len([item for item in self.objectives if item.status == "active"]),
            "journal_entries": len(self.journal),
            "notifications": len(self.notifications),
            "unread_notifications": len([item for item in self.notifications if not item.read]),
        }


workspace_core = AletheusFounderWorkspace()
