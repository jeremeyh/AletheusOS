class AssetTags:
    """
    Asset Tags™

    Lightweight tagging helpers for filtering, grouping, and searching.
    """
    @staticmethod
    def normalize(tags):
        if not tags:
            return []
        if isinstance(tags, str):
            tags = tags.split(",")
        return sorted({str(tag).strip().lower() for tag in tags if str(tag).strip()})

    @staticmethod
    def to_string(tags):
        return ", ".join(AssetTags.normalize(tags))
