def upgrade(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS system_metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()

def rollback(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS system_metadata")
    conn.commit()
