import ast
from pathlib import Path

from .models import CompressionReport


CORE = Path("aletheus/runtime/core.py")


class RuntimeCompressionDashboard:

    ORIGINAL_CORE_LINES = 3572
    RESPONSIBILITIES_TOTAL = 12

    def current_lines(self):

        return len(
            CORE.read_text().splitlines()
        )

    def report(
        self,
        completed=2,
        health=100.0,
    ):

        return CompressionReport(
            original_lines=self.ORIGINAL_CORE_LINES,
            current_lines=self.current_lines(),
            responsibilities_total=self.RESPONSIBILITIES_TOTAL,
            responsibilities_complete=completed,
            platform_health=health,
        )
