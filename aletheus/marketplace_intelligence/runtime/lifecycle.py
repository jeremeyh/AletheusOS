"""
Connector Lifecycle Manager

Genesis 13.24
"""


class ConnectorLifecycleManager:
    def start(self, connector):

        connector.status = "active"

        return connector

    def stop(self, connector):

        connector.status = "disabled"

        return connector
