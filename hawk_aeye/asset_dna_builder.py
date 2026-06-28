class AssetDNABuilder:
    """Builds suggested Asset DNA™ from Hawk A⦿Eye™ detections."""

    @staticmethod
    def build(results: dict) -> dict:
        return {
            "category": results.get("category", {}).get("category", "Trading Card"),
            "player": results.get("player", {}).get("player", ""),
            "year": results.get("year", {}).get("year", 2025) or 2025,
            "brand": results.get("brand", {}).get("brand", ""),
            "parallel": results.get("parallel", {}).get("parallel", ""),
            "serial_number": results.get("serial", {}).get("serial_number", ""),
            "print_run": results.get("serial", {}).get("print_run", None),
            "condition_notes": "; ".join(results.get("condition", {}).get("notes", [])),
            "hawk_aeye_confidence": AssetDNABuilder.confidence(results),
        }

    @staticmethod
    def confidence(results: dict) -> float:
        keys = ["ocr", "category", "player", "brand", "year", "parallel", "serial"]
        vals = []
        for key in keys:
            item = results.get(key, {})
            if isinstance(item, dict):
                vals.append(float(item.get("confidence", 0) or 0))
        return round(sum(vals) / len(vals), 2) if vals else 0.0
