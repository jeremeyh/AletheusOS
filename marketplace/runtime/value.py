class MarketplaceValue:

    @staticmethod
    def estimate(card):

        if card["player"] == "Caleb Williams":
            return {
                "current_value": 125.00,
                "floor": 90.00,
                "ceiling": 250.00,
            }

        return {
            "current_value": 0,
            "floor": 0,
            "ceiling": 0,
        }
@staticmethod
def update_market(asset_id, value):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE assets
        SET
            current_value=?,
            floor=?,
            ceiling=?
        WHERE id=?
        """,
        (
            value["current_value"],
            value["floor"],
            value["ceiling"],
            asset_id,
        ),
    )

    conn.commit()
    conn.close()
