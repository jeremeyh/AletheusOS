from __future__ import annotations

from datetime import UTC, datetime


class ApplicationRuntime:
    def __init__(self):

        self.applications = {}

    def register(
        self,
        name,
        version="1.0.0",
        description="",
        services=None,
    ):

        app = {
            "name": name,
            "version": version,
            "description": description,
            "services": services or [],
            "state": "registered",
            "created": datetime.now(UTC).isoformat(),
        }

        self.applications[name] = app

        return app

    def install(self, name):

        app = self.applications.get(name)

        if not app:
            return {"error": "application_not_found"}

        app["state"] = "installed"

        return app

    def start(self, name):

        app = self.applications.get(name)

        if not app:
            return {"error": "application_not_found"}

        app["state"] = "running"

        return app

    def stop(self, name):

        app = self.applications.get(name)

        if not app:
            return {"error": "application_not_found"}

        app["state"] = "stopped"

        return app

    def restart(self, name):

        self.stop(name)

        return self.start(name)

    def health(self):

        return {
            "applications": len(self.applications),
            "running": [
                name
                for name, app in self.applications.items()
                if app["state"] == "running"
            ],
        }

    def manifest(self, name):

        return self.applications.get(name, {"error": "application_not_found"})


application_runtime = ApplicationRuntime()
