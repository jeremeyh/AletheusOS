from __future__ import annotations

from typing import Any


class Application:
    """
    AletheusOS SDK Application Base™

    All native AletheusOS applications should inherit from this class.
    """

    APP_ID = "application"
    NAME = "Aletheus Application"
    VERSION = "0.1.0"
    SDK_VERSION = "12.0"

    PERMISSIONS: list[str] = []
    SERVICES: list[str] = []
    DEPENDENCIES: list[str] = []

    def startup(self) -> bool:
        return True

    def shutdown(self) -> bool:
        return True

    def health(self) -> dict[str, Any]:
        return {
            "app_id": self.APP_ID,
            "name": self.NAME,
            "version": self.VERSION,
            "status": "online",
        }

    def statistics(self) -> dict[str, Any]:
        return {
            "app_id": self.APP_ID,
            "version": self.VERSION,
        }

    def manifest(self) -> dict[str, Any]:
        return {
            "id": self.APP_ID,
            "name": self.NAME,
            "version": self.VERSION,
            "sdk": self.SDK_VERSION,
            "permissions": self.PERMISSIONS,
            "services": self.SERVICES,
            "dependencies": self.DEPENDENCIES,
        }

    def permissions(self) -> list[str]:
        return list(self.PERMISSIONS)

    def services(self) -> list[str]:
        return list(self.SERVICES)

    def dependencies(self) -> list[str]:
        return list(self.DEPENDENCIES)
