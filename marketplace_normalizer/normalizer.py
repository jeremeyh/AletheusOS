from marketplace_normalizer.normalized_listing import NormalizedListing


class MarketplaceNormalizer:
    """Universal Marketplace Normalizer™."""

    @staticmethod
    def normalize(raw) -> NormalizedListing:
        if isinstance(raw, dict):
            get = raw.get
        else:
            get = lambda k, default=None: getattr(raw, k, default)

        return NormalizedListing(
            title=get("title", ""),
            price=float(get("price", 0) or 0),
            marketplace=get("marketplace", ""),
            url=get("url", ""),
            seller=get("seller", ""),
            image_url=get("image_url", ""),
            raw=get("raw", {}) if not isinstance(raw, dict) else raw,
        )

    @staticmethod
    def normalize_many(raw_rows):
        return [MarketplaceNormalizer.normalize(row) for row in raw_rows]
