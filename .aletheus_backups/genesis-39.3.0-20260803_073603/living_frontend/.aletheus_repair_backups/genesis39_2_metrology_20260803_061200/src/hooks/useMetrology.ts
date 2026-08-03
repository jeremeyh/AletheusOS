import { useEffect, useRef, useState } from "react";
import {
  QuantumMetrologyEngine,
  type MetrologySnapshot,
} from "../runtime/quantum-metrology-engine";
import type { LIGHTSTelemetry } from "../runtime/lights-engine";

export function useMetrology(telemetry: LIGHTSTelemetry) {
  const engineRef = useRef<QuantumMetrologyEngine | null>(null);

  if (!engineRef.current) {
    engineRef.current = new QuantumMetrologyEngine({
      bins: 52,
      refreshMs: 120,
    });
  }

  const [snapshot, setSnapshot] = useState<MetrologySnapshot>(() =>
    engineRef.current!.sample(telemetry, 0)
  );

  useEffect(() => {
    const started = performance.now();

    const timer = window.setInterval(() => {
      const elapsedSeconds = (performance.now() - started) / 1000;

      setSnapshot(
        engineRef.current!.sample(telemetry, elapsedSeconds)
      );
    }, 120);

    return () => window.clearInterval(timer);
  }, [telemetry]);

  return snapshot;
}
