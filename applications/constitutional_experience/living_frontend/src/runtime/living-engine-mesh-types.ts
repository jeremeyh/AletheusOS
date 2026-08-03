export type LivingEngineId =
  | "sdf-optics"
  | "predictive-intent"
  | "thermal-field"
  | "biological-rhythm"
  | "spatial-layout"
  | "constraint-physics"
  | "audio-haptics"
  | "reactive-graph";

export type EngineHealth = "inactive" | "nominal" | "degraded" | "faulted";

export interface EngineTelemetry {
  id: LivingEngineId;
  health: EngineHealth;
  active: boolean;
  latencyMs: number;
  load: number;
  confidence: number;
  detail: string;
}

export interface LivingEngineMeshSnapshot {
  timestamp: number;
  engines: readonly EngineTelemetry[];
  totalLoad: number;
  practicalResonance: number;
  preHydrationConfidence: number;
  thermalPressure: number;
  biologicalCoherence: number;
}
