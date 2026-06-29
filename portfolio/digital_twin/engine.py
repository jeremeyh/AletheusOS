import sqlite3
from collections import defaultdict

DB = "data/cardhawk.db"


class PortfolioDigitalTwin:
    """
    CardHawk Portfolio Digital Twin™

    Builds a live model of the Asset Vault.
    """

    @staticmethod
    def snapshot():

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                player,
                team,
                sport,
                brand,
                set_name,
                current_value,
                purchase_price,
                thorx_score
            FROM assets
            ORDER BY id DESC
            """
        )

        rows = [dict(row) for row in cur.fetchall()]

        conn.close()

        total_value = sum(float(row.get("current_value") or 0) for row in rows)

        total_cost = sum(float(row.get("purchase_price") or 0) for row in rows)

        avg_thorx = 0

        scored = [
            float(row.get("thorx_score") or 0)
            for row in rows
            if float(row.get("thorx_score") or 0) > 0
        ]

        if scored:
            avg_thorx = round(sum(scored) / len(scored), 2)

        by_player = defaultdict(float)

        for row in rows:
            player = row.get("player") or "Unknown"
            by_player[player] += float(row.get("current_value") or 0)

        top_assets = sorted(
            rows,
            key=lambda row: float(row.get("current_value") or 0),
            reverse=True,
        )[:10]

        return {
            "asset_count": len(rows),
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "gain_loss": round(total_value - total_cost, 2),
            "average_thorx": avg_thorx,
            "allocation_by_player": dict(by_player),
            "top_assets": top_assets,
        }
