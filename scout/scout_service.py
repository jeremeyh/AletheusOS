from scout.market_scanner import MarketScanner
from scout.listing_queue import ListingQueue
from scout.candidate_filter import CandidateFilter
from scout.watchlist_manager import WatchlistManager
from scout.alert_manager import AlertManager


class ScoutService:
    """
    Scout™ 1.0

    Discovers marketplace listings, queues candidates, filters by watch targets,
    and raises alerts for founder review.
    """

    def __init__(self, connectors=None):
        self.scanner = MarketScanner(connectors=connectors)
        self.queue = ListingQueue()
        self.watchlist = WatchlistManager()
        self.alerts = AlertManager()

    def scan_query(self, query: str):
        candidates = self.scanner.scan(query)
        candidates = CandidateFilter.dedupe(candidates)
        self.queue.add_many(candidates)
        return candidates

    def scan_watchlist(self):
        all_matches = []
        for target in self.watchlist.all_targets():
            candidates = self.scan_query(target.query)
            matches = CandidateFilter.apply_watch_target(candidates, target)
            all_matches.extend(matches)
            for match in matches:
                self.alerts.create("Watchlist Match", match.title, "Info")
        return all_matches

    def submit_candidate(self, candidate):
        self.queue.add(candidate)
        return candidate
