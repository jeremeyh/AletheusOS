class SellingWorkflow:
    """Listing and sale workflow."""
    def list_asset(self, asset, marketplace, asking_price):
        asset.status='Listed'
        asset.marketplace=marketplace
        asset.current_value=asking_price
        return asset

    def complete_sale(self, asset, sale_price):
        asset.status='Sold'
        asset.current_value=sale_price
        return asset
