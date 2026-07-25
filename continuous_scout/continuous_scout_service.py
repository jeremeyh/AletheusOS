from continuous_scout.candidate_queue import CandidateQueue
from continuous_scout.scan_job import ScanJob
from marketplace_normalizer.listing_deduper import ListingDeduper
from marketplace_normalizer.normalizer import MarketplaceNormalizer


class ContinuousScoutService:
    """Continuous Scout™ runs provider scans and queues normalized candidates."""

    def __init__(self, providers=None):
        self.providers = providers or []
        self.jobs = []
        self.queue = CandidateQueue()

    def add_job(self, query, cadence="hourly"):
        job = ScanJob(query=query, cadence=cadence)
        self.jobs.append(job)
        return job

    def run_job(self, job):
        raw = []
        for provider in self.providers:
            raw.extend(provider.search(job.query))
        listings = MarketplaceNormalizer.normalize_many(raw)
        listings = ListingDeduper.dedupe(listings)
        for listing in listings:
            listing.scout_score = self.score_listing(listing)
        self.queue.add_many(listings)
        return listings

    def run_all(self):
        results = []
        for job in self.jobs:
            if job.enabled:
                results.extend(self.run_job(job))
        return results

    @staticmethod
    def score_listing(listing):
        title = (listing.title or "").lower()
        score = 5.0
        if "gold" in title or "/10" in title:
            score += 2
        if "auto" in title or "rpa" in title:
            score += 1
        if "psa 10" in title:
            score += 1
        return min(score, 10.0)
