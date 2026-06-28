import csv
from data_layer.repositories.asset_repository import AssetRepository

class AssetCSVImporter:
    """Imports CSV rows into Asset Vault™."""

    @staticmethod
    def import_file(path):
        created = []
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean = {k.strip(): v for k, v in row.items() if k}
                asset_id = AssetRepository.create(clean)
                created.append(asset_id)
        return created
