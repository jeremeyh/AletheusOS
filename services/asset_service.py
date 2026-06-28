from datetime import datetime
from typing import Any

from models.asset import Asset
from services.database import db


class AssetService:
    """
    CardHawk OS™ Asset Service

    Business logic layer for Asset Vault™.
    UI pages should use this service instead of direct SQL.
    """

    ASSET_FIELDS = [
        "category", "sport", "player", "team", "year", "brand", "set_name",
        "subset", "card_number", "parallel", "serial_number", "print_run",
        "autograph", "memorabilia", "grade_company", "grade", "condition",
        "purchase_price", "shipping_cost", "tax", "fees", "purchase_date",
        "marketplace", "seller", "current_value", "floor_value",
        "ceiling_value", "nuclear_value", "thorx_score", "ni_score",
        "q_def", "d_def", "strike_zone", "opportunity_rank", "confidence",
        "front_image", "back_image", "notes", "tags",
    ]

    @staticmethod
    def _asset_to_dict(asset: Asset) -> dict[str, Any]:
        data = {}
        for field in AssetService.ASSET_FIELDS:
            if hasattr(asset, field):
                value = getattr(asset, field)
                if isinstance(value, bool):
                    value = int(value)
                data[field] = value

        # Compatibility aliases
        if "shipping_cost" in data:
            data["shipping"] = data["shipping_cost"]

        data["cost_basis"] = float(data.get("purchase_price") or 0) + float(data.get("shipping_cost") or 0) + float(data.get("tax") or 0) + float(data.get("fees") or 0)
        data["market_value"] = float(data.get("current_value") or 0)
        data["gain_loss"] = float(data.get("current_value") or 0) - data["cost_basis"]
        data["roi"] = (data["gain_loss"] / data["cost_basis"] * 100) if data["cost_basis"] else 0

        if not data.get("created_at"):
            data["created_at"] = datetime.now().isoformat()
        data["updated_at"] = datetime.now().isoformat()

        if not data.get("asset_name"):
            pieces = [
                str(data.get("year") or "").strip(),
                str(data.get("brand") or "").strip(),
                str(data.get("player") or "").strip(),
                str(data.get("parallel") or "").strip(),
            ]
            data["asset_name"] = " ".join([p for p in pieces if p]).strip()

        return data

    @staticmethod
    def create(asset: Asset):
        data = AssetService._asset_to_dict(asset)

        existing_columns = db.get_columns("assets")
        insert_data = {k: v for k, v in data.items() if k in existing_columns and k != "asset_id"}

        columns = list(insert_data.keys())
        placeholders = ", ".join(["?"] * len(columns))
        column_sql = ", ".join(columns)
        values = [insert_data[c] for c in columns]

        cur = db.execute(
            f"INSERT INTO assets ({column_sql}) VALUES ({placeholders})",
            values,
        )

        asset_id = cur.lastrowid

        try:
            from services.genome_service import GenomeService
            GenomeService.record_event(
                asset_id=asset_id,
                event_type="Asset Created",
                event_note="Initial Asset DNA™ record created.",
                source="AssetService",
            )
        except Exception:
            pass

        return asset_id

    @staticmethod
    def get_all():
        return db.query("SELECT * FROM assets ORDER BY asset_id DESC")

    @staticmethod
    def get_by_id(asset_id: int):
        return db.query_one("SELECT * FROM assets WHERE asset_id = ?", (asset_id,))

    @staticmethod
    def search(term: str = "", sport: str = "All", category: str = "All", min_thorx: float = 0):
        rows = AssetService.get_all()
        results = []

        term = (term or "").lower().strip()

        for row in rows:
            include = True

            haystack = " ".join(
                str(row[key] or "")
                for key in row.keys()
                if key in {"asset_name", "player", "team", "brand", "set_name", "parallel", "serial_number", "tags"}
            ).lower()

            if term and term not in haystack:
                include = False

            if sport != "All" and row["sport"] != sport:
                include = False

            if category != "All" and row["category"] != category:
                include = False

            if float(row["thorx_score"] or 0) < float(min_thorx or 0):
                include = False

            if include:
                results.append(row)

        return results

    @staticmethod
    def update(asset_id: int, updates: dict[str, Any]):
        if not updates:
            return

        existing_columns = db.get_columns("assets")
        clean_updates = {
            key: int(value) if isinstance(value, bool) else value
            for key, value in updates.items()
            if key in existing_columns and key != "asset_id"
        }

        clean_updates["updated_at"] = datetime.now().isoformat()

        assignments = ", ".join([f"{key}=?" for key in clean_updates.keys()])
        values = list(clean_updates.values()) + [asset_id]

        db.execute(f"UPDATE assets SET {assignments} WHERE asset_id=?", values)

        try:
            from services.genome_service import GenomeService
            GenomeService.record_event(
                asset_id=asset_id,
                event_type="Asset Updated",
                event_note="Asset DNA™ fields updated.",
                source="AssetService",
            )
        except Exception:
            pass

    @staticmethod
    def delete(asset_id: int):
        db.execute("DELETE FROM genome_events WHERE asset_id = ?", (asset_id,))
        db.execute("DELETE FROM assets WHERE asset_id = ?", (asset_id,))

    @staticmethod
    def archive(asset_id: int):
        AssetService.update(asset_id, {"status": "Archived"})

    @staticmethod
    def mark_sold(asset_id: int, sale_price: float, marketplace_sold: str = "", buyer: str = ""):
        asset = AssetService.get_by_id(asset_id)
        cost_basis = float(asset["cost_basis"] or asset["purchase_price"] or 0) if asset else 0
        realized_profit = float(sale_price or 0) - cost_basis

        AssetService.update(
            asset_id,
            {
                "status": "Sold",
                "date_sold": datetime.now().strftime("%Y-%m-%d"),
                "sale_price": sale_price,
                "marketplace_sold": marketplace_sold,
                "buyer": buyer,
                "realized_profit": realized_profit,
            },
        )
