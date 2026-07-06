from pathlib import Path


class ConclaveShield:
    def __init__(self, root, protected_paths):
        self.root = Path(root).resolve()
        self.protected_paths = [self.root / p for p in protected_paths]

    def is_protected(self, path) -> bool:
        target = (self.root / path).resolve()

        for protected in self.protected_paths:
            try:
                target.relative_to(protected.resolve())
                return True
            except ValueError:
                continue

        return False

    def classify_action(self, action: str, target: str = "") -> str:
        lowered = f"{action} {target}".lower()

        destructive_markers = [
            "delete",
            "remove",
            "wipe",
            "destroy",
            "overwrite",
            "exfiltrate",
            "leak",
            "dump",
        ]

        if any(marker in lowered for marker in destructive_markers):
            if target and self.is_protected(target):
                return "blocked_protected_destructive"
            return "suspicious_destructive"

        if target and self.is_protected(target):
            return "protected_access"

        return "allowed"
