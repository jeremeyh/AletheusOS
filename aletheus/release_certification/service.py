import subprocess

from aletheus.platform_verification import (
    PlatformVerificationReport,
    bootstrap_verification_registry,
)

from .models import ReleaseCertification


class ReleaseCertificationService:
    def certify(self) -> ReleaseCertification:
        registry = bootstrap_verification_registry()
        report = PlatformVerificationReport(results=registry.run_all())

        git = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
        )

        git_clean = git.stdout.strip() == ""
        approved = report.passed() and git_clean

        if approved:
            status = "GENESIS CERTIFIED"
            summary = "Platform verification passed and working tree is clean."
        else:
            status = "CERTIFICATION BLOCKED"
            summary = "Platform verification failed or working tree is not clean."

        return ReleaseCertification(
            approved=approved,
            status=status,
            health_score=report.health_score(),
            git_clean=git_clean,
            summary=summary,
        )
