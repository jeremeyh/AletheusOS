import type { RuntimeSignal, VeracityPhase } from "../types.js";

export const clamp01 = (value: number): number => Math.min(1, Math.max(0, value));

export function informationMass(signal: RuntimeSignal): number {
  return Math.max(0, signal.value) * clamp01(signal.provenance) * clamp01(signal.consensus);
}

export function cognitiveDensity(systemUtility: number, intentVelocity: number, cognitiveLoad: number): number {
  const numerator = 0.56 * clamp01(systemUtility) + 0.44 * clamp01(intentVelocity);
  const denominator = 0.85 * clamp01(cognitiveLoad) + 0.12;
  return Math.min(1, Math.max(0.18, numerator / denominator));
}

export function veracityPhase(confidence: number): VeracityPhase {
  if (confidence < 0.6) return "nebular";
  if (confidence < 0.85) return "fluid";
  if (confidence < 0.98) return "quasi";
  return "crystalline";
}

export function contradictionShear(a: RuntimeSignal, b: RuntimeSignal): number {
  const confidenceWeight = (clamp01(a.confidence) + clamp01(b.confidence)) / 2;
  const valueDistance = Math.abs(a.value - b.value) / Math.max(1, Math.abs(a.value), Math.abs(b.value));
  return clamp01(valueDistance * confidenceWeight * (0.5 + 0.5 * Math.max(a.contradiction, b.contradiction)));
}

export function respiration(timeSeconds: number, hz = 0.15): number {
  return 0.5 + 0.5 * Math.sin(Math.PI * 2 * hz * timeSeconds);
}

export function meantimeQuotient(latencyMs: number, coherence: number, vitality: number): number {
  const target = 16.67;
  const practical = 0.55 * clamp01(coherence) + 0.45 * clamp01(vitality);
  return clamp01(practical * (target / Math.max(target, latencyMs)));
}
