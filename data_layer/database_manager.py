import sqlite3
from pathlib import Path

class DatabaseManager:
    """CardHawk OS™ 5.1 canonical persistence layer."""

    def __init__(self, db_path="data/cardhawk.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.initialize()

    def execute(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, tuple(params))
        self.conn.commit()
        return cur

    def query(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, tuple(params))
        return [dict(r) for r in cur.fetchall()]

    def query_one(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, tuple(params))
        row = cur.fetchone()
        return dict(row) if row else None

    def columns(self, table):
        try:
            return {r["name"] for r in self.query(f"PRAGMA table_info({table})")}
        except Exception:
            return set()

    def add_column(self, table, column, col_type):
        if column not in self.columns(table):
            self.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

    def initialize(self):
        self.execute("CREATE TABLE IF NOT EXISTS assets (asset_id INTEGER PRIMARY KEY AUTOINCREMENT)")
        fields = {
            "category": "TEXT", "sport": "TEXT", "player": "TEXT", "team": "TEXT",
            "year": "INTEGER", "brand": "TEXT", "set_name": "TEXT", "subset": "TEXT",
            "card_number": "TEXT", "parallel": "TEXT", "serial_number": "TEXT",
            "print_run": "INTEGER", "rookie": "INTEGER", "autograph": "INTEGER",
            "memorabilia": "INTEGER", "grade_company": "TEXT", "grade": "TEXT",
            "condition": "TEXT", "purchase_price": "REAL", "shipping_cost": "REAL",
            "tax": "REAL", "fees": "REAL", "purchase_date": "TEXT",
            "marketplace": "TEXT", "seller": "TEXT", "current_value": "REAL",
            "floor_value": "REAL", "ceiling_value": "REAL", "nuclear_value": "REAL",
            "thorx_score": "REAL", "ni_score": "REAL", "classification": "TEXT",
            "recommendation": "TEXT", "q_def": "REAL", "d_def": "REAL",
            "strike_zone": "INTEGER", "opportunity_rank": "INTEGER",
            "confidence": "REAL", "front_image": "TEXT", "back_image": "TEXT",
            "notes": "TEXT", "tags": "TEXT", "created_at": "TEXT", "updated_at": "TEXT",
        }
        for col, typ in fields.items():
            self.add_column("assets", col, typ)

        self.execute("""
            CREATE TABLE IF NOT EXISTS intelligence_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                source TEXT,
                message TEXT,
                payload TEXT,
                created_at TEXT
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                watch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                player TEXT,
                query TEXT,
                max_price REAL,
                target_thorx REAL,
                status TEXT,
                notes TEXT,
                created_at TEXT
            )
        """)

db = DatabaseManager()
