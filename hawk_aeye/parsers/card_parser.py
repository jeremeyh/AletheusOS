import re

from hawk_aeye.models.card_fields import CardFields
from hawk_aeye.knowledge.database import KnowledgeDatabase


class CardParser:
    """
    Hawk A•Eye™

    Knowledge-driven parser.

    All supported players, brands, sets,
    and parallels come from the
    Hawk A•Eye Knowledge Database.
    """

    @staticmethod
    def parse(text):

        db = KnowledgeDatabase.load()

        card = CardFields()

        upper = text.upper()

        #
        # PLAYER
        #

        for player in db["players"]:

            if player in upper:

                card.player = player.title()

                break

        #
        # YEAR
        #

        year = re.search(r"(20\d{2})", upper)

        if year:

            card.year = int(year.group(1))

        #
        # BRAND
        #

        for brand in db["brands"]:

            if brand in upper:

                card.brand = brand.title()

                break

        #
        # SET
        #

        longest_sets = sorted(
            db["sets"],
            key=len,
            reverse=True,
        )

        for s in longest_sets:

            if s in upper:

                card.set = s.title()

                break

        #
        # PARALLEL
        #

        longest_parallels = sorted(
            db["parallels"],
            key=len,
            reverse=True,
        )

        for parallel in longest_parallels:

            if parallel in upper:

                card.parallel = parallel.title()

                break

        #
        # GRADE
        #

        if "GEM MT" in upper:

            card.grade = "Gem Mint"

        elif "MINT" in upper:

            card.grade = "Mint"

        #
        # AUTOGRAPH
        #

        if "AUTO" in upper or "AU-" in upper:

            card.autograph = True

        #
        # PATCH
        #

        if "PATCH" in upper:

            card.patch = True

        #
        # ROOKIE
        #

        if " ROOKIE " in upper or " RC " in upper:

            card.rookie = True

        #
        # SERIAL NUMBER
        #

        serial = re.search(r"/(\d+)", upper)

        if serial:

            card.serial = "/" + serial.group(1)

        return card.to_dict()
