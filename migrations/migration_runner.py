import importlib
import sqlite3
from datetime import datetime
from pathlib import Path

from migrations.migration_registry import registered_migrations


class MigrationRunner:
    """Database Migration Framework™."""

    def __init__(self, db_path="data/cardhawk.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        return sqlite3.connect(self.db_path)

    def ensure_history(self, conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS migration_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration TEXT UNIQUE,
                applied_at TEXT
            )
        """)
        conn.commit()

    def applied(self, conn):
        self.ensure_history(conn)
        rows = conn.execute("SELECT migration FROM migration_history").fetchall()
        return {row[0] for row in rows}

    def run(self):
        conn = self.connect()
        self.ensure_history(conn)
        applied = self.applied(conn)
        completed = []

        for migration in registered_migrations():
            if migration in applied:
                continue
            module = importlib.import_module(f"migrations.{migration}")
            module.upgrade(conn)
            conn.execute(
                "INSERT OR IGNORE INTO migration_history (migration, applied_at) VALUES (?, ?)",
                (migration, datetime.utcnow().isoformat()),
            )
            conn.commit()
            completed.append(migration)

        conn.close()
        return completed
