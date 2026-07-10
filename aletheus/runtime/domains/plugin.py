class PluginDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.plugins_v3.bootstrap()

    def install(self, payload):
        return self.runtime.plugins_v3.install(**payload)

    def enable(self, payload):
        return self.runtime.plugins_v3.enable(
            payload.get("plugin_id", "")
        )

    def disable(self, payload):
        return self.runtime.plugins_v3.disable(
            payload.get("plugin_id", "")
        )

    def update(self, payload):
        return self.runtime.plugins_v3.update(
            payload.get("plugin_id", ""),
            payload.get("version"),
        )

    def remove(self, payload):
        return self.runtime.plugins_v3.remove(
            payload.get("plugin_id", "")
        )

    def list(self, payload=None):
        return self.runtime.plugins_v3.list()

    def status(self, payload=None):
        return self.runtime.plugins_v3.status()

    def statistics(self, payload=None):
        return self.runtime.plugins_v3.statistics()
