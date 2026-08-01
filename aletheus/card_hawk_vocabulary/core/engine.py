from __future__ import annotations

import hashlib
import json
from typing import Any

from .models import VocabularyLibrary


class Engine:
    VERSION = "27.0.0"

    def describe(self, library: VocabularyLibrary) -> dict[str, Any]:
        payload = {
            "libraryId": library.library_id,
            "version": library.version,
            "termCount": len(library.terms),
            "mappingCount": len(library.mappings),
            "doctrine": {
                "platformLanguage": "HOW_INTELLIGENCE_WORKS",
                "applicationLanguage": "WHAT_INTELLIGENCE_ACCOMPLISHES",
                "experienceVocabulary": "HOW_HUMANS_NATURALLY_UNDERSTAND_IT",
            },
            "metadata": library.metadata,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        payload["signature"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return payload
