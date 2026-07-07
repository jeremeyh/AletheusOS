from __future__ import annotations

from .models import PlatformVerificationReport


class PlatformVerificationReporter:
    def render(self, report: PlatformVerificationReport) -> str:
        lines = [
            "=" * 56,
            "ALETHEUSOS PLATFORM VERIFICATION",
            "=" * 56,
            "",
        ]

        for result in report.results:
            lines.append(f"{result.name:.<35}{result.status.value}")
            lines.append(f"  {result.summary}")
            if result.warnings:
                for warning in result.warnings:
                    lines.append(f"  WARN: {warning}")
            if result.errors:
                for error in result.errors:
                    lines.append(f"  ERROR: {error}")
            lines.append("")

        lines.extend([
            "-" * 56,
            f"Platform Health Score: {report.health_score()}%",
            f"Overall Status: {'PASS' if report.passed() else 'FAIL'}",
            "=" * 56,
        ])

        return "\n".join(lines)
