from __future__ import annotations
import json, os, uuid
from dataclasses import asdict
from pathlib import Path
from types import MappingProxyType
from typing import Iterable
from aletheus.mammoth.serialization.canonical import canonical_json_bytes
from .digests import MammothDigest
from .model import EvidenceEventType, MammothEvidenceRecord, ChainVerificationResult

GENESIS_HASH = "sha256:" + ("0" * 64)

class MammothProvenanceLedger:
    """
    Durable append-only evidence chain.

    Mammoth owns integrity/provenance evidence material.
    This ledger does not sign releases, issue RAF certificates, or resolve signing authority.
    """

    def __init__(self, ledger_path: str | Path):
        self.ledger_path = Path(ledger_path).expanduser().resolve()
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.touch()
            self._fsync_file(self.ledger_path)
            self._fsync_dir(self.ledger_path.parent)

    @staticmethod
    def _record_hash_payload(record: dict) -> dict:
        payload = dict(record)
        payload.pop("evidence_hash", None)
        payload["attributes"] = dict(sorted((payload.get("attributes") or {}).items()))
        return payload

    @classmethod
    def _compute_record_hash(cls, record: dict) -> str:
        return MammothDigest.canonical_sha256(cls._record_hash_payload(record))

    def _read_raw(self) -> list[dict]:
        rows: list[dict] = []
        with self.ledger_path.open("r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    raw = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"invalid provenance ledger JSON at line {lineno}") from exc
                rows.append(raw)
        return rows

    def records(self) -> tuple[MammothEvidenceRecord, ...]:
        out = []
        for raw in self._read_raw():
            out.append(MammothEvidenceRecord(
                sequence=int(raw["sequence"]),
                event_id=str(raw["event_id"]),
                event_type=EvidenceEventType(raw["event_type"]),
                object_id=str(raw["object_id"]),
                version_id=str(raw["version_id"]),
                content_digest=str(raw["content_digest"]),
                metadata_digest=str(raw["metadata_digest"]),
                previous_evidence_hash=str(raw["previous_evidence_hash"]),
                evidence_hash=str(raw["evidence_hash"]),
                occurred_at_iso=str(raw["occurred_at_iso"]),
                actor_capability=str(raw["actor_capability"]),
                authority_ref=raw.get("authority_ref"),
                attributes=MappingProxyType(dict(raw.get("attributes") or {})),
            ))
        return tuple(out)

    def append(
        self,
        *,
        event_type: EvidenceEventType,
        object_id: str,
        version_id: str,
        content_digest: str,
        metadata_digest: str,
        occurred_at_iso: str,
        actor_capability: str,
        authority_ref: str | None = None,
        attributes: dict[str, str] | None = None,
    ) -> MammothEvidenceRecord:
        existing = self.records()
        previous_hash = existing[-1].evidence_hash if existing else GENESIS_HASH
        sequence = len(existing) + 1
        raw = {
            "sequence": sequence,
            "event_id": "mev-" + uuid.uuid4().hex,
            "event_type": event_type.value,
            "object_id": object_id,
            "version_id": version_id,
            "content_digest": content_digest,
            "metadata_digest": metadata_digest,
            "previous_evidence_hash": previous_hash,
            "occurred_at_iso": occurred_at_iso,
            "actor_capability": actor_capability,
            "authority_ref": authority_ref,
            "attributes": dict(sorted((attributes or {}).items())),
        }
        raw["evidence_hash"] = self._compute_record_hash(raw)
        line = canonical_json_bytes(raw).decode("utf-8") + "\n"
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
        self._fsync_dir(self.ledger_path.parent)
        return self.records()[-1]

    def verify(self) -> ChainVerificationResult:
        try:
            rows = self._read_raw()
        except Exception as exc:
            return ChainVerificationResult(False, 0, GENESIS_HASH, 1, str(exc))
        previous = GENESIS_HASH
        for idx, raw in enumerate(rows, 1):
            if raw.get("sequence") != idx:
                return ChainVerificationResult(False, len(rows), previous, idx, "non-contiguous sequence")
            if raw.get("previous_evidence_hash") != previous:
                return ChainVerificationResult(False, len(rows), previous, idx, "previous hash mismatch")
            computed = self._compute_record_hash(raw)
            if raw.get("evidence_hash") != computed:
                return ChainVerificationResult(False, len(rows), previous, idx, "evidence hash mismatch")
            previous = computed
        return ChainVerificationResult(True, len(rows), previous)

    def recover_and_verify(self) -> ChainVerificationResult:
        """
        Recovery is verification-first. No damaged evidence is silently rewritten.
        Invalid chains fail closed and remain untouched for investigation.
        """
        return self.verify()

    @staticmethod
    def _fsync_file(path: Path) -> None:
        with path.open("rb") as f:
            os.fsync(f.fileno())

    @staticmethod
    def _fsync_dir(path: Path) -> None:
        try:
            fd = os.open(path, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        except OSError:
            pass
