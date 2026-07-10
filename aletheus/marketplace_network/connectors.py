"""
Marketplace Connector Registry

Genesis 13.41
"""


class MarketplaceConnectorRegistry:


    def __init__(self):

        self.connectors = {}



    def register(
        self,
        connector
    ):

        self.connectors[
            connector.name
        ] = connector



    def list(
        self
    ):

        return list(
            self.connectors.keys()
        )

