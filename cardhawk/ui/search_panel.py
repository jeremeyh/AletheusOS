"""
Card Hawk Search Panel

Version 3.0.0
"""

from cardhawk.services import AssetService


class SearchPanel:

    def __init__(self):

        self.service = AssetService()

    def search(self, text):

        return self.service.search(text)
