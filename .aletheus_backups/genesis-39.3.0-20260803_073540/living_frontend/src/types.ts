export type PhaseState =
  | "Nebular"
  | "Fluid Reactive"
  | "Quasi-Crystalline"
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

export interface LoudnessTelemetry {
  shortTerm: number;
  integrated: number;
  momentary: number;
  truePeak: number;
  range: number;
}

export interface MetrologySnapshot {
  timestamp: number;
  loudness: LoudnessTelemetry;
  phaseCorrelation: number;
  stereoWidth: number;
  practicalResonance: number;
  meantimeQuotient: number;
  harmonicStability: number;
  signalIntegrity: number;
  noiseFloor: number;
  fft: readonly number[];
  channels: readonly number[];
}

export interface MagneticVector {
  x: number;
  y: number;
  velocityX: number;
  velocityY: number;
  accelerationX: number;
  accelerationY: number;
}
