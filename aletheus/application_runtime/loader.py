from __future__ import annotations

from typing import Dict, List

from aletheus.sdk import Application


class ApplicationLoader:
    """
    AletheusOS Application Loader™

    Responsible for loading, starting, stopping,
    and unloading SDK applications.
    """

    GENESIS = "13.0"
    VERSION = "0.1.0"

    def __init__(self):
        self._applications: Dict[str, Application] = {}

    def install(self, app: Application):
        self._applications[app.APP_ID] = app
        return app.manifest()

    def uninstall(self, app_id: str):
        return self._applications.pop(app_id, None)

    def start(self, app_id: str):
        app = self._applications[app_id]
        app.startup()
        return app.health()

    def stop(self, app_id: str):
        app = self._applications[app_id]
        app.shutdown()
        return app.health()

    def restart(self, app_id: str):
        self.stop(app_id)
        return self.start(app_id)

    def get(self, app_id: str):
        return self._applications.get(app_id)

    def list(self) -> List[dict]:
        return [app.manifest() for app in self._applications.values()]

    def health(self):
        return {
            "name": "Application Loader",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "applications": len(self._applications),
        }

    def statistics(self):
        return {
            "applications": len(self._applications),
            "installed": sorted(self._applications.keys()),
        }


application_loader = ApplicationLoader()
