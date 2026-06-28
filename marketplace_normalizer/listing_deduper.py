class ListingDeduper:
    """Deduplicates normalized listings."""

    @staticmethod
    def dedupe(listings):
        seen = set()
        out = []
        for listing in listings:
            key = (
                (listing.title or "").lower().strip(),
                (listing.marketplace or "").lower().strip(),
                (listing.url or "").lower().strip(),
            )
            if key not in seen:
                seen.add(key)
                out.append(listing)
        return out
