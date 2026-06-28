import sqlite3
from pathlib import Path
from typing import Any, Iterable


DB_PATH = Path("data/cardhawk.db")


class Database:
    """
    CardHawk OS™ Database Service

    This is the only service that should talk directly to SQLite.
    It also performs safe additive migrations so older local databases
    keep working as CardHawk OS™ grows.
    """

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.initialize()

    def execute(self, query: str, params: Iterable[Any] = ()):
        cur = self.conn.cursor()
        cur.execute(query, tuple(params))
        self.conn.commit()
        return cur

    def executemany(self, query: str, params: Iterable[Iterable[Any]]):
        cur = self.conn.cursor()
        cur.executemany(query, params)
        self.conn.commit()
        return cur

    def query(self, query: str, params: Iterable[Any] = ()):
        cur = self.conn.cursor()
        cur.execute(query, tuple(params))
        return cur.fetchall()

    def query_one(self, query: str, params: Iterable[Any] = ()):
        cur = self.conn.cursor()
        cur.execute(query, tuple(params))
        return cur.fetchone()

    def close(self):
        self.conn.close()

    def table_exists(self, table_name: str) -> bool:
        row = self.query_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return row is not None

    def get_columns(self, table_name: str) -> set[str]:
        if not self.table_exists(table_name):
            return set()
        return {row["name"] for row in self.query(f"PRAGMA table_info({table_name})")}

    def column_exists(self, table_name: str, column_name: str) -> bool:
        return column_name in self.get_columns(table_name)

    def add_column_if_missing(self, table_name: str, column_name: str, column_type: str):
        if not self.column_exists(table_name, column_name):
            self.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

    def initialize(self):
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS assets (
                asset_id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """
        )

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS genome_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """
        )

        self.migrate_assets_table()
        self.migrate_genome_table()

    def migrate_assets_table(self):
        """
        Additive migration only.

        This intentionally does not drop or recreate the assets table, because
        local CardHawk data must survive schema upgrades.
        """
        columns = {
            # Identity
            "uuid": "TEXT",
            "asset_name": "TEXT DEFAULT ''",
            "asset_type": "TEXT DEFAULT ''",
            "category": "TEXT DEFAULT 'Trading Card'",
            "status": "TEXT DEFAULT 'Active'",

            # Classification
            "sport": "TEXT DEFAULT ''",
            "league": "TEXT DEFAULT ''",
            "team": "TEXT DEFAULT ''",
            "player": "TEXT DEFAULT ''",
            "year": "INTEGER DEFAULT 0",
            "manufacturer": "TEXT DEFAULT ''",
            "brand": "TEXT DEFAULT ''",
            "product": "TEXT DEFAULT ''",
            "set_name": "TEXT DEFAULT ''",
            "subset": "TEXT DEFAULT ''",
            "card_number": "TEXT DEFAULT ''",
            "variation": "TEXT DEFAULT ''",
            "parallel": "TEXT DEFAULT ''",

            # Premium Attributes
            "serial_number": "TEXT DEFAULT ''",
            "print_run": "INTEGER DEFAULT 0",
            "rookie": "INTEGER DEFAULT 0",
            "first_bowman": "INTEGER DEFAULT 0",
            "autograph": "INTEGER DEFAULT 0",
            "auto_type": "TEXT DEFAULT ''",
            "patch": "INTEGER DEFAULT 0",
            "memorabilia": "INTEGER DEFAULT 0",
            "one_of_one": "INTEGER DEFAULT 0",
            "case_hit": "INTEGER DEFAULT 0",
            "ssp": "INTEGER DEFAULT 0",
            "sp": "INTEGER DEFAULT 0",

            # Physical / Grading
            "condition": "TEXT DEFAULT 'Raw'",
            "grade_company": "TEXT DEFAULT ''",
            "grading_company": "TEXT DEFAULT ''",
            "grade": "TEXT DEFAULT ''",
            "centering": "TEXT DEFAULT ''",
            "corners": "TEXT DEFAULT ''",
            "edges": "TEXT DEFAULT ''",
            "surface": "TEXT DEFAULT ''",
            "eye_appeal": "TEXT DEFAULT ''",

            # Acquisition
            "purchase_price": "REAL DEFAULT 0",
            "shipping": "REAL DEFAULT 0",
            "shipping_cost": "REAL DEFAULT 0",
            "tax": "REAL DEFAULT 0",
            "fees": "REAL DEFAULT 0",
            "cost_basis": "REAL DEFAULT 0",
            "purchase_date": "TEXT DEFAULT ''",
            "marketplace": "TEXT DEFAULT ''",
            "seller": "TEXT DEFAULT ''",
            "seller_rating": "TEXT DEFAULT ''",
            "payment_method": "TEXT DEFAULT ''",
            "order_number": "TEXT DEFAULT ''",
            "tracking": "TEXT DEFAULT ''",
            "listing_url": "TEXT DEFAULT ''",

            # Valuation
            "current_value": "REAL DEFAULT 0",
            "market_value": "REAL DEFAULT 0",
            "floor": "REAL DEFAULT 0",
            "floor_value": "REAL DEFAULT 0",
            "target_value": "REAL DEFAULT 0",
            "ceiling": "REAL DEFAULT 0",
            "ceiling_value": "REAL DEFAULT 0",
            "cloud": "REAL DEFAULT 0",
            "cloud_value": "REAL DEFAULT 0",
            "nuclear": "REAL DEFAULT 0",
            "nuclear_value": "REAL DEFAULT 0",
            "insurance_value": "REAL DEFAULT 0",
            "replacement_value": "REAL DEFAULT 0",
            "highest_offer": "REAL DEFAULT 0",
            "lowest_offer": "REAL DEFAULT 0",

            # THORx / DEF / DEX
            "thorx_score": "REAL DEFAULT 0",
            "ni_score": "REAL DEFAULT 0",
            "q_def": "REAL DEFAULT 0",
            "d_def": "REAL DEFAULT 0",
            "classification": "TEXT DEFAULT ''",
            "qualification_gate": "TEXT DEFAULT ''",
            "strike_zone": "INTEGER DEFAULT 0",
            "opportunity_rank": "INTEGER DEFAULT 0",
            "confidence": "REAL DEFAULT 0",
            "recommendation": "TEXT DEFAULT ''",
            "scarcity_score": "REAL DEFAULT 0",
            "eye_appeal_score": "REAL DEFAULT 0",
            "visual_gravitas_score": "REAL DEFAULT 0",
            "historical_score": "REAL DEFAULT 0",
            "market_score": "REAL DEFAULT 0",
            "liquidity_score": "REAL DEFAULT 0",
            "risk_score": "REAL DEFAULT 0",
            "player_thesis_score": "REAL DEFAULT 0",
            "portfolio_fit_score": "REAL DEFAULT 0",
            "capital_efficiency_score": "REAL DEFAULT 0",
            "time_efficiency_score": "REAL DEFAULT 0",

            # Media / Hawk A-Eye
            "image_path": "TEXT DEFAULT ''",
            "front_image": "TEXT DEFAULT ''",
            "back_image": "TEXT DEFAULT ''",
            "image_hash": "TEXT DEFAULT ''",
            "hawk_aeye_status": "TEXT DEFAULT ''",
            "hawk_aeye_confidence": "REAL DEFAULT 0",
            "hawk_aeye_notes": "TEXT DEFAULT ''",

            # Marketplace Intelligence
            "active_listings": "INTEGER DEFAULT 0",
            "sold_comps": "INTEGER DEFAULT 0",
            "highest_sale": "REAL DEFAULT 0",
            "lowest_sale": "REAL DEFAULT 0",
            "average_sale": "REAL DEFAULT 0",
            "market_velocity": "REAL DEFAULT 0",

            # Portfolio
            "roi": "REAL DEFAULT 0",
            "gain_loss": "REAL DEFAULT 0",
            "allocation": "TEXT DEFAULT ''",
            "annual_return": "REAL DEFAULT 0",
            "portfolio_weight": "REAL DEFAULT 0",

            # Storage
            "storage_location": "TEXT DEFAULT ''",
            "vault_location": "TEXT DEFAULT ''",
            "safe": "TEXT DEFAULT ''",
            "shelf": "TEXT DEFAULT ''",
            "box": "TEXT DEFAULT ''",
            "row": "TEXT DEFAULT ''",
            "slot": "TEXT DEFAULT ''",
            "qr_code": "TEXT DEFAULT ''",

            # Notes
            "notes": "TEXT DEFAULT ''",
            "tags": "TEXT DEFAULT ''",
            "founder_notes": "TEXT DEFAULT ''",
            "thorx_commentary": "TEXT DEFAULT ''",
            "acquisition_notes": "TEXT DEFAULT ''",
            "disposition_notes": "TEXT DEFAULT ''",
            "agent_notes": "TEXT DEFAULT ''",
            "prediction_notes": "TEXT DEFAULT ''",
            "learning_state": "TEXT DEFAULT ''",

            # Lifecycle
            "created_at": "TEXT DEFAULT ''",
            "updated_at": "TEXT DEFAULT ''",
            "date_sold": "TEXT DEFAULT ''",
            "sale_price": "REAL DEFAULT 0",
            "marketplace_sold": "TEXT DEFAULT ''",
            "buyer": "TEXT DEFAULT ''",
            "realized_profit": "REAL DEFAULT 0",
            "hold_time": "TEXT DEFAULT ''",
        }

        for column_name, column_type in columns.items():
            self.add_column_if_missing("assets", column_name, column_type)

    def migrate_genome_table(self):
        columns = {
            "asset_id": "INTEGER",
            "event_type": "TEXT DEFAULT ''",
            "event_note": "TEXT DEFAULT ''",
            "previous_value": "TEXT DEFAULT ''",
            "new_value": "TEXT DEFAULT ''",
            "source": "TEXT DEFAULT 'CardHawk OS'",
            "created_at": "TEXT DEFAULT ''",
        }

        for column_name, column_type in columns.items():
            self.add_column_if_missing("genome_events", column_name, column_type)


db = Database()
