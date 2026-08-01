from __future__ import annotations

import hashlib
import hmac
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .models import ReleaseManifest


class InstallerError(RuntimeError):
    """Base Genesis installer failure."""


class PreflightError(InstallerError):
    """A required preflight check failed."""


class IntegrityError(InstallerError):
    """Manifest, checksum, or signature validation failed."""


class InstallerEngine:
    """Atomic, resumable installer for declarative Genesis releases."""

    def __init__(self, repository: Path) -> None:
        self.repository = repository.resolve()
        self.state_root = self.repository / ".aletheus_installer/state"
        self.backup_root = self.repository / ".aletheus_install_backups"

    @staticmethod
    def sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    @staticmethod
    def sign_payload(payload: bytes, key: str) -> str:
        return hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()

    @staticmethod
    def verify_signature(payload: bytes, signature: str, key: str) -> bool:
        expected = InstallerEngine.sign_payload(payload, key)
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def run_command(
        command: list[str],
        *,
        cwd: Path,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        executable = shutil.which(command[0])
        if executable is None:
            raise PreflightError(f"Required command is unavailable: {command[0]}")
        process = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        result = {
            "command": command,
            "returncode": process.returncode,
            "stdout": process.stdout[-8000:],
            "stderr": process.stderr[-8000:],
        }
        if process.returncode != 0:
            joined = " ".join(command)
            raise PreflightError(f"Command failed ({joined}):\n{process.stderr}")
        return result

    def verify_repository(self) -> None:
        if not (self.repository / ".git").is_dir():
            raise PreflightError(f"Not a Git repository: {self.repository}")
        if not (self.repository / "aletheus").is_dir():
            raise PreflightError("Aletheus package root is missing.")

    def verify_dependencies(self, manifest: ReleaseManifest) -> None:
        missing = [
            dependency
            for dependency in manifest.dependencies
            if not (self.repository / dependency).exists()
        ]
        if missing:
            raise PreflightError("Missing dependencies: " + ", ".join(sorted(missing)))

    def verify_package_layout(self, manifest: ReleaseManifest) -> None:
        package = manifest.package_root
        required = [
            package / "aletheus/__init__.py",
            package / "aletheus/tooling/__init__.py",
        ]
        for target in manifest.targets:
            source = package / target.source
            if not source.exists():
                required.append(source)
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            raise PreflightError("Package layout is incomplete: " + ", ".join(missing))

    def verify_checksums(
        self,
        manifest: ReleaseManifest,
        checksums: dict[str, str],
    ) -> None:
        for relative, expected in checksums.items():
            path = manifest.package_root / relative
            if not path.is_file():
                raise IntegrityError(f"Missing package file: {relative}")
            actual = self.sha256(path)
            if actual != expected:
                raise IntegrityError(
                    f"Checksum mismatch for {relative}: {actual} != {expected}"
                )

    def stage(self, manifest: ReleaseManifest) -> Path:
        stage = Path(tempfile.mkdtemp(prefix=f"{manifest.release_id}-"))
        for target in manifest.targets:
            source = manifest.package_root / target.source
            destination = stage / target.destination
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)
        return stage

    def backup(self, manifest: ReleaseManifest) -> Path:
        backup = (
            self.backup_root
            / manifest.release_id
            / subprocess.check_output(
                ["date", "+%Y%m%d_%H%M%S"],
                text=True,
            ).strip()
        )
        backup.mkdir(parents=True, exist_ok=True)
        for target in manifest.targets:
            current = self.repository / target.destination
            if not current.exists():
                continue
            archived = backup / target.destination
            archived.parent.mkdir(parents=True, exist_ok=True)
            if current.is_dir():
                shutil.copytree(current, archived, dirs_exist_ok=True)
            else:
                shutil.copy2(current, archived)
        return backup

    def apply(self, manifest: ReleaseManifest, stage: Path) -> None:
        for target in manifest.targets:
            staged = stage / target.destination
            destination = self.repository / target.destination
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if destination.is_dir():
                    shutil.rmtree(destination)
                else:
                    destination.unlink()
            if staged.is_dir():
                shutil.copytree(staged, destination)
            else:
                temporary = destination.with_suffix(destination.suffix + ".tmp")
                shutil.copy2(staged, temporary)
                os.replace(temporary, destination)

    def rollback(self, manifest: ReleaseManifest, backup: Path) -> None:
        for target in manifest.targets:
            destination = self.repository / target.destination
            archived = backup / target.destination
            if destination.exists():
                if destination.is_dir():
                    shutil.rmtree(destination)
                else:
                    destination.unlink()
            if archived.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                if archived.is_dir():
                    shutil.copytree(archived, destination)
                else:
                    shutil.copy2(archived, destination)

    def install(
        self,
        manifest: ReleaseManifest,
        *,
        checksums: dict[str, str],
        dry_run: bool = False,
        resume: bool = True,
    ) -> dict[str, Any]:
        self.verify_repository()
        self.verify_dependencies(manifest)
        self.verify_package_layout(manifest)
        self.verify_checksums(manifest, checksums)

        state_path = self.state_root / f"{manifest.release_id}.json"
        if resume and state_path.is_file():
            prior = json.loads(state_path.read_text(encoding="utf-8"))
            if prior.get("status") == "installed":
                destinations = [
                    self.repository / target.destination for target in manifest.targets
                ]
                if all(path.exists() for path in destinations):
                    return prior

        stage = self.stage(manifest)
        try:
            if dry_run:
                return {
                    "release_id": manifest.release_id,
                    "status": "dry_run_complete",
                    "targets": [target.destination for target in manifest.targets],
                }

            backup = self.backup(manifest)
            try:
                self.apply(manifest, stage)
            except (OSError, ValueError, KeyError, InstallerError):
                self.rollback(manifest, backup)
                raise

            result = {
                "release_id": manifest.release_id,
                "version": manifest.version,
                "status": "installed",
                "backup": str(backup),
                "targets": [target.destination for target in manifest.targets],
            }
            self.state_root.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(result, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            return result
        finally:
            shutil.rmtree(stage, ignore_errors=True)
