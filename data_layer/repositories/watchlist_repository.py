from datetime import datetime

from data_layer.database_manager import db


class WatchlistRepository:
    @staticmethod
    def create(title, player="", query="", max_price=0, target_thorx=0, notes=""):
        db.execute(
            """
            INSERT INTO watchlist (title, player, query, max_price, target_thorx, status, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                title,
                player,
                query,
                max_price,
                target_thorx,
                "Active",
                notes,
                datetime.utcnow().isoformat(),
            ),
        )

    @staticmethod
    def all():
        return db.query("SELECT * FROM watchlist ORDER BY watch_id DESC")

    @staticmethod
    def close(watch_id):
        db.execute("UPDATE watchlist SET status='Closed' WHERE watch_id=?", (watch_id,))
