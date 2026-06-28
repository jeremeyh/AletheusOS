from providers.base_provider import BaseProvider, RawListing


class MercariLive(BaseProvider):
    """Mercari provider adapter.

    Alpha 2.0 implementation is provider-ready: the method contract is stable,
    while authenticated live API calls can be added when credentials and terms allow.
    """

    NAME = "Mercari"

    def search(self, query: str, limit: int = 25) -> list[RawListing]:
        # Live connector hook:
        # 1. Authenticate to Mercari
        # 2. Execute search/query
        # 3. Return RawListing objects
        # For now, return provider-shaped demo rows so the workflow is testable.
        return [
            RawListing(
                title=f"{query} — Mercari Candidate",
                price=0.0,
                marketplace=self.NAME,
                seller="demo",
                url="",
                raw={"provider": self.NAME, "query": query, "live_ready": True},
            )
        ][:limit]
