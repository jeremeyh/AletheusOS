from __future__ import annotations
import hashlib, json, os, shutil, tempfile
from pathlib import Path
from aletheus.mammoth.contracts.objects import MammothObjectMetadata, MammothRetentionClass
from aletheus.mammoth.contracts.providers import *
from aletheus.mammoth.validation.invariants import MammothInvariants

class MammothLocalDiskError(IOError): pass
def _metadata_from_dict(d: dict) -> MammothObjectMetadata:
    d = dict(d); d["retention_class"] = MammothRetentionClass(d["retention_class"])
    d["tags"] = tuple(d.get("tags", ()))
    return MammothObjectMetadata(**d)

class LocalDiskPersistenceProvider:
    provider_id = "mammoth.local-disk.v1"
    capabilities = MammothProviderCapabilities(
        atomic_write=True, delete=True, versioning=True, replication=False,
        durable_metadata=True, crash_recovery=True
    )

    def __init__(self, root: str | Path):
        self.root = Path(root).expanduser().resolve()
        self.objects = self.root / "objects"
        self.txn = self.root / ".transactions"
        self.objects.mkdir(parents=True, exist_ok=True)
        self.txn.mkdir(parents=True, exist_ok=True)
        self.recover()

    def _safe(self, p: Path) -> Path:
        r = p.resolve()
        if r != self.root and self.root not in r.parents:
            raise MammothLocalDiskError("path escapes provider root")
        return r

    def _version_dir(self, object_id: str, version_id: str) -> Path:
        MammothInvariants.validate_object_id(object_id)
        MammothInvariants.validate_version_id(version_id)
        return self._safe(self.objects / object_id / version_id)

    def put(self, request: MammothPutRequest) -> MammothPutResult:
        m = request.metadata
        MammothInvariants.validate_object_id(m.object_id)
        MammothInvariants.validate_version_id(m.version_id)
        digest = "sha256:" + hashlib.sha256(bytes(request.data)).hexdigest()
        if digest != m.content_digest or len(request.data) != m.size_bytes:
            raise MammothLocalDiskError("payload does not match canonical metadata")
        final = self._version_dir(m.object_id, m.version_id)
        if final.exists():
            existing = self.get(MammothGetRequest(m.object_id, m.version_id))
            if existing and existing.data == bytes(request.data) and existing.metadata == m:
                return MammothPutResult(self.provider_id, True, m.object_id, m.version_id, str(final))
            raise MammothLocalDiskError("immutable version collision")
        stage = Path(tempfile.mkdtemp(prefix="txn-", dir=self.txn))
        try:
            (stage/"payload.bin").write_bytes(bytes(request.data))
            (stage/"metadata.json").write_text(json.dumps(m.to_canonical_dict(), sort_keys=True, separators=(",",":")), encoding="utf-8")
            final.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stage, final)
            self._fsync_dir(final.parent)
            return MammothPutResult(self.provider_id, True, m.object_id, m.version_id, str(final))
        except Exception:
            shutil.rmtree(stage, ignore_errors=True); raise

    def get(self, request: MammothGetRequest) -> MammothGetResult | None:
        MammothInvariants.validate_object_id(request.object_id)
        if request.version_id is None:
            parent = self._safe(self.objects/request.object_id)
            if not parent.exists(): return None
            versions = sorted(p for p in parent.iterdir() if p.is_dir())
            if not versions: return None
            # Metadata sequence, not lexical version hash, determines latest.
            pairs = []
            for p in versions:
                try:
                    md = json.loads((p/"metadata.json").read_text(encoding="utf-8"))
                    pairs.append((int(md["version_sequence"]), p, md))
                except Exception: continue
            if not pairs: return None
            _, target, md = max(pairs, key=lambda x: x[0])
        else:
            target = self._version_dir(request.object_id, request.version_id)
            if not target.exists(): return None
            md = json.loads((target/"metadata.json").read_text(encoding="utf-8"))
        data = (target/"payload.bin").read_bytes()
        meta = _metadata_from_dict(md)
        digest = "sha256:" + hashlib.sha256(data).hexdigest()
        if digest != meta.content_digest or len(data) != meta.size_bytes:
            raise MammothLocalDiskError("stored object failed integrity verification")
        return MammothGetResult(self.provider_id, meta, data)

    def remove(self, request: MammothDeleteRequest) -> MammothDeleteResult:
        MammothInvariants.validate_object_id(request.object_id)
        target = self._safe(self.objects/request.object_id)
        if request.version_id is not None:
            target = self._version_dir(request.object_id, request.version_id)
        if not target.exists(): return MammothDeleteResult(self.provider_id, False)
        shutil.rmtree(target)
        return MammothDeleteResult(self.provider_id, True)

    def health(self) -> MammothProviderHealth:
        try:
            usage = shutil.disk_usage(self.root)
            probe = self.txn / ".health-probe"
            probe.write_bytes(b"MAMMOTH"); probe.unlink()
            return MammothProviderHealth(self.provider_id, True, usage.free, "read/write probe passed")
        except Exception as exc:
            return MammothProviderHealth(self.provider_id, False, None, str(exc))

    def recover(self) -> int:
        recovered = 0
        for p in self.txn.glob("txn-*"):
            if p.is_dir(): shutil.rmtree(p, ignore_errors=True); recovered += 1
        return recovered

    @staticmethod
    def _fsync_dir(p: Path) -> None:
        try:
            fd = os.open(p, os.O_RDONLY)
            try: os.fsync(fd)
            finally: os.close(fd)
        except OSError:
            pass
