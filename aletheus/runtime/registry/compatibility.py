from __future__ import annotations


class RegistryCompatibility:
    CURRENT_VERSION = "2.0.0"

    def validate(self, registry):

        snapshot = registry.snapshot()

        version = snapshot.get("version")

        compatible = version == self.CURRENT_VERSION

        return {
            "compatible": compatible,
            "current_version": self.CURRENT_VERSION,
            "registry_version": version,
            "snapshot": snapshot,
        }

    def migrate(self, registry):

        return {
            "migrated": False,
            "message": "No migration required",
            "version": self.CURRENT_VERSION,
        }
