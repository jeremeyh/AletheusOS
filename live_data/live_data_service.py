from live_data.comps.comp_engine import CompEngine
from live_data.providers.demo_provider import DemoLiveProvider
from live_data.watchlist.live_watchlist import LiveWatchlist


class LiveDataService:
    """CardHawk OS™ 8.0 — Live Data Activation."""

    def __init__(self, providers=None):
        self.providers = providers or [DemoLiveProvider()]

    def search(self, query, limit=25):
        listings = []
        for provider in self.providers:
            try:
                listings.extend(provider.search(query, limit))
            except Exception:
                continue
        return listings

    def comps(self, query):
        listings = self.search(query)
        return CompEngine.build(query, listings)

    def add_watch(self, query, max_price=0, min_score=0):
        return LiveWatchlist.add(query, max_price, min_score)

    def watchlist(self):
        return LiveWatchlist.all()

    def scan_watchlist(self):
        results = {}
        for target in LiveWatchlist.active():
            results[target.query] = self.comps(target.query)
        return results
