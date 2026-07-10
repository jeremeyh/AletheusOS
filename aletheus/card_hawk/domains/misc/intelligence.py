"""
Miscellaneous Collectible Intelligence

Genesis 13.22
"""


class MiscCollectibleEngine:


    def evaluate(
        self,
        item
    ):


        return {


            "category":

                item.category,


            "rarity":

                item.rarity_score

        }

