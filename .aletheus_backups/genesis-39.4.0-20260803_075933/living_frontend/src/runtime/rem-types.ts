export type REMPhase =
  | "ambient"
  | "nucleating"
  | "condensing"
  | "stabilized"
  | "transforming"
  | "dissolving";

export interface REMParticle {
  x: number;
  y: number;
  velocityX: number;
  velocityY: number;
  anchorX: number;
  anchorY: number;
  coherence: number;
  size: number;
  charge: number;
  seed: number;
}

export interface REMRuntimeState {
  phase: REMPhase;
  coherence: number;
  targetCoherence: number;
  crystallized: boolean;
  particleCount: number;
  frameTimeMs: number;
  frameVarianceMs: number;
  meantimeQuotient: number;
  droppedFrameRatio: number;
}

export interface REMPointer {
  x: number;
  y: number;
  active: boolean;
}

export interface REMRuntimeConfiguration {
  particleCount: number;
  latticeStiffness: number;
  damping: number;
  brownianStrength: number;
  magneticStrength: number;
  magneticRadius: number;
  connectionRadius: number;
  targetFrameMs: number;
  seed: number;
}
