from __future__ import annotations

from aletheus.sdk import Application


class DemoApplication(Application):
    APP_ID = "demo"
    NAME = "Demo Application"
    VERSION = "1.0.0"

    PERMISSIONS = [
        "runtime.read",
        "services.read",
    ]

    SERVICES = [
        "demo.status",
    ]

    DEPENDENCIES = [
        "aletheus.application_runtime",
        "aletheus.sdk",
    ]
