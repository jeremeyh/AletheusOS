from pathlib import Path

from .scanner import RepositoryScanner
from .writer import RepositoryWriter


class Runner:

    def run(self):

        root = Path.cwd()

        scanner = RepositoryScanner(root)

        result = scanner.scan()

        writer = RepositoryWriter(root)

        writer.apply(result.safe_candidates)

        print()
        print("=" * 72)
        print("Genesis 11 Safe RUF012")
        print("=" * 72)
        print(f"Safe candidates : {len(result.safe_candidates)}")
        print(f"Shared skipped  : {len(result.shared_candidates)}")
        print(f"Manual skipped  : {len(result.manual_candidates)}")
        print()
        print("Done.")
