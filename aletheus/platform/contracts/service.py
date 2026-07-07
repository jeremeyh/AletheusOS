from abc import ABC


class PlatformService(ABC):
    """
    Platform Service™

    Canonical interface implemented by first-class AletheusOS
    platform services.
    """

    def initialize(self):
        """Initialize the service."""
        return None

    def health(self):
        """Return service health."""
        return {
            "status": "online",
        }

    def metrics(self):
        """Return service metrics."""
        return {}

    def snapshot(self):
        """Return current service snapshot."""
        return {}

    def shutdown(self):
        """Gracefully stop the service."""
        return None
