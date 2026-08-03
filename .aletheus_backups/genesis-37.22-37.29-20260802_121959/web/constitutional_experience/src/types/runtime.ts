export type VeracityPhase = "nebular" | "fluid" | "quasi-crystalline" | "crystalline";

export interface SceneNode {
  id: string;
  x: number;
  y: number;
  z: number;
  mass: number;
  veracity: number;
  tension: number;
}

export interface InstrumentDefinition {
  id: string;
  title: string;
  minWidth: number;
  minHeight: number;
  founderOnly?: boolean;
  telemetryStreams?: string[];
}

export interface RuntimeTelemetry {
  timestamp: number;
  fps: number;
  frameTimeMs: number;
  gpuQueueDepth: number;
  wasmStepMs: number;
  meantimeQuotient: number;
}
