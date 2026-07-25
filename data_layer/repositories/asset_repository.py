from datetime import datetime

from data_layer.database_manager import db


class AssetRepository:
    """Repository for canonical Asset Vault™ persistence."""

    TABLE = "assets"

    @staticmethod
    def create(data):
        data = dict(data or {})
        now = datetime.utcnow().isoformat()
        data.setdefault("created_at", now)
        data.setdefault("updated_at", now)

        columns = db.columns(AssetRepository.TABLE)
        clean = {k: v for k, v in data.items() if k in columns and k != "asset_id"}

        if not clean:
            return None

        keys = list(clean.keys())
        placeholders = ",".join(["?"] * len(keys))
        sql = f"INSERT INTO assets ({','.join(keys)}) VALUES ({placeholders})"
        cur = db.execute(sql, [clean[k] for k in keys])
        return cur.lastrowid

    @staticmethod
    def all():
        return db.query("SELECT * FROM assets ORDER BY asset_id DESC")

    @staticmethod
    def get(asset_id):
        return db.query_one("SELECT * FROM assets WHERE asset_id = ?", (asset_id,))

    @staticmethod
    def update(asset_id, data):
        data = dict(data or {})
        data["updated_at"] = datetime.utcnow().isoformat()
        columns = db.columns(AssetRepository.TABLE)
        clean = {k: v for k, v in data.items() if k in columns and k != "asset_id"}
        if not clean:
            return False
        assignments = ",".join([f"{k}=?" for k in clean])
        db.execute(f"UPDATE assets SET {assignments} WHERE asset_id=?", list(clean.values()) + [asset_id])
        return True

    @staticmethod
    def delete(asset_id):
        db.execute("DELETE FROM assets WHERE asset_id=?", (asset_id,))
        return True

    @staticmethod
    def search(query):
        q = f"%{query}%"
        return db.query("""
            SELECT * FROM assets
            WHERE player LIKE ? OR team LIKE ? OR brand LIKE ? OR set_name LIKE ?
               OR parallel LIKE ? OR serial_number LIKE ? OR notes LIKE ? OR tags LIKE ?
            ORDER BY asset_id DESC
        """, (q, q, q, q, q, q, q, q))
