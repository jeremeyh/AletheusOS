from models.asset import Asset
from asset_core.asset_validator import AssetValidator
from asset_core.asset_tags import AssetTags

class AssetFactory:
    """
    Asset Factory™

    Creates validated Asset objects with normalized CardHawk OS™ defaults.
    """
    @staticmethod
    def create(**kwargs) -> Asset:
        if "tags" in kwargs:
            kwargs["tags"] = AssetTags.to_string(kwargs["tags"])

        asset = Asset(**kwargs)
        AssetValidator.validate(asset)
        return asset
