from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class LocaleProfile:
    locale_id: str
    language_code: str
    country_code: str
    display_name: str
    native_name: str
    currency_code: str
    date_format: str
    time_format: str
    number_format: str
    direction: str = "ltr"
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_timestamp)

    def to_dict(self) -> dict[str, Any]:
        return {
            "locale_id": self.locale_id,
            "language_code": self.language_code,
            "country_code": self.country_code,
            "display_name": self.display_name,
            "native_name": self.native_name,
            "currency_code": self.currency_code,
            "date_format": self.date_format,
            "time_format": self.time_format,
            "number_format": self.number_format,
            "direction": self.direction,
            "enabled": self.enabled,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


@dataclass(slots=True)
class LocalizationContext:
    locale_id: str = "en-US"
    language_code: str = "en"
    country_code: str = "US"
    currency_code: str = "USD"
    timezone: str = "America/Chicago"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "locale_id": self.locale_id,
            "language_code": self.language_code,
            "country_code": self.country_code,
            "currency_code": self.currency_code,
            "timezone": self.timezone,
            "metadata": self.metadata,
        }
