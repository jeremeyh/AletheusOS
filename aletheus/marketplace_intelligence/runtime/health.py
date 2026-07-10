"""
Connector Health Monitoring

Genesis 13.24
"""


class ConnectorHealthManager:


    def inspect(
        self,
        connector
    ):

        return connector.health()

