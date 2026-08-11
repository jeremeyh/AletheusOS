"""
Card Hawk Asset Form

Version 3.0.0
"""

from cardhawk.services import AssetService


class AssetForm:
    def __init__(self):

        self.service = AssetService()

    def create(self, **kwargs):

        return self.service.create_asset(**kwargs)
