from scout.listing_queue import ListingCandidate


class MarketScanner:
    """
    Scout™ market scanner.

    V1 accepts connectors that expose .search(query) and normalizes results.
    """

    def __init__(self, connectors=None):
        self.connectors = connectors or []

    def scan(self, query: str):
        candidates = []

        for connector in self.connectors:
            try:
                rows = connector.search(query)
            except Exception:
                rows = []

            for row in rows:
                candidates.append(
                    ListingCandidate(
                        title=row.get("title", ""),
                        price=float(row.get("price", 0) or 0),
                        marketplace=row.get(
                            "marketplace", getattr(connector, "NAME", "")
                        ),
                        url=row.get("url", ""),
                        seller=row.get("seller", ""),
                        raw=row,
                    )
                )

        return candidates
