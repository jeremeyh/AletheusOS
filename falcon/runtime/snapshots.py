import sqlite3
from datetime import datetime
from pathlib import Path

from decision_engine.runtime.engine import DecisionEngine
from nest.runtime.score import NestScoringEngine
from portfolio.digital_twin.engine import PortfolioDigitalTwin


DB = "data/cardhawk.db"


class FalconSnapshots:
    """
    FALCON™ Snapshot Engine

    Records portfolio intelligence snapshots over time.
    """

    @staticmethod
    def connect():
        Path("data").mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row

        return conn

    @staticmethod
    def ensure_schema():
        conn = FalconSnapshots.connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS falcon_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_count INTEGER DEFAULT 0,
                total_value REAL DEFAULT 0,
                total_cost REAL DEFAULT 0,
                gain_loss REAL DEFAULT 0,
                roi REAL DEFAULT 0,
                average_thorx REAL DEFAULT 0,
                average_def REAL DEFAULT 0,
                average_nest REAL DEFAULT 0,
                created_at TEXT
            )
            """
        )

        conn.commit()
        conn.close()

    @staticmethod
    def create():
        FalconSnapshots.ensure_schema()

        portfolio = PortfolioDigitalTwin.snapshot()
        def_summary = DecisionEngine.portfolio_summary()

        assets = portfolio.get("assets", [])

        nest_scores = []

        for asset in assets:
            nest = NestScoringEngine.calculate(asset)
            nest_scores.append(nest.score)

        average_nest = 0.0

        if nest_scores:
            average_nest = sum(nest_scores) / len(nest_scores)

        total_value = float(portfolio.get("total_value") or 0)
        total_cost = float(portfolio.get("total_cost") or 0)
        gain_loss = float(portfolio.get("gain_loss") or 0)

        roi = 0.0

        if total_cost > 0:
            roi = (gain_loss / total_cost) * 100

        snapshot = {
            "asset_count": int(portfolio.get("asset_count") or 0),
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "gain_loss": round(gain_loss, 2),
            "roi": round(roi, 2),
            "average_thorx": round(float(portfolio.get("average_thorx") or 0), 2),
            "average_def": round(float(def_summary.get("average_score") or 0), 2),
            "average_nest": round(average_nest, 2),
            "created_at": datetime.utcnow().isoformat(),
        }

        conn = FalconSnapshots.connect()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO falcon_snapshots (
                asset_count,
                total_value,
                total_cost,
                gain_loss,
                roi,
                average_thorx,
                average_def,
                average_nest,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot["asset_count"],
                snapshot["total_value"],
                snapshot["total_cost"],
                snapshot["gain_loss"],
                snapshot["roi"],
                snapshot["average_thorx"],
                snapshot["average_def"],
                snapshot["average_nest"],
                snapshot["created_at"],
            ),
        )

        conn.commit()
        snapshot_id = cur.lastrowid
        conn.close()

        snapshot["id"] = snapshot_id

        return snapshot

    @staticmethod
    def history(limit=30):
        FalconSnapshots.ensure_schema()

        conn = FalconSnapshots.connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM falcon_snapshots
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )

        rows = [dict(row) for row in cur.fetchall()]
        conn.close()

        return rows
