from __future__ import annotations

from typing import Any, Dict, List

from aletheus.applications.models import ApplicationManifest, NativeApplication


class AletheusApplicationManager:
    def __init__(self) -> None:
        self.version = "2.0.0-beta"
        self.applications: List[NativeApplication] = []

    def install_application(
        self,
        app_id: str,
        name: str,
        version: str = "1.0.0",
        author: str = "6th Dimension Multimedia",
        description: str = "",
        autostart: bool = False,
        permissions: List[str] | None = None,
        dependencies: List[str] | None = None,
        commands: List[str] | None = None,
        services: List[str] | None = None,
    ) -> NativeApplication:
        existing = self.get_application(app_id=app_id, name=name)
        if existing:
            return existing

        manifest = ApplicationManifest(
            app_id=app_id,
            name=name,
            version=version,
            author=author,
            description=description,
            autostart=autostart,
            permissions=permissions or [],
            dependencies=dependencies or [],
            commands=commands or [],
            services=services or [],
        )

        app = NativeApplication(manifest=manifest)
        app.emit("application.installed", f"{name} installed.", {"manifest": manifest.to_dict()})
        self.applications.append(app)

        if autostart:
            app.start()

        return app

    def register_application(
        self,
        name: str,
        version: str,
        description: str = "",
        services: List[Dict[str, Any]] | None = None,
        dependencies: List[str] | None = None,
        commands: List[str] | None = None,
    ) -> NativeApplication:
        app_id = name.lower().replace("™", "").replace("•", "").replace(" ", ".")
        service_names = [item.get("name", "Unnamed Service") for item in (services or [])]

        return self.install_application(
            app_id=app_id,
            name=name,
            version=version,
            description=description,
            services=service_names,
            dependencies=dependencies or [],
            commands=commands or [],
            permissions=["memory", "knowledge", "prediction", "learning", "planning"],
            autostart=False,
        )

    def register_card_hawk_foundation(self) -> NativeApplication:
        return self.install_application(
            app_id="cardhawk.foundation",
            name="Card Hawk Foundation™",
            version="2.0.0-beta",
            description="Flagship native AletheusOS reference application.",
            autostart=True,
            permissions=[
                "memory",
                "knowledge",
                "semantic",
                "planning",
                "prediction",
                "learning",
                "optimization",
                "agents",
                "kernel",
            ],
            dependencies=[
                "Aletheus Runtime Core",
                "Aletheus v2 Autonomous Kernel",
                "Aletheus Memory Core",
                "Aletheus Knowledge Graph Engine",
                "Aletheus Predictive Intelligence Layer",
                "Aletheus Adaptive Learning Engine",
            ],
            commands=[
                "cardhawk.status",
                "cardhawk.start",
                "cardhawk.stop",
                "cardhawk.foundation.bootstrap",
            ],
            services=[
                "Asset Vault",
                "Portfolio Engine",
                "Marketplace Intelligence",
                "Hawk A•Eye™",
                "THORᵡ",
                "DEF",
                "FALCON™",
                "NEST™",
            ],
        )

    def install_default_applications(self) -> List[Dict[str, Any]]:
        apps = [
            self.register_card_hawk_foundation(),
            self.install_application(
                app_id="cardhawk.asset_vault",
                name="Asset Vault",
                version="2.0.0-beta",
                description="Native collectible asset registry.",
                autostart=True,
                permissions=["memory", "knowledge", "storage", "kernel"],
                dependencies=["Card Hawk Foundation™"],
                commands=["asset.create", "asset.read", "asset.update", "asset.delete", "asset.search"],
                services=["Asset CRUD", "Asset Search", "Asset Uploads"],
            ),
            self.install_application(
                app_id="cardhawk.portfolio",
                name="Portfolio Engine",
                version="2.0.0-beta",
                description="Native portfolio valuation and allocation engine.",
                autostart=True,
                permissions=["memory", "knowledge", "prediction", "learning"],
                dependencies=["Asset Vault"],
                commands=["portfolio.refresh", "portfolio.value", "portfolio.allocation"],
                services=["Valuation", "Allocation", "Gain/Loss"],
            ),
            self.install_application(
                app_id="cardhawk.marketplace",
                name="Marketplace Intelligence",
                version="2.0.0-beta",
                description="Native marketplace signal and comps intelligence.",
                autostart=True,
                permissions=["memory", "knowledge", "prediction", "learning", "agents"],
                dependencies=["Asset Vault", "Portfolio Engine"],
                commands=["market.search", "market.comps", "market.alerts"],
                services=["Comps", "Alerts", "Opportunity Detection"],
            ),
            self.install_application(
                app_id="cardhawk.thorx",
                name="THORᵡ",
                version="2.0.0-beta",
                description="Trading Heuristic Opportunity Rating engine.",
                autostart=True,
                permissions=["prediction", "learning", "optimization"],
                dependencies=["Marketplace Intelligence"],
                commands=["thorx.score", "thorx.evaluate"],
                services=["Opportunity Rating", "Heuristic Scoring"],
            ),
            self.install_application(
                app_id="cardhawk.hawk_aeye",
                name="Hawk A•Eye™",
                version="2.0.0-beta",
                description="Native visual intelligence engine.",
                autostart=True,
                permissions=["memory", "knowledge", "storage"],
                dependencies=["Asset Vault"],
                commands=["aeye.scan", "aeye.identify"],
                services=["Image Recognition", "Visual Matching"],
            ),
        ]

        return [app.to_dict() for app in apps]

    def uninstall_application(self, app_id: str = "", name: str = "") -> Dict[str, Any]:
        app = self.get_application(app_id=app_id, name=name)
        if app is None:
            return {"error": "Application not found."}

        app.emit("application.uninstalled", f"{app.name} uninstalled.")
        self.applications = [item for item in self.applications if item.application_id != app.application_id]
        return app.to_dict()

    def get_application(self, app_id: str = "", application_id: str = "", name: str = "") -> NativeApplication | None:
        lookup_id = app_id or application_id
        for app in self.applications:
            if lookup_id and app.application_id == lookup_id:
                return app
            if name and app.name == name:
                return app
        return None

    def list_applications(self) -> List[Dict[str, Any]]:
        return [app.to_dict() for app in self.applications]

    def start_application(self, app_id: str = "", application_id: str = "", name: str = "") -> Dict[str, Any]:
        app = self.get_application(app_id=app_id, application_id=application_id, name=name)
        if app is None:
            return {"error": "Application not found."}
        app.start()
        return app.to_dict()

    def stop_application(self, app_id: str = "", application_id: str = "", name: str = "") -> Dict[str, Any]:
        app = self.get_application(app_id=app_id, application_id=application_id, name=name)
        if app is None:
            return {"error": "Application not found."}
        app.stop()
        return app.to_dict()

    def restart_application(self, app_id: str = "", application_id: str = "", name: str = "") -> Dict[str, Any]:
        app = self.get_application(app_id=app_id, application_id=application_id, name=name)
        if app is None:
            return {"error": "Application not found."}
        app.restart()
        return app.to_dict()

    def health(self, app_id: str = "", application_id: str = "", name: str = "") -> Dict[str, Any]:
        app = self.get_application(app_id=app_id, application_id=application_id, name=name)
        if app is None:
            return {"error": "Application not found."}
        app.heartbeat()
        return {
            "application_id": app.application_id,
            "name": app.name,
            "version": app.version,
            "status": app.status,
            "health": app.health,
            "lifecycle": app.lifecycle,
            "services": app.manifest.services,
            "dependencies": app.dependencies,
            "commands": app.commands,
            "permissions": app.manifest.permissions,
            "last_heartbeat": app.last_heartbeat,
        }

    def manifest(self, app_id: str = "", application_id: str = "", name: str = "") -> Dict[str, Any]:
        app = self.get_application(app_id=app_id, application_id=application_id, name=name)
        if app is None:
            return {"error": "Application not found."}
        return app.manifest.to_dict()

    def events(self, app_id: str = "", application_id: str = "", name: str = "") -> List[Dict[str, Any]]:
        app = self.get_application(app_id=app_id, application_id=application_id, name=name)
        if app is None:
            return [{"error": "Application not found."}]
        return [event.to_dict() for event in app.events]

    def stats(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "applications": len(self.applications),
            "running": len([app for app in self.applications if app.status == "running"]),
            "installed": len([app for app in self.applications if app.status == "installed"]),
            "stopped": len([app for app in self.applications if app.status == "stopped"]),
            "healthy": len([app for app in self.applications if app.health == "healthy"]),
            "events": sum(len(app.events) for app in self.applications),
        }


application_core = AletheusApplicationManager()
