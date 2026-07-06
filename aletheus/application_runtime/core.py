from __future__ import annotations

from typing import Any

from aletheus.contracts import PlatformComponentContract

from .loader import application_loader


class ApplicationRuntime(PlatformComponentContract):
    """
    AletheusOS Application Runtime™

    Public runtime interface for installing and managing
    SDK applications.
    """

    GENESIS = "14.0"
    VERSION = "0.2.0"

    def __init__(self):
        self.status_value = "online"

    def boot(self):
        self.status_value = "online"
        return self.health()

    def shutdown(self):
        self.status_value = "offline"
        return self.health()

    def install(self, app: Any):
        return application_loader.install(app)

    def uninstall(self, app_id: str):
        return application_loader.uninstall(app_id)

    def start(self, app_id: str):
        return application_loader.start(app_id)

    def stop(self, app_id: str):
        return application_loader.stop(app_id)

    def restart(self, app_id: str):
        return application_loader.restart(app_id)

    def list(self):
        return application_loader.list()

    def health(self):
        loader_health = application_loader.health()

        return {
            "name": "Application Runtime",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": self.status_value,
            "loader": loader_health,
        }

    def statistics(self):
        loader_stats = application_loader.statistics()

        return {
            "name": "Application Runtime",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "applications": loader_stats.get("applications", 0),
            "installed": loader_stats.get("installed", []),
        }


application_runtime = ApplicationRuntime()
