#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$PROJECT_ROOT/.aletheus_repair_backups/genesis39_2_metrology_$STAMP"

echo "============================================================"
echo "AletheusOS Genesis 39.2 — Metrology Integration Repair"
echo "============================================================"

[[ -f package.json ]] || {
  echo "ERROR: package.json not found at $PROJECT_ROOT"
  exit 1
}

[[ -f src/runtime/quantum-metrology-engine.ts ]] || {
  echo "ERROR: quantum-metrology-engine.ts not found"
  exit 1
}

[[ -f src/types.ts ]] || {
  echo "ERROR: src/types.ts not found"
  exit 1
}

mkdir -p \
  "$BACKUP_DIR/src/hooks" \
  "$BACKUP_DIR/src/runtime" \
  "$BACKUP_DIR/src"

if [[ -f src/hooks/useMetrology.ts ]]; then
  cp src/hooks/useMetrology.ts \
    "$BACKUP_DIR/src/hooks/useMetrology.ts"
fi

if [[ -f src/runtime/lights-engine.ts ]]; then
  cp src/runtime/lights-engine.ts \
    "$BACKUP_DIR/src/runtime/lights-engine.ts"
fi

if [[ -f src/App.tsx ]]; then
  cp src/App.tsx \
    "$BACKUP_DIR/src/App.tsx"
fi

echo "Backup created:"
echo "  $BACKUP_DIR"

mkdir -p src/hooks

cat > src/hooks/useMetrology.ts <<'EOF'
import { useEffect, useRef, useState } from "react";
import { QuantumMetrologyEngine } from "../runtime/quantum-metrology-engine";
import type {
  MetrologySnapshot,
  TelemetryState,
} from "../types";

/**
 * Connects the typed LIGHTS telemetry state to the deterministic
 * Genesis 39.2 Quantum Metrology Engine.
 *
 * The telemetry ref prevents the sampling interval from being
 * destroyed and recreated whenever React creates a new object identity.
 */
export function useMetrology(
  telemetry: TelemetryState,
  refreshMilliseconds = 120,
): MetrologySnapshot {
  const engineRef = useRef<QuantumMetrologyEngine | null>(null);
  const telemetryRef = useRef<TelemetryState>(telemetry);
  const startedAtRef = useRef<number>(performance.now());

  if (engineRef.current === null) {
    engineRef.current = new QuantumMetrologyEngine({
      fftBins: 52,
      channelCount: 6,
      smoothing: 0.82,
      seed: 3921,
    });
  }

  const [snapshot, setSnapshot] = useState<MetrologySnapshot>(() =>
    engineRef.current!.sample(telemetry, 0),
  );

  useEffect(() => {
    telemetryRef.current = telemetry;
  }, [
    telemetry.veracity,
    telemetry.consensus,
    telemetry.contradiction,
    telemetry.elasticity,
    telemetry.resonance,
    telemetry.fieldDensity,
    telemetry.entropy,
    telemetry.missionMass,
    telemetry.founderMode,
    telemetry.meantimeQuotient,
  ]);

  useEffect(() => {
    const sample = () => {
      const engine = engineRef.current;

      if (engine === null) {
        return;
      }

      const elapsedSeconds =
        (performance.now() - startedAtRef.current) / 1000;

      setSnapshot(
        engine.sample(
          telemetryRef.current,
          elapsedSeconds,
        ),
      );
    };

    sample();

    const timer = window.setInterval(
      sample,
      refreshMilliseconds,
    );

    return () => {
      window.clearInterval(timer);
    };
  }, [refreshMilliseconds]);

  return snapshot;
}
EOF

echo "✓ Replaced src/hooks/useMetrology.ts"

# Remove a malformed standalone backslash at the beginning of
# lights-engine.ts, while preserving all legitimate source content.
python3 <<'PY'
from pathlib import Path

path = Path("src/runtime/lights-engine.ts")

if path.exists():
    text = path.read_text(encoding="utf-8")

    if text.startswith("\\\n"):
        text = text[2:]
    elif text.startswith("\\\r\n"):
        text = text[3:]

    # Leading empty lines are harmless, but normalize the source file.
    text = text.lstrip("\r\n")

    path.write_text(text, encoding="utf-8")
PY

echo "✓ Normalized src/runtime/lights-engine.ts"

# Add explicit callback types only if the older untyped form remains.
python3 <<'PY'
from pathlib import Path

path = Path("src/App.tsx")
text = path.read_text(encoding="utf-8")

old = (
    "metrology.fft.slice(0, 44)"
    ".map((value, index) => ("
)

new = (
    "metrology.fft.slice(0, 44)"
    ".map((value: number, index: number) => ("
)

if old in text:
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print("✓ Added explicit FFT callback types in App.tsx")
else:
    print("✓ App.tsx FFT callback already typed or structurally updated")
PY

echo
echo "Verifying repaired hook:"
grep -n "engineRef\|fftBins\|channelCount\|TelemetryState" \
  src/hooks/useMetrology.ts

echo
echo "Running TypeScript validation..."
npm run check

echo
echo "Running production build..."
npm run build

echo
echo "============================================================"
echo "GENESIS 39.2 METROLOGY REPAIR PASSED"
echo "============================================================"
echo "Backup:"
echo "  $BACKUP_DIR"
echo
echo "Launch:"
echo "  npm run dev"
echo
echo "Open:"
echo "  http://localhost:3737"
