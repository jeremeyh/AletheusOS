import { Activity, Cpu, Radio, Waves } from "lucide-react";
import { motion } from "framer-motion";
import type { MetrologySnapshot } from "../types";

const channelLabels = ["L", "C", "R", "Ls", "Rs", "LFE"] as const;

export function AdvancedMetrologyPanel({
  snapshot,
}: {
  snapshot: MetrologySnapshot;
}) {
  return (
    <section className="metrology-grid" aria-label="Advanced metrology">
      <article className="metrology-panel metrology-panel--loudness">
        <div className="metrology-heading">
          <div>
            <span className="eyebrow">Platform Evidence</span>
            <h2><Activity size={17} /> Kinetic Pulse & Metrology</h2>
          </div>
          <span className="metrology-live"><i /> LIVE</span>
        </div>

        <div className="metrology-values">
          <Value
            label="Short-Term"
            value={snapshot.loudness.shortTerm}
            unit="LUFS"
            tone="gold"
          />
          <Value
            label="Integrated"
            value={snapshot.loudness.integrated}
            unit="LUFS"
            tone="rose"
          />
          <Value
            label="Momentary"
            value={snapshot.loudness.momentary}
            unit="LUFS"
            tone="green"
          />
        </div>

        <div className="channel-caption">
          <span>CHANNEL LEVELS (RMS / PEAK)</span>
          <span>TRUE PEAK {snapshot.loudness.truePeak.toFixed(2)} dB</span>
        </div>
        <div className="channel-array">
          {snapshot.channels.map((level, index) => (
            <div className="channel-meter" key={channelLabels[index] ?? index}>
              <div className="channel-meter__well">
                <motion.span
                  animate={{ height: `${Math.max(5, level * 100)}%` }}
                  transition={{ type: "spring", stiffness: 260, damping: 26 }}
                />
                <i />
              </div>
              <small>{channelLabels[index] ?? index + 1}</small>
            </div>
          ))}
        </div>
      </article>

      <article className="metrology-panel metrology-panel--phase">
        <div className="metrology-heading">
          <div>
            <span className="eyebrow">Phase-Space Topology</span>
            <h2><Radio size={17} /> Lissajous Polar Engine</h2>
          </div>
          <span className="phase-chip">POLAR</span>
        </div>

        <Lissajous
          phase={snapshot.phaseCorrelation}
          width={snapshot.stereoWidth}
        />

        <div className="phase-readout">
          <span>
            Phase Correlation
            <strong>+{snapshot.phaseCorrelation.toFixed(3)}</strong>
          </span>
          <span>
            Spatial Width
            <strong>{Math.round(snapshot.stereoWidth * 100)}%</strong>
          </span>
        </div>
      </article>

      <article className="metrology-panel metrology-panel--spectrum">
        <div className="metrology-heading">
          <div>
            <span className="eyebrow">Constitutional Signal Spectrum</span>
            <h2><Cpu size={17} /> Active Dynamic Frequency Field</h2>
          </div>
          <span className="spectrum-range">20Hz — 20kHz / 52 BINS</span>
        </div>

        <div className="fft-spectrum">
          {snapshot.fft.map((value, index) => (
            <motion.span
              key={index}
              animate={{ height: `${Math.max(4, value * 100)}%` }}
              transition={{ duration: 0.12, ease: "linear" }}
            />
          ))}
        </div>
        <div className="spectrum-axis">
          <span>20</span><span>100</span><span>1k</span><span>10k</span><span>20k Hz</span>
        </div>
      </article>

      <article className="metrology-panel metrology-panel--quotient">
        <div className="metrology-heading">
          <div>
            <span className="eyebrow">Practical Resonance</span>
            <h2><Waves size={17} /> Meantime Quotient</h2>
          </div>
        </div>
        <QuotientGauge snapshot={snapshot} />
      </article>
    </section>
  );
}

function Value({
  label,
  value,
  unit,
  tone,
}: {
  label: string;
  value: number;
  unit: string;
  tone: "gold" | "rose" | "green";
}) {
  return (
    <div className={`metrology-value metrology-value--${tone}`}>
      <span>{label}</span>
      <strong>{value.toFixed(1)}</strong>
      <small>{unit}</small>
    </div>
  );
}

function Lissajous({
  phase,
  width,
}: {
  phase: number;
  width: number;
}) {
  const delta = (1 - phase) * Math.PI * 0.8;
  const points = Array.from({ length: 220 }, (_, index) => {
    const t = (index / 219) * Math.PI * 2;
    const x = 100 + Math.sin(t + delta) * 67 * Math.min(width / 1.42, 1.2);
    const y = 80 + Math.sin(t * 2) * 55;
    return `${x.toFixed(2)},${y.toFixed(2)}`;
  }).join(" ");

  return (
    <div className="lissajous-field">
      <svg viewBox="0 0 200 160" role="img" aria-label="Lissajous phase topology">
        <circle cx="100" cy="80" r="58" />
        <circle cx="100" cy="80" r="36" />
        <line x1="18" y1="80" x2="182" y2="80" />
        <line x1="100" y1="10" x2="100" y2="150" />
        <motion.polyline
          points={points}
          initial={false}
          animate={{ opacity: [0.62, 0.96, 0.62] }}
          transition={{ duration: 8.8, repeat: Infinity, ease: "easeInOut" }}
        />
      </svg>
    </div>
  );
}

function QuotientGauge({
  snapshot,
}: {
  snapshot: MetrologySnapshot;
}) {
  const value = snapshot.meantimeQuotient * 100;
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - snapshot.meantimeQuotient);

  return (
    <div className="quotient-instrument">
      <svg viewBox="0 0 176 176">
        <defs>
          <linearGradient id="mq-spectrum" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#61d7ff" />
            <stop offset=".48" stopColor="#72e6b7" />
            <stop offset="1" stopColor="#e7c35f" />
          </linearGradient>
        </defs>
        <circle cx="88" cy="88" r={radius} className="quotient-track" />
        <motion.circle
          cx="88"
          cy="88"
          r={radius}
          className="quotient-progress"
          strokeDasharray={circumference}
          animate={{ strokeDashoffset: offset }}
          transition={{ type: "spring", stiffness: 70, damping: 18 }}
        />
      </svg>
      <div>
        <span>MEANTIME QUOTIENT</span>
        <strong>{value.toFixed(1)}</strong>
        <small>Practical resonance</small>
      </div>
      <footer>
        <span>Stability {(snapshot.harmonicStability * 100).toFixed(1)}</span>
        <span>Integrity {(snapshot.signalIntegrity * 100).toFixed(1)}</span>
      </footer>
    </div>
  );
}
