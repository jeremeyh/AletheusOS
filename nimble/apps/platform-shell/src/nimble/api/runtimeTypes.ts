import type {
  NimbleConfidence,
  NimbleProvenance,
  NimbleTruthEnvelope,
  NimbleUncertainty,
} from "@aletheus/nimble-core";

export type RuntimeHealthState =
  | "healthy"
  | "degraded"
  | "unavailable"
  | "unknown";

export interface RuntimeCheck {
  readonly id: string;
  readonly name: string;
  readonly state: RuntimeHealthState;
  readonly detail: string;
  readonly latencyMs?: number;
  readonly checkedAt: string;
}

export interface RuntimeHealthSnapshot {
  readonly state: RuntimeHealthState;
  readonly summary: string;
  readonly passingChecks: number;
  readonly totalChecks: number;
  readonly warningCount: number;
  readonly checks: readonly RuntimeCheck[];
  readonly truth: NimbleTruthEnvelope;
}

export interface RuntimeMission {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly state:
    | "planned"
    | "active"
    | "blocked"
    | "complete";
  readonly progress: number;
  readonly confidence?: NimbleConfidence;
  readonly provenance?: readonly NimbleProvenance[];
  readonly uncertainty?: readonly NimbleUncertainty[];
}

export interface RuntimeOverview {
  readonly health: RuntimeHealthSnapshot;
  readonly missions: readonly RuntimeMission[];
  readonly generatedAt: string;
}
