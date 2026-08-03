import type { PhaseState, TelemetryState } from "../types";

export const clamp01 = (value: number): number =>
  Math.max(0, Math.min(1, value));

export function constitutionalResonance(
  veracity: number,
  consensus: number,
  contradiction: number,
): number {
  const contradictionGate = 1 - clamp01(contradiction / 0.24);
  return clamp01(
    (veracity * 0.52 + consensus * 0.48) * contradictionGate,
  );
}

export function phaseForDensity(density: number): PhaseState {
  if (density < 0.35) return "Nebular";
  if (density < 0.70) return "Fluid Reactive";
  if (density < 0.92) return "Quasi-Crystalline";
  return "Crystalline Solid";
}

export function practicalResonance(
  signalIntegrity: number,
  harmonicStability: number,
  constitutionalAlignment: number,
  contradiction: number,
): number {
  return clamp01(
    signalIntegrity * 0.30 +
      harmonicStability * 0.28 +
      constitutionalAlignment * 0.34 +
      (1 - clamp01(contradiction)) * 0.08,
  );
}

export function meantimeQuotient(
  progress: number,
  seconds: number,
  coherence: number,
  vitality: number,
): number {
  const usefulVelocity = progress / Math.max(seconds, 1);
  return clamp01(
    usefulVelocity *
      (0.55 * clamp01(coherence) + 0.45 * clamp01(vitality)),
  );
}

export function integratedFieldResonance(
  signal: readonly number[],
  noise: readonly number[],
  epsilon = 1e-6,
): number {
  const count = Math.max(1, Math.min(signal.length, noise.length));
  let sum = 0;
  for (let index = 0; index < count; index += 1) {
    sum += Math.abs(signal[index] ?? 0) /
      (Math.abs(noise[index] ?? 0) + epsilon);
  }
  return clamp01(sum / count / 10);
}

export const defaultTelemetry: TelemetryState = {
  veracity: 0.982,
  consensus: 0.947,
  contradiction: 0.061,
  elasticity: 0.72,
  resonance: 0.965,
  fieldDensity: 0.72,
  entropy: 0.17,
  missionMass: 0.86,
  founderMode: 0,
  meantimeQuotient: 0.913,
};
