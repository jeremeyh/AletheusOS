from .models import CapabilityManifest


class CapabilityManifestRegistry:
    def __init__(self):
        self.manifests = {}

    def register(self, manifest: CapabilityManifest):
        self.manifests[manifest.id] = manifest

    def all(self):
        return sorted(
            self.manifests.values(),
            key=lambda m: m.id,
        )

    def health(self):
        return {
            "status": "online",
            "capabilities": len(self.manifests),
        }
