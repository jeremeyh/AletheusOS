from asset_core.asset_tags import AssetTags
from asset_core.asset_validator import AssetValidator
from models.asset import Asset


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
