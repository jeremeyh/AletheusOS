from pathlib import Path
from zipfile import ZipFile


class PackageBuilder:
    """Release packaging helper."""

    @staticmethod
    def build(source=".", output="dist/cardhawk_release.zip"):
        source = Path(source)
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)

        exclude = {"venv", ".venv", "__pycache__", ".git", "dist"}

        with ZipFile(output, "w") as z:
            for p in source.rglob("*"):
                if any(part in exclude for part in p.parts):
                    continue
                if p.is_file():
                    z.write(p, arcname=str(p.relative_to(source)))

        return str(output)
