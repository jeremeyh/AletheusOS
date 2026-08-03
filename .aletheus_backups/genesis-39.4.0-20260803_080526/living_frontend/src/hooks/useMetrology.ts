import { useEffect, useRef, useState } from "react";
import type { MetrologySnapshot, TelemetryState } from "../types";
import { QuantumMetrologyEngine } from "../runtime/quantum-metrology-engine";

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
      seed: 3922,
    });
  }

  const [snapshot, setSnapshot] = useState<MetrologySnapshot>(() =>
    engineRef.current!.sample(telemetry, 0),
  );

  useEffect(() => {
    telemetryRef.current = telemetry;
  }, [telemetry]);

  useEffect(() => {
    const sample = (): void => {
      const engine = engineRef.current;
      if (engine === null) return;

      const elapsedSeconds =
        (performance.now() - startedAtRef.current) / 1000;

      setSnapshot(engine.sample(telemetryRef.current, elapsedSeconds));
    };

    sample();
    const timer = window.setInterval(sample, refreshMilliseconds);
    return () => window.clearInterval(timer);
  }, [refreshMilliseconds]);

  return snapshot;
}
