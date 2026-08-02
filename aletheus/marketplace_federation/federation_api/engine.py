from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, ClassVar

from .models import ApiRequest


class Engine:
    """Validate and authorize Marketplace Federation API requests.

    Genesis 31.15 provides the protected connector boundary through which
    approved external marketplaces and internal AletheusOS capabilities may
    invoke Marketplace Federation operations.

    Every request is treated as untrusted until it has passed:

    - connector identity validation;
    - operation normalization;
    - timestamp freshness validation;
    - nonce and replay-defense validation;
    - signature-presence validation;
    - schema validation;
    - SPARTAN security evaluation;
    - constitutional-policy evaluation;
    - audit and evidence requirements.

    This engine validates the request envelope. Cryptographic signature
    verification, nonce persistence, rate-limiting persistence, and connector
    policy resolution are delegated to the appropriate SPARTAN, cryptographic,
    registry, and evidence services at runtime.
    """

    VERSION: ClassVar[str] = "31.15.0"

    MAX_REQUEST_AGE_SECONDS: ClassVar[int] = 300
    MAX_FUTURE_SKEW_SECONDS: ClassVar[int] = 30

    SUPPORTED_OPERATIONS: ClassVar[frozenset[str]] = frozenset(
        {
            "ASSET_LOOKUP",
            "CANCEL_OFFER",
            "CANCEL_ORDER",
            "CREATE_LISTING",
            "CREATE_OFFER",
            "CREATE_ORDER",
            "CREATE_TRADE",
            "ESCROW_STATUS",
            "EVENT_PUBLISH",
            "EVENT_SUBSCRIBE",
            "INVENTORY_READ",
            "LISTING_READ",
            "MARKETPLACE_HEALTH",
            "OFFER_READ",
            "ORDER_READ",
            "PRICE_READ",
            "SETTLEMENT_STATUS",
            "TRADE_READ",
            "UPDATE_LISTING",
            "UPDATE_OFFER",
            "UPDATE_TRADE",
            "VAULT_STATUS",
        }
    )

    HIGH_RISK_OPERATIONS: ClassVar[frozenset[str]] = frozenset(
        {
            "CANCEL_ORDER",
            "CREATE_ORDER",
            "CREATE_TRADE",
            "UPDATE_TRADE",
        }
    )

    MUTATING_OPERATIONS: ClassVar[frozenset[str]] = frozenset(
        {
            "CANCEL_OFFER",
            "CANCEL_ORDER",
            "CREATE_LISTING",
            "CREATE_OFFER",
            "CREATE_ORDER",
            "CREATE_TRADE",
            "EVENT_PUBLISH",
            "UPDATE_LISTING",
            "UPDATE_OFFER",
            "UPDATE_TRADE",
        }
    )

    def validate(
        self,
        request: ApiRequest,
        *,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Validate a Marketplace Federation API request envelope.

        Args:
            request:
                Canonical API request envelope.
            now:
                Optional UTC-aware reference time used for deterministic tests.
                The current UTC time is used when omitted.

        Returns:
            A render-neutral validation contract consumed by the Federation API
            Shield, SPARTAN, connector runtime, and Marketplace Federation
            Orchestrator.

        Raises:
            TypeError:
                If the request or supplied reference time has an invalid type.
            ValueError:
                If required fields are missing, malformed, unsupported, stale,
                or outside the permitted clock-skew window.
        """

        self._validate_request_type(request)

        connector_id = self._require_text(
            request.connector_id,
            field_name="connector_id",
        )
        operation = self._normalize_operation(request.operation)
        nonce = self._require_text(
            request.nonce,
            field_name="nonce",
        )
        signature = self._require_text(
            request.signature,
            field_name="signature",
        )
        timestamp = self._parse_timestamp(request.timestamp)
        reference_time = self._resolve_reference_time(now)

        age_seconds = (reference_time - timestamp).total_seconds()

        if age_seconds > self.MAX_REQUEST_AGE_SECONDS:
            raise ValueError(
                "API request timestamp is stale. "
                f"Maximum age is {self.MAX_REQUEST_AGE_SECONDS} seconds."
            )

        if age_seconds < -self.MAX_FUTURE_SKEW_SECONDS:
            raise ValueError(
                "API request timestamp is too far in the future. "
                f"Maximum permitted future skew is "
                f"{self.MAX_FUTURE_SKEW_SECONDS} seconds."
            )

        high_risk = operation in self.HIGH_RISK_OPERATIONS
        mutating = operation in self.MUTATING_OPERATIONS

        return {
            "validator": {
                "name": "Marketplace Federation API Shield",
                "version": self.VERSION,
                "status": "VALIDATED",
            },
            "accepted": True,
            "decision": "ACCEPT_FOR_SECURITY_EVALUATION",
            "connectorId": connector_id,
            "operation": operation,
            "requestEnvelope": {
                "nonce": nonce,
                "timestamp": timestamp.isoformat(),
                "signaturePresent": bool(signature),
                "ageSeconds": round(age_seconds, 6),
            },
            "riskClassification": {
                "highRiskOperation": high_risk,
                "mutatingOperation": mutating,
                "stepUpAuthenticationRequired": high_risk,
                "dualControlEligible": high_risk,
            },
            "securityControls": {
                "connectorAuthenticationRequired": True,
                "signatureVerificationRequired": True,
                "nonceRegistrationRequired": True,
                "replayProtectionRequired": True,
                "schemaValidationRequired": True,
                "rateLimitingRequired": True,
                "tenantIsolationRequired": True,
                "leastPrivilegeRequired": True,
                "spartanEvaluationRequired": True,
                "constitutionalPolicyRequired": True,
                "evidenceCommitRequired": True,
                "conclaveIsolationOnFailure": True,
            },
            "transportPolicy": {
                "minimumTransport": "TLS_1_3",
                "mutualTlsPreferred": True,
                "plaintextTransportAllowed": False,
            },
            "cryptographicPolicy": {
                "requestSignatureRequired": True,
                "payloadHashRequired": mutating,
                "keyCustody": "HSM_OR_MANAGED_KMS",
                "atRestEncryption": "AES_256_GCM",
            },
            "federationDirectives": {
                "routeToConnectorRegistry": True,
                "routeToSpartan": True,
                "routeToConstitutionalGovernance": True,
                "routeToMarketplaceOrchestrator": True,
                "routeToSecurityEvidenceLedger": True,
            },
            "status": "VALIDATED",
        }

    def supports(self, operation: str) -> bool:
        """Return whether the supplied API operation is supported."""

        if not isinstance(operation, str):
            return False

        return operation.strip().upper() in self.SUPPORTED_OPERATIONS

    def describe_operation(self, operation: str) -> dict[str, Any]:
        """Describe the security profile of a supported operation."""

        normalized_operation = self._normalize_operation(operation)
        high_risk = normalized_operation in self.HIGH_RISK_OPERATIONS
        mutating = normalized_operation in self.MUTATING_OPERATIONS

        return {
            "operation": normalized_operation,
            "supported": True,
            "highRisk": high_risk,
            "mutating": mutating,
            "stepUpAuthenticationRequired": high_risk,
            "payloadHashRequired": mutating,
            "spartanEvaluationRequired": True,
            "constitutionalPolicyRequired": True,
            "auditRequired": True,
        }

    def validate_legacy(
        self,
        nonce: str,
        timestamp: str,
        signature: str,
        *,
        connector_id: str = "LEGACY_CONNECTOR",
        operation: str = "MARKETPLACE_HEALTH",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Validate the former positional request format.

        This compatibility method preserves the original Genesis 31.15 calling
        contract while routing validation through the canonical ApiRequest
        model.
        """

        request = ApiRequest(
            connector_id=connector_id,
            operation=operation,
            nonce=nonce,
            timestamp=timestamp,
            signature=signature,
        )

        return self.validate(request, now=now)

    def _normalize_operation(self, operation: str) -> str:
        normalized_operation = self._require_text(
            operation,
            field_name="operation",
        ).upper()

        if normalized_operation not in self.SUPPORTED_OPERATIONS:
            supported = ", ".join(sorted(self.SUPPORTED_OPERATIONS))
            raise ValueError(
                f"Unsupported Marketplace Federation API operation: "
                f"{operation}. Supported operations: {supported}"
            )

        return normalized_operation

    @staticmethod
    def _parse_timestamp(timestamp: str) -> datetime:
        timestamp_text = Engine._require_text(
            timestamp,
            field_name="timestamp",
        )

        try:
            parsed = datetime.fromisoformat(timestamp_text)
        except ValueError as exc:
            raise ValueError("timestamp must be a valid ISO-8601 datetime.") from exc

        if parsed.tzinfo is None:
            raise ValueError("timestamp must include an explicit timezone offset.")

        return parsed.astimezone(UTC)

    @staticmethod
    def _resolve_reference_time(now: datetime | None) -> datetime:
        if now is None:
            return datetime.now(UTC)

        if not isinstance(now, datetime):
            raise TypeError("now must be a datetime instance or None.")

        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware.")

        return now.astimezone(UTC)

    @staticmethod
    def _validate_request_type(request: ApiRequest) -> None:
        if not isinstance(request, ApiRequest):
            raise TypeError("request must be an ApiRequest instance.")

    @staticmethod
    def _require_text(value: str, *, field_name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")

        normalized = value.strip()

        if not normalized:
            raise ValueError(f"{field_name} cannot be empty.")

        return normalized
