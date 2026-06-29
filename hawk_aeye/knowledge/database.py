import json
from pathlib import Path


class KnowledgeDatabase:
    """
    Hawk A•Eye™

    Knowledge Base

    Central repository for players,
    brands, sets, and parallels.
    """

    FILE = (
        Path(__file__)
        .parent
        / "card_database.json"
    )

    @classmethod
    def load(cls):

        with open(cls.FILE, "r") as f:

            return json.load(f)
