export type PhaseState =
  | "Nebular"
  | "Fluid Reactive"
  | "Quasi-Penrose"
  | "Crystalline Solid";

export type RiskState =
  | "stable"
  | "watch"
  | "strong"
  | "critical";

export interface TelemetryState {
  veracity: number;
  consensus: number;
  contradiction: number;
  elasticity: number;
  resonance: number;
  fieldDensity: number;
  entropy: number;
  missionMass: number;
  founderMode: number;
  meantimeQuotient: number;
}

export interface InstrumentDefinition {
  id: string;
  title: string;
  metric: string;
  value: number;
  accent: string;
  risk: RiskState;
  detail: string;
}
