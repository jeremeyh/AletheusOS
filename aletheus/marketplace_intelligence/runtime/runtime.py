"""
Marketplace Connector Runtime

Genesis 13.24
"""


from .health import ConnectorHealthManager
from .lifecycle import ConnectorLifecycleManager
from .registry import ConnectorRegistry


class MarketplaceConnectorRuntime:


    def __init__(
        self
    ):

        self.registry = (
            ConnectorRegistry()
        )

        self.lifecycle = (
            ConnectorLifecycleManager()
        )

        self.health = (
            ConnectorHealthManager()
        )



    def register(
        self,
        connector
    ):

        self.registry.register(
            connector
        )

        return connector



    def status(
        self
    ):

        return [

            self.health.inspect(
                self.registry.get(name)
            )

            for name

            in self.registry.list()

        ]

