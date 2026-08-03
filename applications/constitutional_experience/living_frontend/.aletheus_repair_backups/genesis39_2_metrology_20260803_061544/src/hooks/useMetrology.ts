import { useEffect, useRef, useState } from "react";
import type { MetrologySnapshot, TelemetryState } from "../types";
import { QuantumMetrologyEngine } from "../runtime/quantum-metrology-engine";

export function useMetrology(
  telemetry: TelemetryState,
  refreshMilliseconds = 120,
): MetrologySnapshot {
  const engineRef = useRef<QuantumMetrologyEngine>();
  const startedAtRef = useRef(performance.now());

  if (!engineRef.current) {
    engineRef.current = new QuantumMetrologyEngine({
      fftBins: 52,
      channelCount: 6,
      smoothing: 0.82,
    });
  }

  const [snapshot, setSnapshot] = useState(() =>
    engineRef.current!.sample(telemetry, 0),
  );

  useEffect(() => {
    const timer = window.setInterval(() => {
      const elapsedSeconds =
        (performance.now() - startedAtRef.current) / 1000;
      setSnapshot(engineRef.current!.sample(telemetry, elapsedSeconds));
    }, refreshMilliseconds);

    return () => window.clearInterval(timer);
  }, [telemetry, refreshMilliseconds]);

  return snapshot;
}
