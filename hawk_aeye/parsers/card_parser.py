import re


class CardParser:

    @staticmethod
    def parse(text: str):

        upper = text.upper()

        data = {
            "player": None,
            "year": None,
            "brand": None,
            "set": None,
            "grade": None,
        }

        # Year
        m = re.search(r"\b(19|20)\d{2}\b", upper)
        if m:
            data["year"] = int(m.group())

        # Player
        if "CALEB WILLIAMS" in upper:
            data["player"] = "Caleb Williams"

        # Brand
        if "LEAF" in upper:
            data["brand"] = "Leaf"

        # Set
        if "METAL" in upper:
            data["set"] = "Metal Draft"

        # Grade
        if "GEM MT" in upper:
            data["grade"] = "Gem Mint"

        return data
