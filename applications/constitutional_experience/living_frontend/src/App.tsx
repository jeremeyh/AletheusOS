import { useMemo, useState } from "react";
import {
  Activity,
  Blocks,
  BrainCircuit,
  ChevronRight,
  Command,
  Eye,
  Fingerprint,
  LayoutDashboard,
  LockKeyhole,
  Radar,
  Search,
  ShieldCheck,
  Sparkles,
  Workflow,
} from "lucide-react";
import { AdvancedMetrologyPanel } from "./components/AdvancedMetrologyPanel";
import { AxiomCard } from "./components/AxiomCard";
import { FounderObservatory } from "./components/FounderObservatory";
import { LIGHTSField } from "./components/LIGHTSField";
import { REMDreamSubstrate } from "./components/REMDreamSubstrate";
import { REMRuntimeHUD } from "./components/REMRuntimeHUD";
import { HardwareRuntimeHUD } from "./components/HardwareRuntimeHUD";
import { LivingEngineMeshHUD } from "./components/LivingEngineMeshHUD";
import { useHardwareRuntime } from "./runtime/use-hardware-runtime";
import { useLivingEngineMesh } from "./runtime/use-living-engine-mesh";
import { useMetrology } from "./hooks/useMetrology";
import {
  constitutionalResonance,
  defaultTelemetry,
  phaseForDensity,
} from "./runtime/information-physics";
import { SIGHTHapticsDriver } from "./runtime/sight-haptics";
import type {
  InstrumentDefinition,
  RiskState,
  TelemetryState,
} from "./types";
import type { REMRuntimeState } from "./runtime/rem-types";
import "./styles/global.css";

const instrumentRows: ReadonlyArray<
  readonly [string, string, string, number, string, RiskState, string]
> = [
  [
    "mission",
    "Mission Health",
    "MISSION",
    85,
    "#e7c35f",
    "stable",
    "Mission momentum, objective integrity, and execution readiness.",
  ],
  [
    "runtime",
    "Runtime Topology",
    "RUNTIME",
    83.5,
    "#70a3ff",
    "watch",
    "Live service topology, dependency shape, and runtime pressure.",
  ],
  [
    "truth",
    "Constitutional Compliance",
    "TRUTH",
    86.8,
    "#72e6b7",
    "strong",
    "Truth, provenance, constitutional alignment, and governance health.",
  ],
  [
    "defense",
    "SPARTAN Posture",
    "DEFENSE",
    84.2,
    "#ff7168",
    "watch",
    "Threat posture, containment readiness, and trust-plane integrity.",
  ],
  [
    "signal",
    "Market Intelligence",
    "SIGNAL",
    94.7,
    "#d675ff",
    "strong",
    "Opportunity pressure, scarcity, momentum, and market signal.",
  ],
  [
    "build",
    "Developer Activity",
    "BUILD",
    89.5,
    "#61d7ff",
    "stable",
    "Contribution velocity, patch activity, and release convergence.",
  ],
];

const instruments: InstrumentDefinition[] = instrumentRows.map(
  ([id, title, metric, value, accent, risk, detail]) => ({
    id,
    title,
    metric,
    value,
    accent,
    risk,
    detail,
  }),
);

const navigation = [
  ["LIGHTS Field", Sparkles],
  ["Workspace Composer", Blocks],
  ["Runtime Topology", Workflow],
  ["Mission Intelligence", BrainCircuit],
  ["SPARTAN", ShieldCheck],
] as const;

const haptics = new SIGHTHapticsDriver();

export function App() {
  const [selected, setSelected] = useState("mission");
  const [telemetry, setTelemetry] =
    useState<TelemetryState>(defaultTelemetry);
  const [founder, setFounder] = useState(false);
  const hardwareRuntime = useHardwareRuntime();
  const livingEngineMesh = useLivingEngineMesh();
  const [remCrystallized, setREMCrystallized] = useState(true);
  const [remState, setREMState] = useState<REMRuntimeState>({
    phase: "ambient",
    coherence: 0.06,
    targetCoherence: 0.06,
    crystallized: false,
    particleCount: 320,
    frameTimeMs: 1000 / 120,
    frameVarianceMs: 0,
    meantimeQuotient: 0.913,
    droppedFrameRatio: 0,
  });

  const current = useMemo(
    () => instruments.find((instrument) => instrument.id === selected) ??
      instruments[0],
    [selected],
  );
  const phase = phaseForDensity(telemetry.fieldDensity);
  const resonance = constitutionalResonance(
    telemetry.veracity,
    telemetry.consensus,
    telemetry.contradiction,
  );
  const metrology = useMetrology({
    ...telemetry,
    resonance,
  });

  const setDensity = (density: number) => {
    setTelemetry((currentTelemetry) => ({
      ...currentTelemetry,
      fieldDensity: density,
      elasticity: Math.max(0.05, 1 - density * 0.72),
    }));
    if (density >= 0.92) {
      haptics.trigger("PHASE_CRYSTALLIZATION", density);
    }
  };

  const toggleFounder = () => {
    const next = !founder;
    setFounder(next);
    setTelemetry((currentTelemetry) => ({
      ...currentTelemetry,
      founderMode: next ? 1 : 0,
    }));
    if (next) {
      haptics.trigger("FOUNDER_DECRYPTION", 1);
    }
  };

  return (
    <div className={`app-shell rem-phase-${remState.phase}`}>
      <REMDreamSubstrate
        crystallized={remCrystallized}
        resonance={resonance}
        founderMode={founder}
        onState={setREMState}
      />
      <REMRuntimeHUD state={remState} />
      <HardwareRuntimeHUD state={hardwareRuntime} />
      <LivingEngineMeshHUD snapshot={livingEngineMesh} />
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">
            <img src="/aletheusos-canonical-mark.jpeg" alt="AletheusOS" />
            <span />
          </div>
          <div>
            <strong>ALETHEUSOS</strong>
            <small>Genesis 39.2 • LIGHTS</small>
          </div>
        </div>

        <nav>
          {navigation.map(([label, Icon], index) => (
            <button className={index === 0 ? "active" : ""} key={label}>
              <Icon size={18} />
              <span>{label}</span>
              <ChevronRight size={14} />
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="authority">
            <Fingerprint size={18} />
            <div>
              <span>Authority Plane</span>
              <strong>{founder ? "Founder Root" : "Standard User"}</strong>
            </div>
          </div>
          <button
            className="rem-crystallize-toggle"
            onClick={() => setREMCrystallized((current) => !current)}
          >
            <Sparkles size={16} />
            {remCrystallized ? "Dissolve UI Lattice" : "Crystallize UI Lattice"}
          </button>
          <button className="founder-toggle" onClick={toggleFounder}>
            {founder ? <Eye size={16} /> : <LockKeyhole size={16} />}
            {founder ? "Founder View Active" : "Founder View Sealed"}
          </button>
        </div>
      </aside>

      <main>
        <header>
          <div>
            <span className="eyebrow">
              AletheusOS Constitutional Experience Engine
            </span>
            <h1>LIGHTS™ Living Intelligence Field</h1>
          </div>
          <div className="actions">
            <label>
              <Search size={17} />
              <input placeholder="Search missions, evidence, engines..." />
              <kbd>⌘K</kbd>
            </label>
            <button aria-label="Open command surface">
              <Command size={18} />
            </button>
            <button className="avatar">JK</button>
          </div>
        </header>

        <section className="hero">
          <LIGHTSField telemetry={{ ...telemetry, resonance }} />
          <div className="hero-copy">
            <span className="status"><i />Field Alive</span>
            <h2>
              The interface is not a screen.
              <br />
              <em>It is LIGHTS™.</em>
            </h2>
            <p>
              A Living Intelligence Gravitational Harmonic Topology Space
              where evidence, mission priority, constitutional authority,
              and runtime state continuously reshape the operator environment.
            </p>
          </div>
          <div className="mq">
            <div>
              <span>Meantime Quotient</span>
              <strong>
                {(remState.meantimeQuotient * 100).toFixed(1)}
              </strong>
              <small>Practical resonance</small>
            </div>
          </div>
        </section>

        <section className="controls">
          <div>
            <span>Current Phase</span>
            <strong>{phase}</strong>
          </div>
          <label>
            <span>Field Density</span>
            <input
              type="range"
              min="0"
              max="1"
              step=".01"
              value={telemetry.fieldDensity}
              onChange={(event) => setDensity(Number(event.target.value))}
            />
            <strong>{telemetry.fieldDensity.toFixed(2)}</strong>
          </label>
        </section>

        <section className="instrument-grid">
          {instruments.map((instrument) => (
            <AxiomCard
              key={instrument.id}
              instrument={instrument}
              telemetry={telemetry}
              active={instrument.id === selected}
              onSelect={() => setSelected(instrument.id)}
            />
          ))}
        </section>

        <AdvancedMetrologyPanel snapshot={metrology} />

        <section className="detail-grid">
          <article className="panel wide">
            <div className="panel-head">
              <div>
                <span className="eyebrow">Selected Living Instrument</span>
                <h2>{current.title}</h2>
              </div>
              <span className="phase">{phase}</span>
            </div>
            <div className="bars">
              {metrology.fft.slice(0, 44).map((value: number, index: number) => (
                <span key={index} style={{ height: `${value * 100}%` }} />
              ))}
            </div>
            <div className="metrics">
              {[
                ["Veracity", telemetry.veracity],
                ["Consensus", telemetry.consensus],
                ["Contradiction", telemetry.contradiction],
                ["Elasticity", telemetry.elasticity],
                ["Resonance", resonance],
              ].map(([key, value]) => (
                <div key={key as string}>
                  <span>{key}</span>
                  <strong>{(value as number).toFixed(3)}</strong>
                </div>
              ))}
            </div>
          </article>

          <article className="panel">
            <div className="panel-head">
              <div>
                <span className="eyebrow">Information Physics</span>
                <h2>Field State</h2>
              </div>
              <Radar size={20} />
            </div>
            <div className="physics">
              {[
                ["Information Mass", 0.861],
                ["Entropy", telemetry.entropy],
                ["Mission Gravity", telemetry.missionMass],
                ["Harmonic Stability", metrology.harmonicStability],
                ["Signal Integrity", metrology.signalIntegrity],
                ["Noise Floor", metrology.noiseFloor],
              ].map(([key, value]) => (
                <div key={key as string}>
                  <span>{key}</span>
                  <strong>{(value as number).toFixed(3)}</strong>
                </div>
              ))}
            </div>
          </article>
        </section>

        <FounderObservatory authorized={founder} />

        <footer>
          {[
            [Activity, "Runtime healthy"],
            [Radar, "SIGHT observer active"],
            [LayoutDashboard, "Topology persistent"],
            [ShieldCheck, "Constitutional isolation active"],
          ].map(([Icon, text]) => (
            <div key={text as string}>
              <Icon size={15} />
              {text as string}
            </div>
          ))}
        </footer>
      </main>
    </div>
  );
}
