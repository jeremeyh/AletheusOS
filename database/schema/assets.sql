CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_name TEXT NOT NULL,
    category TEXT,
    player TEXT,
    team TEXT,
    year TEXT,
    purchase_price REAL DEFAULT 0,
    current_value REAL DEFAULT 0,
    status TEXT,
    created_at TEXT,
    updated_at TEXT
);
