"""
Asset Memory Store

Genesis 13.47
"""


class AssetMemory:


    def __init__(self):

        self.records = []



    def remember(
        self,
        record
    ):

        self.records.append(
            record
        )

