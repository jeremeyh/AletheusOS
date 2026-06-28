from enum import Enum

class AssetStatus(Enum):
    TARGET='Target'
    NEGOTIATING='Negotiating'
    PURCHASED='Purchased'
    SHIPPING='Shipping'
    RECEIVED='Received'
    VAULTED='Vaulted'
    GRADING='Grading'
    PORTFOLIO='Portfolio'
    LISTED='Listed'
    SOLD='Sold'
    ARCHIVED='Archived'

class AssetWorkflow:
    """CardHawk OS™ Asset Lifecycle."""
    def __init__(self, asset):
        self.asset = asset

    def transition(self, status: AssetStatus):
        self.asset.status = status.value
        return self.asset
