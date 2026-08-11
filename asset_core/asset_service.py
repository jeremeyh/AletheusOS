from asset_core.asset_factory import AssetFactory
from asset_core.asset_filters import AssetFilters
from asset_core.asset_search import AssetSearch
from services.asset_service import AssetService as CoreAssetService


class DomainAssetService:
    """
    Asset Domain Service™

    Higher-level asset package facade.
    Uses the existing Core AssetService for persistence.
    """

    @staticmethod
    def create_asset(**kwargs):
        asset = AssetFactory.create(**kwargs)
        CoreAssetService.create(asset)
        return asset

    @staticmethod
    def all_assets():
        return CoreAssetService.get_all()

    @staticmethod
    def search(assets, query):
        return AssetSearch.filter(assets, query)

    @staticmethod
    def filter_by_sport(assets, sport):
        return AssetFilters.by_sport(assets, sport)

    @staticmethod
    def filter_by_team(assets, team):
        return AssetFilters.by_team(assets, team)

    @staticmethod
    def filter_by_min_thorx(assets, minimum):
        return AssetFilters.by_min_thorx(assets, minimum)
