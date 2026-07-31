"""
Card Hawk Runtime Application

Genesis 13.13
"""

from .lifecycle import CardHawkLifecycle
from .manifest import CARD_HAWK_MANIFEST


class CardHawkApplication:
    def __init__(self, intelligence=None):

        self.manifest = CARD_HAWK_MANIFEST

        self.intelligence = intelligence

        self.lifecycle = CardHawkLifecycle()

    def start(self):

        return self.lifecycle.start()

    def health(self):

        return {
            "application": self.manifest["application_id"],
            "runtime": self.lifecycle.health(),
            "intelligence": bool(self.intelligence),
        }

    def capabilities(self):

        return self.manifest["capabilities"]
