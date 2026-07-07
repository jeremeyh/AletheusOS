from pathlib import Path

from .models import ArchitecturalFitnessReport


class PlatformIntelligenceEngine:
    """
    AletheusOS Platform Intelligence™

    Evaluates architectural fitness of the repository.
    This is the first practical step toward a self-describing platform.
    """

    IGNORED_DIRS = {
        ".git",
        ".venv",
        "venv",
        "venv_backup",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
    }

    LARGE_FILE_LINE_THRESHOLD = 400

    def __init__(self, root: str = "."):
        self.root = Path(root)

    def scan_python_files(self):
        files = []

        for path in self.root.rglob("*.py"):
            if any(part in self.IGNORED_DIRS for part in path.parts):
                continue
            files.append(path)

        return files

    def detect_oversized_files(self, files):
        oversized = []

        for path in files:
            try:
                lines = path.read_text(errors="ignore").splitlines()
            except Exception:
                continue

            if len(lines) > self.LARGE_FILE_LINE_THRESHOLD:
                oversized.append(f"{path} ({len(lines)} lines)")

        return oversized

    def detect_duplicate_risk(self, files):
        names = {}

        for path in files:
            names.setdefault(path.name, []).append(str(path))

        risks = []

        for name, paths in names.items():
            if len(paths) >= 3:
                risks.append(f"{name}: {len(paths)} occurrences")

        return risks

    def evaluate(self) -> ArchitecturalFitnessReport:
        files = self.scan_python_files()

        subsystem_count = len(
            [
                p
                for p in self.root.iterdir()
                if p.is_dir() and p.name not in self.IGNORED_DIRS
            ]
        )

        oversized = self.detect_oversized_files(files)
        duplicate_risk = self.detect_duplicate_risk(files)

        score = 100.0
        score -= min(len(oversized) * 1.5, 25)
        score -= min(len(duplicate_risk) * 1.0, 20)

        score = max(score, 0.0)

        status = "PASS" if score >= 80 else "REVIEW"

        return ArchitecturalFitnessReport(
            subsystem_count=subsystem_count,
            python_file_count=len(files),
            oversized_files=oversized[:20],
            duplicate_risk=duplicate_risk[:20],
            score=round(score, 2),
            status=status,
        )
