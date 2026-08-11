import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import sqlite3

from asset_core.repository.asset_repository import AssetRepository
from engines.thorx.runtime import ThorX

DB = "data/cardhawk.db"


def main():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            player,
            year,
            brand,
            set_name,
            parallel,
            serial_number,
            autograph,
            patch,
            grade,
            thorx_score
        FROM assets
        WHERE thorx_score IS NULL
           OR thorx_score = 0
        """
    )

    rows = cur.fetchall()

    print("=" * 70)
    print(f"Found {len(rows)} asset(s) requiring THORᵡ scoring.")
    print("=" * 70)

    updated = 0

    for row in rows:
        card = {
            "player": row["player"],
            "year": row["year"],
            "brand": row["brand"],
            "set": row["set_name"],
            "parallel": row["parallel"],
            "serial": row["serial_number"],
            "autograph": bool(row["autograph"]),
            "patch": bool(row["patch"]),
            "grade": row["grade"],
        }

        try:
            score = ThorX.score(card)

            AssetRepository.update_thorx(
                row["id"],
                score,
            )

            print(f"Asset {row['id']:>3} | {row['player']} | THORᵡ {score}")

            updated += 1

        except Exception as exc:
            print(f"Asset {row['id']} failed: {exc}")

    conn.close()

    print()
    print("=" * 70)
    print(f"Updated {updated} asset(s).")
    print("=" * 70)


if __name__ == "__main__":
    main()
