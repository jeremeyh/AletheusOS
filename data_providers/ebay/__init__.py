class Provider:
    NAME = "Ebay"

    def search(self, query: str):
        return []

    def normalize(self, record: dict):
        return record
