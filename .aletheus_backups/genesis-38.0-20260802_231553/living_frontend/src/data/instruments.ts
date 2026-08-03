import type { InstrumentDefinition } from "../types.js";

export const instruments: InstrumentDefinition[] = [
  { id: "mission-health", title: "Mission Health", category: "mission", minWidth: 300, minHeight: 220, defaultWidth: 420, defaultHeight: 280 },
  { id: "runtime-topology", title: "Runtime Topology", category: "topology", minWidth: 360, minHeight: 260, defaultWidth: 560, defaultHeight: 360 },
  { id: "information-physics", title: "Information Physics", category: "telemetry", minWidth: 320, minHeight: 240, defaultWidth: 440, defaultHeight: 300 },
  { id: "constitutional-compliance", title: "Constitutional Compliance", category: "governance", minWidth: 320, minHeight: 220, defaultWidth: 420, defaultHeight: 280 },
  { id: "spartan-posture", title: "SPARTAN™ Security Posture", category: "security", minWidth: 340, minHeight: 240, defaultWidth: 470, defaultHeight: 300 },
  { id: "market-intelligence", title: "Market Intelligence", category: "market", minWidth: 340, minHeight: 240, defaultWidth: 470, defaultHeight: 300 },
  { id: "founder-observatory", title: "Founder Observatory", category: "governance", minWidth: 520, minHeight: 360, defaultWidth: 760, defaultHeight: 520, founderOnly: true },
];
