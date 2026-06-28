"""
CardHawk OS™
Global Platform Constants
"""

from pathlib import Path

# ------------------------------------------------------------------
# Platform Identity
# ------------------------------------------------------------------

PLATFORM_NAME = "CardHawk OS™"
PLATFORM_CODENAME = "Repository Consolidation"

# ------------------------------------------------------------------
# Directory Structure
# ------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

ASSETS = ROOT / "assets"
DATA = ROOT / "data"
DATABASE = ROOT / "database"
DOCS = ROOT / "docs"
EXPORTS = ROOT / "exports"
UPLOADS = ROOT / "uploads"
LOGS = ROOT / "logs"
STORAGE = ROOT / "storage"
CACHE = STORAGE / "cache"

# ------------------------------------------------------------------
# Asset Categories
# ------------------------------------------------------------------

CARD = "Card"
MEMORABILIA = "Memorabilia"
FUNKO = "Funko"
BOBBLEHEAD = "Bobblehead"

# ------------------------------------------------------------------
# Intelligence Engines
# ------------------------------------------------------------------

ENGINE_THORX = "THORᵡ"
ENGINE_HAWK_AEYE = "Hawk A•Eye™"
ENGINE_SCOUT = "Continuous Scout™"
ENGINE_FOUNDER = "Founder AI™"

# ------------------------------------------------------------------
# Recommendation Actions
# ------------------------------------------------------------------

BUY = "BUY"
WATCH = "WATCH"
PASS = "PASS"
SELL = "SELL"
GRADE = "GRADE"

# ------------------------------------------------------------------
# Runtime
# ------------------------------------------------------------------

DEFAULT_CURRENCY = "USD"
DEFAULT_TIMEZONE = "UTC"

# ------------------------------------------------------------------
# Ensure Runtime Directories Exist
# ------------------------------------------------------------------

for directory in (
    LOGS,
    EXPORTS,
    UPLOADS,
    CACHE,
):
    directory.mkdir(parents=True, exist_ok=True)
