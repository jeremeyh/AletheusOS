class Provider:
    NAME = "Fanatics"

    def search(self, query: str):
        return []

    def normalize(self, record: dict):
        return record
