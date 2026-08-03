import { useEffect, useMemo, useRef } from "react";
import { LIGHTSEngine } from "../runtime/lights-engine";
import {
  buildIntelligenceTensor,
  projectTensor,
} from "../runtime/tensor-field";
import type { TelemetryState } from "../types";

export function LIGHTSField({
  telemetry,
}: {
  telemetry: TelemetryState;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const engineRef = useRef<LIGHTSEngine | null>(null);

  const tensorProjection = useMemo(
    () => projectTensor(
      buildIntelligenceTensor(telemetry),
    ),
    [telemetry],
  );

  const emergence = Math.max(
    0,
    Math.min(
      1,
      (telemetry.resonance - 0.88) / 0.10,
    ),
  ) * Math.max(
    0,
    Math.min(
      1,
      (telemetry.consensus - 0.90) / 0.07,
    ),
  ) * (
    1 - Math.max(
      0,
      Math.min(
        1,
        telemetry.contradiction / 0.16,
      ),
    )
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    try {
      const engine = new LIGHTSEngine(canvas);
      engineRef.current = engine;
      engine.start();

      const resize = () => engine.resize();
      window.addEventListener("resize", resize);

      return () => {
        window.removeEventListener("resize", resize);
        engine.stop();
      };
    } catch (error) {
      console.error(
        "LIGHTS tensor field unavailable:",
        error,
      );
    }
  }, []);

  useEffect(() => {
    engineRef.current?.updateTelemetry({
      veracity: telemetry.veracity,
      consensus: telemetry.consensus,
      contradiction: telemetry.contradiction,
      elasticity: telemetry.elasticity,
      fieldDensity: telemetry.fieldDensity,
      resonance: telemetry.resonance,
      founderMode: telemetry.founderMode,
      curvature: tensorProjection.curvature,
      phaseOrder: tensorProjection.phaseOrder,
      entropyHamiltonian:
        tensorProjection.entropyHamiltonian,
      attraction: tensorProjection.attraction,
      shear: tensorProjection.shear,
    });
  }, [telemetry, tensorProjection]);

  return (
    <div
      className="lights-field-stack"
      style={{
        "--principle-x-emergence": emergence,
        "--tensor-curvature":
          tensorProjection.curvature,
        "--tensor-shear": tensorProjection.shear,
      } as React.CSSProperties}
      aria-hidden="true"
    >
      <canvas
        ref={canvasRef}
        className="lights-field"
      />

      <div className="principle-x-attractor">
        <div className="principle-x-attractor__halo" />
        <img
          src="/aletheusos-canonical-mark.jpeg"
          alt=""
          className="principle-x-attractor__mark"
        />
        <span className="principle-x-attractor__orbit principle-x-attractor__orbit--a" />
        <span className="principle-x-attractor__orbit principle-x-attractor__orbit--b" />
      </div>

      <div className="tensor-lensing tensor-lensing--a" />
      <div className="tensor-lensing tensor-lensing--b" />
    </div>
  );
}
