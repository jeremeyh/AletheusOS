def upgrade(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS migration_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            migration TEXT UNIQUE,
            applied_at TEXT
        )
    """)
    conn.commit()

def rollback(conn):
    # Do not drop migration history during safe rollback.
    pass
