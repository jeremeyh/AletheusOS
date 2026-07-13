export type InstrumentStatus =
  | "initializing"
  | "healthy"
  | "attention"
  | "review"
  | "critical"
  | "unavailable";


export type InstrumentTrend =
  | "increasing"
  | "stable"
  | "declining"
  | "unknown";


export type ReservedInstrumentId =
  | "instrument.aletheus-index"
  | "instrument.thorx";


export type EngineInstrumentId =
  | "engine.evidence"
  | "engine.knowledge"
  | "engine.reason"
  | "engine.memory"
  | "engine.bias"
  | "engine.risk"
  | "engine.predictive";


export type InstrumentId =
  | ReservedInstrumentId
  | EngineInstrumentId
  | `application.${string}`;


export interface InstrumentTelemetryEntry {
  readonly id: string;
  readonly label: string;
  readonly value: string | number;
  readonly unit?: string;
}


export interface InstrumentTelemetry {
  readonly latencyMs?: number;
  readonly confidence?: number;
  readonly sourceCount?: number;
  readonly updatedAt: string;
  readonly warnings?: readonly string[];
  readonly notes?: readonly string[];
  readonly entries?: readonly InstrumentTelemetryEntry[];
}


export interface InstrumentState {
  readonly id: InstrumentId;
  readonly canonicalName: string;
  readonly displayName?: string;
  readonly value: number | string;
  readonly displayValue: string;
  readonly status: InstrumentStatus;
  readonly trend: InstrumentTrend;
  readonly confidence?: number;
  readonly telemetry: InstrumentTelemetry;
  readonly reserved: boolean;
  readonly metadata?: Readonly<Record<string, unknown>>;
}


export interface InstrumentationSnapshot {
  readonly schemaVersion: "1.0";
  readonly capturedAt: string;
  readonly instruments: readonly InstrumentState[];
}


export type InstrumentationListener = (
  snapshot: InstrumentationSnapshot,
) => void;
