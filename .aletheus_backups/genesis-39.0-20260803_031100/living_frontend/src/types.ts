export type PhaseState =
  | "Nebular"
  | "Fluid Reactive"
  | "Quasi-Crystalline"
  | "Crystalline Solid";

export type RiskState = "stable" | "watch" | "strong";

export interface InstrumentDefinition {
  id: string;
  title: string;
  metric: string;
  value: number;
  accent: string;
  risk: RiskState;
  detail: string;
}
