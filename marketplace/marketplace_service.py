class MarketplaceService:
    """Coordinates marketplace connectors."""

    def __init__(self, connectors=None):
        self.connectors = connectors or []

    def scan(self, query):
        results = []
        for c in self.connectors:
            try:
                results.extend(c.search(query))
            except Exception:
                pass
        return results
