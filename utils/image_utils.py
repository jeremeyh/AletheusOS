from pathlib import Path
import base64
import uuid
import shutil

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

def image_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

def image_tag(path: Path | None, css_class: str, fallback: str = "🦅") -> str:
    if path and path.exists():
        ext = path.suffix.lower().replace(".", "")
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        return f'<img class="{css_class}" src="data:image/{mime};base64,{image_to_base64(path)}" />'
    return f'<div class="{css_class}" style="font-size:6rem;">{fallback}</div>'

def save_uploaded_image(uploaded_file, destination_dir: Path, prefix: str = "asset") -> str:
    if uploaded_file is None:
        return ""
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Unsupported image type. Use PNG, JPG, JPEG, or WEBP.")
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{prefix}_{uuid.uuid4().hex[:12]}{suffix}"
    target = destination_dir / filename
    with target.open("wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    return str(target)
