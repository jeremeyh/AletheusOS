"""
Scanner wrapper around the existing Genesis 11 analyzer.

This avoids maintaining two independent AST scanners.
"""

from __future__ import annotations

from pathlib import Path

# Reuse the working analyzer
import tools.maintenance.fix_ruf012 as analyzer


class RepositoryScanner:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()

    def scan(self):
        """
        Uses the existing analyzer implementation.

        Requires fix_ruf012.py to expose:

            scan_repository(root: Path) -> ScanSummary

        where the returned object contains:

            safe_candidates
            shared_candidates
            manual_candidates
            files_discovered/files_parsed
            syntax_failures
        """

        if not hasattr(analyzer, "scan_repository"):
            raise RuntimeError(
                "tools.maintenance.fix_ruf012.scan_repository() "
                "has not been implemented yet.\n\n"
                "Refactor the working analyzer into a reusable "
                "function before using this package."
            )

        return analyzer.scan_repository(self.root)
