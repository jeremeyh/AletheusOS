export type ExperienceEngineId =
  | "evidence"
  | "knowledge"
  | "reason"
  | "memory"
  | "bias"
  | "risk"
  | "predictive"
  | "experience"
  | "governance";

export type InstrumentIdentity =
  | "aletheus-index"
  | "thorx"
  | `engine:${ExperienceEngineId}`;

export type ExperienceStatus =
  | "idle"
  | "healthy"
  | "attention"
  | "critical"
  | "unavailable";

export interface ExperienceIdentity {
  readonly id: string;
  readonly canonicalName: string;
  readonly displayName?: string;
  readonly instrumentIdentity?: InstrumentIdentity;
  readonly status?: ExperienceStatus;
}

export interface ExperienceCapability {
  readonly identity: ExperienceIdentity;
  readonly version: string;
  readonly description: string;
  readonly metadata?: Readonly<Record<string, unknown>>;
}


/**
 * Canonical reserved instrument display identities.
 *
 * These names are constitutionally reserved by AletheusOS
 * and may not be replaced by downstream applications.
 */
export const RESERVED_INSTRUMENT_DISPLAY_NAMES = {
  "aletheus-index": "Aletheus Index™",
  "thorx": "THORᵡ",
} as const;
