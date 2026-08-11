import uuid
from datetime import datetime
from pathlib import Path
from shutil import copyfile

from asset_core.repository.asset_repository import AssetRepository
from hawk_aeye.runtime.pipeline import AssetPipeline
from hawk_aeye.vision.vision_engine import VisionEngine


class AssetIntakePipeline:
    """
    CardHawkOS Real Asset Intake™

    Handles upload storage, Hawk A•Eye™ analysis,
    visual intelligence, and Asset Vault save.
    """

    UPLOAD_DIR = Path("uploads/incoming")
    ASSET_DIR = Path("uploads/assets")

    @classmethod
    def ensure_dirs(cls):
        cls.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        cls.ASSET_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def save_upload(cls, uploaded_file):
        cls.ensure_dirs()

        suffix = Path(uploaded_file.name).suffix.lower() or ".jpg"

        filename = (
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{suffix}"
        )

        path = cls.UPLOAD_DIR / filename

        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return str(path)

    @classmethod
    def analyze(cls, image_path, asking_price=0):
        result = AssetPipeline.process(
            image_path,
            asking_price=asking_price,
        )

        result["vision_intelligence"] = VisionEngine.analyze(image_path)

        return result

    @classmethod
    def save_to_vault(cls, result, image_path):
        card = result["hawk"]["card"]

        market = result.get("market", {})
        vision = result.get("vision_intelligence", {})
        image_data = vision.get("image", {})

        card["market_value"] = market.get("current_value", 0)
        card["current_value"] = market.get("current_value", 0)
        card["thorx_score"] = result.get("thorx", 0)

        card["hawk_aeye_confidence"] = image_data.get("confidence", 0)
        card["image_hash"] = image_data.get("sha256", "")
        card["hawk_aeye_status"] = image_data.get("quality", "Unknown")
        card["hawk_aeye_notes"] = (
            f"Dimensions: {image_data.get('width', 0)}x{image_data.get('height', 0)} | "
            f"Brightness: {image_data.get('brightness', 0)} | "
            f"Orientation: {image_data.get('orientation', 'Unknown')}"
        )

        asset_id = AssetRepository.save(card)

        final_path = cls.ASSET_DIR / f"{asset_id}{Path(image_path).suffix.lower()}"

        copyfile(
            image_path,
            final_path,
        )

        AssetRepository.update(
            asset_id,
            {
                "image_path": str(final_path),
                "current_value": market.get("current_value", 0),
                "market_value": market.get("current_value", 0),
                "thorx_score": result.get("thorx", 0),
                "hawk_aeye_confidence": image_data.get("confidence", 0),
                "image_hash": image_data.get("sha256", ""),
                "hawk_aeye_status": image_data.get("quality", "Unknown"),
                "hawk_aeye_notes": card["hawk_aeye_notes"],
            },
        )

        AssetRepository.update_market(
            asset_id,
            market,
        )

        return {
            "asset_id": asset_id,
            "image_path": str(final_path),
            "card": AssetRepository.get(asset_id),
            "vision": vision,
        }
