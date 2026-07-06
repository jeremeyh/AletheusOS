from __future__ import annotations

import ast
import json
import shutil
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from watch_tower.models.finding import WatchTowerFinding


class WatchTowerEngine:
    """
    Watch Tower™
    Structural integrity, architecture, and repair guardian for AletheusOS.

    Modes:
    - scan: report only
    - repair: safe repairs only
    """

    VERSION = "1.0.0"

    SAFE_DELETE_NAMES = {
        ".DS_Store",
    }

    SAFE_DELETE_DIRS = {
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }

    REQUIRED_ROOT_FILES = [
        "README.md",
        "VERSION",
        "CHANGELOG.md",
    ]

    REQUIRED_ROOT_DIRS = [
        "aletheus",
        "cardhawk",
        "watch_tower",
        "tools",
        "tests",
    ]

    SUSPICIOUS_NAMES = [
        "_ _init_ _ .py",
        "...",
        "portfolio_enine.py",
    ]

    def __init__(self, root: str | Path = "."):
        self.root = Path(root).resolve()
        self.findings: list[WatchTowerFinding] = []
        self.repairs: list[str] = []

    def scan(self) -> dict:
        self.findings = []
        self.repairs = []

        self._check_root()
        self._check_required_files()
        self._check_required_dirs()
        self._check_suspicious_files()
        self._check_cache_artifacts()
        self._check_missing_init_files()
        self._check_python_syntax()
        self._check_version_alignment()
        self._check_duplicate_architecture_markers()
        self._check_principle_x()

        return self._result()

    def repair(self) -> dict:
        self.scan()

        for path in self.root.rglob("*"):
            if self._is_ignored(path):
                continue

            if path.name in self.SAFE_DELETE_NAMES and path.exists():
                path.unlink()
                self.repairs.append(f"Removed file: {self._rel(path)}")

            if path.is_dir() and path.name in self.SAFE_DELETE_DIRS:
                shutil.rmtree(path)
                self.repairs.append(f"Removed directory: {self._rel(path)}")

        for directory in self.root.rglob("*"):
            if self._is_ignored(directory):
                continue
            if not directory.is_dir():
                continue
            if self._should_have_init(directory):
                init_file = directory / "__init__.py"
                if not init_file.exists():
                    init_file.write_text('"""AletheusOS package."""\n', encoding="utf-8")
                    self.repairs.append(f"Created: {self._rel(init_file)}")

        self.scan()
        return self._result()

    def write_reports(self, output_dir: str | Path = "reports/watch_tower") -> dict:
        result = self._result()
        out = self.root / output_dir
        out.mkdir(parents=True, exist_ok=True)

        json_path = out / "watch_tower_report.json"
        md_path = out / "watch_tower_report.md"

        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        md_path.write_text(self._markdown(result), encoding="utf-8")

        return {
            "json": str(json_path),
            "markdown": str(md_path),
        }

    def _check_root(self):
        if not self.root.exists():
            self._finding(
                "ROOT_MISSING",
                "critical",
                "Project root missing",
                f"Root does not exist: {self.root}",
                str(self.root),
            )

    def _check_required_files(self):
        for name in self.REQUIRED_ROOT_FILES:
            path = self.root / name
            if not path.exists():
                self._finding(
                    "REQUIRED_FILE_MISSING",
                    "high",
                    "Required root file missing",
                    f"Missing required file: {name}",
                    name,
                    repairable=False,
                )

    def _check_required_dirs(self):
        for name in self.REQUIRED_ROOT_DIRS:
            path = self.root / name
            if not path.exists():
                self._finding(
                    "REQUIRED_DIR_MISSING",
                    "high",
                    "Required root directory missing",
                    f"Missing required directory: {name}",
                    name,
                    repairable=False,
                )

    def _check_suspicious_files(self):
        for suspicious in self.SUSPICIOUS_NAMES:
            for path in self.root.rglob(suspicious):
                if self._is_ignored(path):
                    continue
                self._finding(
                    "SUSPICIOUS_FILE",
                    "medium",
                    "Suspicious malformed file detected",
                    f"Suspicious file or directory exists: {self._rel(path)}",
                    self._rel(path),
                    repairable=suspicious in {"_ _init_ _ .py", "..."},
                )

    def _check_cache_artifacts(self):
        for path in self.root.rglob("*"):
            if self._is_ignored(path):
                continue

            if path.name in self.SAFE_DELETE_NAMES:
                self._finding(
                    "CACHE_ARTIFACT",
                    "low",
                    "Disposable system artifact found",
                    f"Safe cleanup candidate: {self._rel(path)}",
                    self._rel(path),
                    repairable=True,
                )

            if path.is_dir() and path.name in self.SAFE_DELETE_DIRS:
                self._finding(
                    "CACHE_DIR",
                    "low",
                    "Disposable cache directory found",
                    f"Safe cleanup candidate: {self._rel(path)}",
                    self._rel(path),
                    repairable=True,
                )

    def _check_missing_init_files(self):
        for directory in self.root.rglob("*"):
            if self._is_ignored(directory):
                continue
            if not directory.is_dir():
                continue
            if self._should_have_init(directory):
                init_file = directory / "__init__.py"
                if not init_file.exists():
                    self._finding(
                        "INIT_MISSING",
                        "medium",
                        "Missing package initializer",
                        f"Python package appears to need __init__.py: {self._rel(directory)}",
                        self._rel(directory),
                        repairable=True,
                    )

    def _check_python_syntax(self):
        for path in self.root.rglob("*.py"):
            if self._is_ignored(path):
                continue
            try:
                ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
            except SyntaxError as exc:
                self._finding(
                    "PYTHON_SYNTAX_ERROR",
                    "critical",
                    "Python syntax error",
                    f"{exc.msg} at line {exc.lineno}",
                    self._rel(path),
                    repairable=False,
                )

    def _check_version_alignment(self):
        version_file = self.root / "VERSION"
        runtime_core = self.root / "aletheus/runtime/core.py"

        if not version_file.exists() or not runtime_core.exists():
            return

        version = version_file.read_text(encoding="utf-8", errors="ignore").strip()
        text = runtime_core.read_text(encoding="utf-8", errors="ignore")

        if version and version not in text:
            self._finding(
                "VERSION_DRIFT",
                "medium",
                "VERSION drift detected",
                f"VERSION file says {version}, but aletheus/runtime/core.py does not appear to expose that version.",
                "VERSION",
                repairable=False,
            )

    def _check_duplicate_architecture_markers(self):
        markers = [
            ("plugins", "plugins_v3"),
            ("planning", "planning_v2"),
            ("missions_v2", "mission"),
            ("workflows_v2", "workflow_v3"),
            ("eventbus", "event_bus"),
        ]

        for left, right in markers:
            left_path = self.root / left
            right_path = self.root / right

            if left_path.exists() and right_path.exists():
                self._finding(
                    "ARCHITECTURE_DUPLICATE_MARKER",
                    "medium",
                    "Potential duplicate architecture packages",
                    f"Both {left} and {right} exist. Confirm canonical ownership before deleting either.",
                    f"{left}, {right}",
                    repairable=False,
                )

    def _check_principle_x(self):
        hits = []
        for path in self.root.rglob("*.py"):
            if self._is_ignored(path):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "Principle X" in text or "principle_x" in text or "Reciprocity Principle" in text:
                hits.append(self._rel(path))

        for path in self.root.rglob("*.md"):
            if self._is_ignored(path):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "Principle X" in text or "principle_x" in text or "Reciprocity Principle" in text:
                hits.append(self._rel(path))

        if not hits:
            self._finding(
                "PRINCIPLE_X_MISSING",
                "medium",
                "Principle X not detected",
                "No Principle X / principle_x / Reciprocity Principle reference was found in scanned source or docs.",
                "",
                repairable=False,
            )

    def _should_have_init(self, directory: Path) -> bool:
        if directory.name.startswith("."):
            return False

        if directory.name in {
            "venv",
            "__pycache__",
            ".git",
            "reports",
            "logs",
            "runtime_state",
            "uploads",
            "exports",
            "vault",
            "data",
            "sample_data",
            "datasets",
        }:
            return False

        if any(part in {"venv", ".git", "__pycache__", "reports", "logs"} for part in directory.parts):
            return False

        return any(child.suffix == ".py" for child in directory.iterdir() if child.is_file())

    def _is_ignored(self, path: Path) -> bool:
        ignored_parts = {
            ".git",
            "venv",
            ".Trash",
            "node_modules",
            "__pycache__",
        }
        return any(part in ignored_parts for part in path.parts)

    def _finding(
        self,
        code: str,
        severity: str,
        title: str,
        message: str,
        path: str = "",
        repairable: bool = False,
    ):
        self.findings.append(
            WatchTowerFinding(
                code=code,
                severity=severity,
                title=title,
                message=message,
                path=path,
                repairable=repairable,
                created_at=datetime.utcnow().isoformat(),
            )
        )

    def _result(self) -> dict:
        counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

        for finding in self.findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1

        score = 100
        score -= counts["critical"] * 25
        score -= counts["high"] * 10
        score -= counts["medium"] * 4
        score -= counts["low"] * 1
        score = max(score, 0)

        status = "healthy"
        if counts["critical"]:
            status = "critical"
        elif counts["high"]:
            status = "degraded"
        elif counts["medium"]:
            status = "watching"

        return {
            "watch_tower": {
                "version": self.VERSION,
                "root": str(self.root),
                "generated_at": datetime.utcnow().isoformat(),
                "status": status,
                "score": score,
                "counts": counts,
                "repairs": self.repairs,
                "findings": [f.to_dict() for f in self.findings],
            }
        }

    def _markdown(self, result: dict) -> str:
        wt = result["watch_tower"]

        lines = [
            "# Watch Tower™ Report",
            "",
            f"Generated: {wt['generated_at']}",
            f"Root: `{wt['root']}`",
            f"Status: **{wt['status']}**",
            f"Score: **{wt['score']}**",
            "",
            "## Counts",
            "",
        ]

        for key, value in wt["counts"].items():
            lines.append(f"- {key}: {value}")

        lines.append("")
        lines.append("## Repairs")
        lines.append("")

        if wt["repairs"]:
            for repair in wt["repairs"]:
                lines.append(f"- {repair}")
        else:
            lines.append("- None")

        lines.append("")
        lines.append("## Findings")
        lines.append("")

        if not wt["findings"]:
            lines.append("- No findings.")
        else:
            for item in wt["findings"]:
                lines.append(
                    f"- **[{item['severity']}] {item['code']}** — {item['title']} — {item['message']} `{item.get('path', '')}`"
                )

        lines.append("")
        return "\n".join(lines)

    def _rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except ValueError:
            return str(path)
