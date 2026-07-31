class AssetSearch:
    """
    Asset Search™

    Text and structured search helpers.
    """

    @staticmethod
    def matches(asset, query: str) -> bool:
        if not query:
            return True

        q = query.lower().strip()

        fields = [
            getattr(asset, "player", ""),
            getattr(asset, "team", ""),
            getattr(asset, "sport", ""),
            getattr(asset, "brand", ""),
            getattr(asset, "set_name", ""),
            getattr(asset, "parallel", ""),
            getattr(asset, "serial_number", ""),
            getattr(asset, "tags", ""),
        ]

        haystack = " ".join(str(field).lower() for field in fields)
        return q in haystack

    @staticmethod
    def filter(assets, query: str):
        return [asset for asset in assets if AssetSearch.matches(asset, query)]
