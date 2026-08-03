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
import { AdaptiveField } from "./components/AdaptiveField";
import { FounderObservatory } from "./components/FounderObservatory";
import { InstrumentCard } from "./components/InstrumentCard";
import type { InstrumentDefinition, PhaseState } from "./types";
import "./styles/global.css";

const instruments: InstrumentDefinition[] = [
  { id: "mission", title: "Mission Health", metric: "MISSION", value: 85.0, accent: "#e7c35f", risk: "stable", detail: "Mission momentum, objective integrity, and execution readiness." },
  { id: "runtime", title: "Runtime Topology", metric: "RUNTIME", value: 83.5, accent: "#70a3ff", risk: "stable", detail: "Live service topology, dependency shape, and runtime pressure." },
  { id: "truth", title: "Constitutional Compliance", metric: "TRUTH", value: 86.8, accent: "#72e6b7", risk: "stable", detail: "Truth, provenance, constitutional alignment, and governance health." },
  { id: "defense", title: "SPARTAN Posture", metric: "DEFENSE", value: 84.2, accent: "#ff7168", risk: "watch", detail: "Threat posture, containment readiness, and trust-plane integrity." },
  { id: "signal", title: "Market Intelligence", metric: "SIGNAL", value: 94.7, accent: "#d675ff", risk: "strong", detail: "Opportunity pressure, scarcity, momentum, and market signal." },
  { id: "build", title: "Developer Activity", metric: "BUILD", value: 89.5, accent: "#61d7ff", risk: "strong", detail: "Contribution velocity, patch activity, and release convergence." },
];

const navigation = [
  { label: "Living Field", icon: Sparkles },
  { label: "Workspace Composer", icon: Blocks },
  { label: "Runtime Topology", icon: Workflow },
  { label: "Mission Intelligence", icon: BrainCircuit },
  { label: "SPARTAN", icon: ShieldCheck },
];

const phases: PhaseState[] = [
  "Nebular",
  "Fluid Reactive",
  "Quasi-Crystalline",
  "Crystalline Solid",
];

export function App() {
  const [selectedId, setSelectedId] = useState("mission");
  const [phase, setPhase] = useState<PhaseState>("Quasi-Crystalline");
  const [founderMode, setFounderMode] = useState(false);
  const [density, setDensity] = useState(0.72);

  const selected = useMemo(
    () => instruments.find((instrument) => instrument.id === selectedId)!,
    [selectedId],
  );

  const phaseClass = phase.toLowerCase().replaceAll(" ", "-");

  return (
    <div
      className={`app-shell phase-${phaseClass}`}
      style={{ "--density": density } as React.CSSProperties}
    >
      <aside className="sidebar">
        <div className="brand">
          <div className="brand__logo-shell">
            <img
              className="brand__logo"
              src="/aletheusos-canonical-logo.jpeg"
              alt="AletheusOS canonical gold logo"
            />
            <span className="brand__shimmer" />
          </div>
          <div className="brand__copy">
            <strong>ALETHEUSOS</strong>
            <small>Genesis 38.2</small>
          </div>
        </div>

        <nav className="nav-stack">
          {navigation.map(({ label, icon: Icon }, index) => (
            <button
              key={label}
              className={`nav-item ${index === 0 ? "nav-item--active" : ""}`}
            >
              <Icon size={18} />
              <span>{label}</span>
              <ChevronRight size={14} />
            </button>
          ))}
        </nav>

        <div className="sidebar__bottom">
          <div className="authority-plane">
            <Fingerprint size={18} />
            <div>
              <span>Authority Plane</span>
              <strong>{founderMode ? "Founder Root" : "Standard User"}</strong>
            </div>
          </div>

          <button
            className="founder-toggle"
            onClick={() => setFounderMode((value) => !value)}
          >
            {founderMode ? <Eye size={16} /> : <LockKeyhole size={16} />}
            {founderMode ? "Founder View Active" : "Founder View Sealed"}
          </button>
        </div>
      </aside>

      <main className="experience">
        <header className="topbar">
          <div>
            <span className="eyebrow">
              Constitutional Experience Intelligence
            </span>
            <h1>Living Intelligence Field</h1>
          </div>

          <div className="topbar__actions">
            <label className="search-box">
              <Search size={17} />
              <input placeholder="Search missions, evidence, engines..." />
              <kbd>⌘K</kbd>
            </label>
            <button className="icon-button"><Command size={18} /></button>
            <button className="avatar">JK</button>
          </div>
        </header>

        <section className="hero-field">
          <AdaptiveField phase={phase} density={density} />
          <div className="hero-copy">
            <span className="status-pill"><span />System Alive</span>
            <h2>
              The interface is not a screen.
              <br />
              <em>It is a responsive field.</em>
            </h2>
            <p>
              Information mass, veracity, mission priority, and constitutional
              authority continuously shape the workspace around the operator.
            </p>
          </div>

          <div className="mq-ring">
            <div>
              <span>Meantime Quotient</span>
              <strong>91.3</strong>
              <small>Practical resonance</small>
            </div>
          </div>
        </section>

        <section className="controls-strip">
          <div className="phase-switcher">
            {phases.map((phaseName) => (
              <button
                key={phaseName}
                className={phase === phaseName ? "active" : ""}
                onClick={() => setPhase(phaseName)}
              >
                {phaseName}
              </button>
            ))}
          </div>

          <label className="density-control">
            <span>Field Density</span>
            <input
              type="range"
              min="0.35"
              max="1"
              step="0.01"
              value={density}
              onChange={(event) => setDensity(Number(event.target.value))}
            />
            <strong>{density.toFixed(2)}</strong>
          </label>
        </section>

        <section className="instrument-grid">
          {instruments.map((instrument) => (
            <InstrumentCard
              key={instrument.id}
              instrument={instrument}
              active={instrument.id === selectedId}
              onSelect={() => setSelectedId(instrument.id)}
            />
          ))}
        </section>

        <section className="detail-grid">
          <article className="glass-panel glass-panel--wide">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Selected Instrument</span>
                <h2>{selected.title}</h2>
              </div>
              <div className="phase-chip"><span />{phase}</div>
            </div>

            <div className="signal-chart">
              {Array.from({ length: 44 }, (_, index) => (
                <span
                  key={index}
                  style={{
                    height: `${28 + Math.abs(Math.sin(index * 0.46 + density)) * 72}%`,
                  }}
                />
              ))}
            </div>

            <div className="metric-row">
              <div><span>Veracity</span><strong>0.982</strong></div>
              <div><span>Consensus</span><strong>0.947</strong></div>
              <div className="metric-row__warning"><span>Contradiction</span><strong>0.061</strong></div>
              <div><span>Elasticity</span><strong>{density.toFixed(3)}</strong></div>
            </div>
          </article>

          <article className="glass-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Information Physics</span>
                <h2>Phase State</h2>
              </div>
              <Radar size={20} />
            </div>

            <div className="phase-list">
              {phases.map((phaseName, index) => (
                <button
                  key={phaseName}
                  onClick={() => setPhase(phaseName)}
                  className={`phase-list__item ${phase === phaseName ? "active" : ""}`}
                >
                  <span>{phaseName}</span>
                  <strong>{[0.18, 0.63, 0.91, 0.98][index]}</strong>
                </button>
              ))}
            </div>
          </article>
        </section>

        <FounderObservatory authorized={founderMode} />

        <footer className="system-strip">
          <div><Activity size={15} />Runtime healthy</div>
          <div><Radar size={15} />Telemetry streaming</div>
          <div><LayoutDashboard size={15} />Workspace persistent</div>
          <div><ShieldCheck size={15} />Constitutional isolation active</div>
        </footer>
      </main>
    </div>
  );
}
