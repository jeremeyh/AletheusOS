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
    """Base installer failure."""


class PreflightError(InstallerError):
    """Preflight validation failed."""


class ChecksumError(InstallerError):
    """A package checksum did not match."""


class InstallerEngine:
    def __init__(self, repository: Path) -> None:
        self.repository = repository.resolve()
        self.state_root = self.repository / ".aletheus_installer"
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

    def resolve_dependencies(self, manifest: ReleaseManifest) -> None:
        missing = [
            dependency
            for dependency in manifest.dependencies
            if not (self.repository / dependency).exists()
        ]
        if missing:
            raise PreflightError(
                "Missing release dependencies: " + ", ".join(sorted(missing))
            )

    def verify_checksums(
        self,
        package_root: Path,
        checksums: dict[str, str],
    ) -> None:
        for relative, expected in checksums.items():
            path = package_root / relative
            if not path.is_file():
                raise ChecksumError(f"Missing package file: {relative}")
            actual = self.sha256(path)
            if actual != expected:
                raise ChecksumError(
                    f"Checksum mismatch for {relative}: {actual} != {expected}"
                )

    def run_preflight(
        self,
        manifest: ReleaseManifest,
        *,
        shellcheck_optional: bool = True,
    ) -> list[dict[str, Any]]:
        self.resolve_dependencies(manifest)
        results = []
        commands = [
            ["ruff", "check", "."],
            ["black", "--check", "."],
            ["pytest"],
            ["python", "-m", "compileall", "aletheus"],
        ]
        commands.extend(manifest.validation_commands)

        for command in commands:
            executable = shutil.which(command[0])
            if executable is None:
                raise PreflightError(
                    f"Required preflight tool is unavailable: {command[0]}"
                )
            process = subprocess.run(
                command,
                cwd=self.repository,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "command": command,
                    "returncode": process.returncode,
                    "stdout": process.stdout[-4000:],
                    "stderr": process.stderr[-4000:],
                }
            )
            if process.returncode != 0:
                raise PreflightError(f"Preflight command failed: {' '.join(command)}")

        shellcheck = shutil.which("shellcheck")
        if shellcheck:
            shell_scripts = sorted(manifest.package_root.parent.glob("*.sh"))
            if shell_scripts:
                process = subprocess.run(
                    [shellcheck, *(str(path) for path in shell_scripts)],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                results.append(
                    {
                        "command": ["shellcheck", *map(str, shell_scripts)],
                        "returncode": process.returncode,
                        "stdout": process.stdout[-4000:],
                        "stderr": process.stderr[-4000:],
                    }
                )
                if process.returncode != 0:
                    raise PreflightError("ShellCheck failed.")
        elif not shellcheck_optional:
            raise PreflightError("ShellCheck is required but unavailable.")

        return results

    def install(
        self,
        manifest: ReleaseManifest,
        *,
        checksums: dict[str, str],
        dry_run: bool = False,
        resume: bool = True,
    ) -> dict[str, Any]:
        self.verify_checksums(manifest.package_root, checksums)
        self.resolve_dependencies(manifest)

        state_path = self.state_root / f"{manifest.release_id}.json"
        if resume and state_path.is_file():
            prior = json.loads(state_path.read_text(encoding="utf-8"))
            if prior.get("status") == "installed":
                return prior

        stage = Path(tempfile.mkdtemp(prefix=f"{manifest.release_id}-"))
        backup = self.backup_root / manifest.release_id
        try:
            for relative in manifest.targets:
                source = manifest.package_root / relative
                destination = stage / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                elif source.is_file():
                    shutil.copy2(source, destination)
                else:
                    raise InstallerError(f"Missing staged target: {relative}")

            if dry_run:
                return {
                    "release_id": manifest.release_id,
                    "status": "dry_run_complete",
                    "targets": manifest.targets,
                }

            backup.mkdir(parents=True, exist_ok=True)
            for relative in manifest.targets:
                current = self.repository / relative
                if current.exists():
                    archived = backup / relative
                    archived.parent.mkdir(parents=True, exist_ok=True)
                    if current.is_dir():
                        shutil.copytree(
                            current,
                            archived,
                            dirs_exist_ok=True,
                        )
                    else:
                        shutil.copy2(current, archived)

            for relative in manifest.targets:
                staged = stage / relative
                target = self.repository / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                if staged.is_dir():
                    shutil.copytree(staged, target, dirs_exist_ok=True)
                else:
                    temporary = target.with_suffix(target.suffix + ".tmp")
                    shutil.copy2(staged, temporary)
                    os.replace(temporary, target)

            result = {
                "release_id": manifest.release_id,
                "version": manifest.version,
                "status": "installed",
                "targets": manifest.targets,
                "backup": str(backup),
            }
            self.state_root.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(result, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            return result
        except (OSError, ValueError, KeyError, InstallerError):
            self.rollback(manifest, backup)
            raise
        finally:
            shutil.rmtree(stage, ignore_errors=True)

    def rollback(self, manifest: ReleaseManifest, backup: Path) -> None:
        for relative in manifest.targets:
            target = self.repository / relative
            archived = backup / relative
            if archived.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                if archived.is_dir():
                    if target.exists():
                        shutil.rmtree(target)
                    shutil.copytree(archived, target)
                else:
                    shutil.copy2(archived, target)
            elif target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
