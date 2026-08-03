import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  constitutionalResonance,
  defaultTelemetry,
  phaseForDensity,
} from "../runtime/information-physics";
import type { PhaseState, TelemetryState } from "../types";

export interface LIGHTSContextValue {
  telemetry: TelemetryState;
  phase: PhaseState;
  resonance: number;
  respiration: number;
  setFieldDensity: (density: number) => void;
  setFounderMode: (enabled: boolean) => void;
  updateTelemetry: (patch: Partial<TelemetryState>) => void;
}

const LIGHTSContext = createContext<LIGHTSContextValue | null>(null);

export function LIGHTSProvider({ children }: { children: ReactNode }) {
  const [telemetry, setTelemetry] =
    useState<TelemetryState>(defaultTelemetry);

  const resonance = constitutionalResonance(
    telemetry.veracity,
    telemetry.consensus,
    telemetry.contradiction,
  );
  const phase = phaseForDensity(telemetry.fieldDensity);

  const value = useMemo<LIGHTSContextValue>(() => {
    const respiration =
      8 + (1 - resonance) * 4 + telemetry.entropy * 1.5;

    return {
      telemetry: { ...telemetry, resonance },
      phase,
      resonance,
      respiration,
      setFieldDensity: (density: number) => {
        const bounded = Math.max(0, Math.min(1, density));
        setTelemetry((current) => ({
          ...current,
          fieldDensity: bounded,
          elasticity: Math.max(0.05, 1 - bounded * 0.72),
        }));
      },
      setFounderMode: (enabled: boolean) => {
        setTelemetry((current) => ({
          ...current,
          founderMode: enabled ? 1 : 0,
        }));
      },
      updateTelemetry: (patch: Partial<TelemetryState>) => {
        setTelemetry((current) => ({ ...current, ...patch }));
      },
    };
  }, [phase, resonance, telemetry]);

  return (
    <LIGHTSContext.Provider value={value}>
      {children}
    </LIGHTSContext.Provider>
  );
}

export function useLIGHTS(): LIGHTSContextValue {
  const value = useContext(LIGHTSContext);
  if (value === null) {
    throw new Error("useLIGHTS must be used inside LIGHTSProvider");
  }
  return value;
}
