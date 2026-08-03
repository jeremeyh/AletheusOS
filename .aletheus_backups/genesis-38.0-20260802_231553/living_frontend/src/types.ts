export type VeracityPhase = "nebular" | "fluid" | "quasi" | "crystalline";

export interface RuntimeSignal {
  id: string;
  label: string;
  value: number;
  confidence: number;
  urgency: number;
  contradiction: number;
  provenance: number;
  consensus: number;
}

export interface InstrumentDefinition {
  id: string;
  title: string;
  category: "mission" | "telemetry" | "topology" | "governance" | "market" | "security";
  minWidth: number;
  minHeight: number;
  defaultWidth: number;
  defaultHeight: number;
  founderOnly?: boolean;
}

export interface WorkspaceInstrument {
  instanceId: string;
  instrumentId: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface WorkspaceState {
  version: number;
  name: string;
  instruments: WorkspaceInstrument[];
}

export interface Principal {
  subject: string;
  displayName: string;
  claims: string[];
}
