import type { InstrumentDefinition } from "../types";

interface Props {
  instrument: InstrumentDefinition;
  active: boolean;
  onSelect: () => void;
}

export function InstrumentCard({ instrument, active, onSelect }: Props) {
  return (
    <button
      className={`instrument-card ${active ? "instrument-card--active" : ""} risk-${instrument.risk}`}
      onClick={onSelect}
      style={{ "--accent": instrument.accent } as React.CSSProperties}
    >
      <div className="instrument-card__head">
        <span className="signal-dot" />
        <span>{instrument.metric}</span>
      </div>
      <strong>{instrument.value.toFixed(1)}</strong>
      <h3>{instrument.title}</h3>
      <p>{instrument.detail}</p>
    </button>
  );
}
