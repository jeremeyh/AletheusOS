import { useMemo } from "react";
import type { PhaseState, RiskState } from "../types";

export interface FieldBodyStyle {
  "--field-mass": number;
  "--field-elasticity": number;
  "--field-respiration": string;
  "--field-drift": string;
  "--field-risk-pressure": number;
}

const phaseMass: Record<PhaseState, number> = {
  Nebular: 0.58,
  "Fluid Reactive": 0.74,
  "Quasi-Crystalline": 0.9,
  "Crystalline Solid": 1,
};

const riskPressure: Record<RiskState, number> = {
  stable: 0.12,
  watch: 0.36,
  strong: 0.08,
  critical: 0.82,
};

export function useFieldBody(
  id: string,
  phase: PhaseState,
  elasticity: number,
  respirationSeconds: number,
  risk: RiskState,
): FieldBodyStyle {
  return useMemo(() => {
    const seed = Array.from(id).reduce(
      (total, character) => total + character.charCodeAt(0),
      0,
    );
    const drift = 2.5 + (seed % 7) * 0.45;

    return {
      "--field-mass": phaseMass[phase],
      "--field-elasticity": elasticity,
      "--field-respiration": `${respirationSeconds}s`,
      "--field-drift": `${drift}s`,
      "--field-risk-pressure": riskPressure[risk],
    };
  }, [elasticity, id, phase, respirationSeconds, risk]);
}
