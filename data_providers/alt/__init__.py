class Provider:
    NAME = "Alt"

    def search(self, query: str):
        return []

    def normalize(self, record: dict):
        return record
