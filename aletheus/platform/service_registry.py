from __future__ import annotations

from datetime import datetime, timezone


class ServiceRegistry:

    def __init__(self):

        self.services = {}


    def register(
        self,
        name,
        version="1.0.0",
        domain="core",
        status="active",
        metadata=None,
    ):

        self.services[name] = {
            "name": name,
            "version": version,
            "domain": domain,
            "status": status,
            "metadata": metadata or {},
            "registered":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

        return self.services[name]


    def get(self, name):

        return self.services.get(
            name,
            {
                "error":
                    "service_not_found"
            }
        )


    def list(self):

        return list(
            self.services.values()
        )


    def health(self):

        unhealthy = []

        for name, service in self.services.items():

            if service["status"] != "active":
                unhealthy.append(name)


        return {
            "healthy":
                len(unhealthy) == 0,

            "services":
                len(self.services),

            "unhealthy":
                unhealthy,
        }


service_registry = ServiceRegistry()
