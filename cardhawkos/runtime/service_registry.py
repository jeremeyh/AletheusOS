class ServiceRegistry:
    """
    CardHawkOS™

    Central registry for application services.

    Examples:

    • Database
    • Marketplace Manager
    • OCR Engine
    • Timeline
    • Event Bus
    • Configuration
    • Notification Center
    """

    _services = {}

    @classmethod
    def register(cls, name, service):
        cls._services[name] = service

    @classmethod
    def get(cls, name):
        return cls._services.get(name)

    @classmethod
    def names(cls):
        return sorted(cls._services.keys())

    @classmethod
    def count(cls):
        return len(cls._services)

    @classmethod
    def status(cls):

        results = []

        for name in sorted(cls._services):
            results.append(
                {
                    "service": name,
                    "loaded": True,
                }
            )

        return results
