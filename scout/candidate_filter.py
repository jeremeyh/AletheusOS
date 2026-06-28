class CandidateFilter:
    """Filters marketplace listings into Scout™ candidates."""

    @staticmethod
    def price_under(candidate, max_price):
        if max_price is None:
            return True
        return float(candidate.price or 0) <= float(max_price)

    @staticmethod
    def title_contains(candidate, terms):
        if not terms:
            return True
        title = (candidate.title or "").lower()
        return all(term.lower() in title for term in terms)

    @staticmethod
    def dedupe(candidates):
        seen = set()
        unique = []
        for candidate in candidates:
            key = (candidate.title.lower().strip(), candidate.marketplace.lower().strip(), candidate.url)
            if key not in seen:
                seen.add(key)
                unique.append(candidate)
        return unique

    @staticmethod
    def apply_watch_target(candidates, target):
        terms = target.query.split()
        filtered = [
            candidate for candidate in candidates
            if CandidateFilter.title_contains(candidate, terms)
            and CandidateFilter.price_under(candidate, target.max_price)
        ]
        return CandidateFilter.dedupe(filtered)
