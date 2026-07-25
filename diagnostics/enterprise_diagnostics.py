from qa.smoke_tests import SmokeTests
from release.build_manager import BuildManager
from startup.startup_verifier import StartupVerifier


class EnterpriseDiagnostics:
    """Enterprise Diagnostics™."""

    @staticmethod
    def run():
        return {
            "startup": StartupVerifier.verify(run_migrations=False),
            "smoke_tests": SmokeTests.run(),
            "manifest": BuildManager.generate_manifest("release_manifest.json"),
        }
