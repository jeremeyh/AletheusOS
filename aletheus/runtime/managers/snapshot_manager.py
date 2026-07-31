"""
Snapshot Manager

Genesis 7.5

Owns runtime snapshots.
"""


class SnapshotManager:
    def __init__(self, runtime):
        self.runtime = runtime

    def snapshot(self):

        return {
            "runtime": self.runtime.version,
            "commands": self.runtime.commands.count(),
            "registry": self.runtime.registry.snapshot(),
        }
