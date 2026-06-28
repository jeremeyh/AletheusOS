import sqlite3

DB = "data/cardhawk.db"


class PortfolioEngine:

    @staticmethod
    def summary():

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        cur.execute("""
            SELECT
                COUNT(*) assets,
                COALESCE(SUM(current_value),0) value,
                COALESCE(AVG(thorx_score),0) thorx
            FROM assets
        """)

        row = dict(cur.fetchone())

        conn.close()

        return {
            "assets": row["assets"],
            "portfolio_value": round(row["value"],2),
            "average_thorx": round(row["thorx"],2),
        }
