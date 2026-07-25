import importlib
import sqlite3
from pathlib import Path


class RollbackManager:
    """Safe rollback helper."""

    def __init__(self, db_path="data/cardhawk.db"):
        self.db_path = Path(db_path)

    def rollback(self, migration):
        conn = sqlite3.connect(self.db_path)
        module = importlib.import_module(f"migrations.{migration}")
        if hasattr(module, "rollback"):
            module.rollback(conn)
        conn.execute("DELETE FROM migration_history WHERE migration = ?", (migration,))
        conn.commit()
        conn.close()
        return migration
