from collections import Counter

from asset_core.repository.asset_repository import AssetRepository


class FalconDNA:
    """
    FALCON™ Collection DNA

    Learns portfolio patterns and acquisition tendencies.
    """

    @staticmethod
    def analyze():
        assets = AssetRepository.all(include_archived=False) or []

        players = Counter()
        brands = Counter()
        years = Counter()
        features = Counter()

        for asset in assets:
            if asset.get("player"):
                players[asset.get("player")] += 1

            if asset.get("brand"):
                brands[asset.get("brand")] += 1

            if asset.get("year"):
                years[str(asset.get("year"))] += 1

            if asset.get("autograph"):
                features["Autographs"] += 1

            if asset.get("patch"):
                features["Patch / Memorabilia"] += 1

            if asset.get("rookie"):
                features["Rookies"] += 1

            if asset.get("serial_number") or asset.get("print_run"):
                features["Serial Numbered"] += 1

        return {
            "top_players": players.most_common(5),
            "top_brands": brands.most_common(5),
            "top_years": years.most_common(5),
            "features": features.most_common(10),
        }
