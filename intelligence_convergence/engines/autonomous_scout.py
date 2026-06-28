from marketplace_normalizer.normalizer import MarketplaceNormalizer

class AutonomousScout:
    """Autonomous Scout™ continuous opportunity engine contract."""

    def __init__(self, providers=None):
        self.providers = providers or []
        self.fingerprints = set()

    def scan(self, query):
        raw = []
        for provider in self.providers:
            try:
                raw.extend(provider.search(query))
            except Exception:
                continue

        normalized = MarketplaceNormalizer.normalize_many(raw)
        results = []

        for listing in normalized:
            fingerprint = self.fingerprint(listing)
            is_new = fingerprint not in self.fingerprints
            self.fingerprints.add(fingerprint)
            listing.fingerprint = fingerprint
            listing.is_new = is_new
            listing.opportunity_score = self.score(listing)
            results.append(listing)

        return results

    @staticmethod
    def fingerprint(listing):
        return f"{listing.marketplace}|{listing.title}|{listing.price}|{listing.seller}".lower().strip()

    @staticmethod
    def score(listing):
        title = (listing.title or "").lower()
        score = 5.0
        if "gold" in title or "/10" in title:
            score += 2.0
        if "auto" in title or "rpa" in title:
            score += 1.0
        if "psa 10" in title:
            score += 1.0
        if getattr(listing, "is_new", False):
            score += 0.5
        return min(round(score, 2), 10.0)
