"""
Registry Manager

Genesis 7.2

Owns registry snapshots and inspection.
"""


class RegistryManager:
    def __init__(self, runtime):
        self.runtime = runtime

    def snapshot(self):

        return self.runtime.registry.snapshot()

    def healthy(self):

        return self.snapshot().get("healthy", False)
