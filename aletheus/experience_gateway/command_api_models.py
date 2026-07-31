from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CommandPreviewRequestModel(BaseModel):
    command_id: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = None


class CommandAuthorizationRequestModel(BaseModel):
    preview_id: str = Field(min_length=1)


class CommandExecutionRequestModel(BaseModel):
    preview_id: str = Field(min_length=1)
    authorization_id: str | None = None
    idempotency_key: str | None = None


class CommandReversalRequestModel(BaseModel):
    execution_id: str = Field(min_length=1)
    reversal_token: str = Field(min_length=1)
