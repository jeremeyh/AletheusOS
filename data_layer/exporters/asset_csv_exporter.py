import csv
from data_layer.repositories.asset_repository import AssetRepository

class AssetCSVExporter:
    @staticmethod
    def export_file(path):
        rows = AssetRepository.all()
        if not rows:
            with open(path, "w", newline="", encoding="utf-8") as f:
                f.write("")
            return path

        keys = sorted(rows[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)
        return path
