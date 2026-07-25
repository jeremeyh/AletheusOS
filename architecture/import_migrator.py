from pathlib import Path


class ImportMigrator:
    """
    Conservative import migration helper.

    By default this runs as a dry-run and returns proposed changes.
    Set apply=True to rewrite files.
    """

    REPLACEMENTS = {
        "from engine.": "from engines.",
        "import engine.": "import engines.",
        "from cardhawk_aeye.": "from hawk_aeye.",
        "import cardhawk_aeye.": "import hawk_aeye.",
        "hawk_a_eye": "hawk_aeye",
    }

    @staticmethod
    def migrate(root=".", apply=False):
        root = Path(root)
        changes = []

        for path in root.rglob("*.py"):
            if any(part in {".venv", "venv", "__pycache__"} for part in path.parts):
                continue

            original = path.read_text(errors="ignore")
            updated = original

            for old, new in ImportMigrator.REPLACEMENTS.items():
                updated = updated.replace(old, new)

            if updated != original:
                changes.append({
                    "file": str(path),
                    "changed": True,
                    "applied": apply,
                })
                if apply:
                    path.write_text(updated, encoding="utf-8")

        return changes
