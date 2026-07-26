"""
Module entry point.

Enables:

    python -m tools.maintenance.ruf012
"""

from __future__ import annotations

import sys

from tools.maintenance.ruf012.cli import main

if __name__ == "__main__":
    sys.exit(main())
