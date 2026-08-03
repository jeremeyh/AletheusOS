import type { TelemetryState } from "../types";

export type Tensor12 = readonly [
  number, number, number, number,
  number, number, number, number,
  number, number, number, number,
];

export interface TensorProjection {
  curvature: number;
  phaseOrder: number;
  entropyHamiltonian: number;
  attraction: number;
  shear: number;
  harmonicContraction: number;
}

const clamp01 = (value: number): number =>
  Math.max(0, Math.min(1, value));

export function buildIntelligenceTensor(
  telemetry: TelemetryState,
): Tensor12 {
  return [
    telemetry.veracity,
    telemetry.consensus,
    telemetry.contradiction,
    telemetry.elasticity,
    telemetry.resonance,
    telemetry.fieldDensity,
    telemetry.entropy,
    telemetry.missionMass,
    telemetry.meantimeQuotient,
    telemetry.founderMode,
    telemetry.veracity * telemetry.consensus,
    telemetry.contradiction * telemetry.entropy,
  ] as const;
}

export function projectTensor(
  tensor: Tensor12,
): TensorProjection {
  const [
    veracity,
    consensus,
    contradiction,
    elasticity,
    resonance,
    density,
    entropy,
    missionMass,
    meantimeQuotient,
    founderMode,
    coherentEvidence,
    entropyShear,
  ] = tensor;

  const curvature = clamp01(
    0.28 * missionMass
      + 0.24 * coherentEvidence
      + 0.18 * density
      - 0.22 * contradiction,
  );

  const phaseOrder = clamp01(
    0.42 * density
      + 0.28 * resonance
      + 0.20 * consensus
      + 0.10 * veracity,
  );

  const entropyHamiltonian = clamp01(
    0.58 * entropy
      + 0.34 * contradiction
      + 0.08 * entropyShear,
  );

  const attraction = clamp01(
    resonance * consensus * (1 - contradiction),
  );

  const shear = clamp01(
    contradiction * (1 + entropy) * (1 - elasticity * 0.4),
  );

  const harmonicContraction = clamp01(
    attraction
      * (0.65 + 0.20 * meantimeQuotient + 0.15 * founderMode),
  );

  return {
    curvature,
    phaseOrder,
    entropyHamiltonian,
    attraction,
    shear,
    harmonicContraction,
  };
}
