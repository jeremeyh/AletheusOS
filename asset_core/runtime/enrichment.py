import sqlite3

from marketplace.runtime.value import MarketplaceValue
from engines.thorx.runtime import ThorX

from asset_core.repository.asset_repository import AssetRepository

DB = "data/cardhawk.db"


class AssetEnrichmentEngine:
    """
    Refreshes existing assets with the latest intelligence.
    """

    @staticmethod
    def refresh_all():

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute("SELECT * FROM assets")

        rows = cur.fetchall()

        conn.close()

        updated = 0

        for row in rows:

            card = dict(row)

            market = MarketplaceValue.estimate(card)

            AssetRepository.update_market(
                card["id"],
                market,
            )

            thorx = ThorX.score(card)

            AssetRepository.update_thorx(
                card["id"],
                thorx["score"],
            )

            updated += 1

        return updated
