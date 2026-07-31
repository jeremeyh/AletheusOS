class Provider:
    NAME = "Mercari"

    def search(self, query: str):
        return []

    def normalize(self, record: dict):
        return record
