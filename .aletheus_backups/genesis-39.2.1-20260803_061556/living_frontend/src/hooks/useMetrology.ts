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
