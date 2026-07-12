export type NimbleTheme = "light" | "dark" | "system";

export type NimbleDensity =
  | "comfortable"
  | "balanced"
  | "compact";

export type NimbleMotionPreference =
  | "full"
  | "reduced"
  | "system";

export type NimbleDisclosureLevel =
  | "summary"
  | "standard"
  | "complete";

export interface NimbleConfidence {
  readonly value: number;
  readonly label:
    | "unknown"
    | "low"
    | "moderate"
    | "high"
    | "verified";
  readonly basis?: string;
}

export interface NimbleProvenance {
  readonly sourceId: string;
  readonly sourceType: string;
  readonly label: string;
  readonly observedAt?: string;
}

export interface NimbleUncertainty {
  readonly known: boolean;
  readonly description: string;
  readonly material: boolean;
}

export interface NimbleReversibility {
  readonly reversible: boolean;
  readonly undoLabel?: string;
  readonly consequence?: string;
}

export interface NimbleTruthEnvelope {
  readonly state: string;
  readonly explanation: string;
  readonly confidence?: NimbleConfidence;
  readonly provenance?: readonly NimbleProvenance[];
  readonly uncertainty?: readonly NimbleUncertainty[];
  readonly reversibility: NimbleReversibility;
}

export interface NimbleApplicationIdentity {
  readonly id: string;
  readonly name: string;
  readonly displayName: string;
  readonly description: string;
  readonly accent?: string;
}

export interface NimblePreferences {
  readonly theme: NimbleTheme;
  readonly density: NimbleDensity;
  readonly motion: NimbleMotionPreference;
  readonly disclosure: NimbleDisclosureLevel;
}

export const NIMBLE_DOCTRINE =
  "Complex beneath. Clear above. Alive throughout." as const;

export * from "./experience";
