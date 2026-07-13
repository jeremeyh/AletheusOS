import type {
  EngineInstrumentId,
  ReservedInstrumentId,
} from "./contracts";


export const RESERVED_INSTRUMENT_NAMES = {
  "instrument.aletheus-index":
    "Aletheus Index™",

  "instrument.thorx":
    "THORᵡ",
} as const satisfies Readonly<
  Record<
    ReservedInstrumentId,
    string
  >
>;


export const ENGINE_INSTRUMENT_NAMES = {
  "engine.evidence":
    "Evidence Engine™",

  "engine.knowledge":
    "Knowledge Engine™",

  "engine.reason":
    "Reason Engine™",

  "engine.memory":
    "Memory Engine™",

  "engine.bias":
    "Bias Engine™",

  "engine.risk":
    "Risk Engine™",

  "engine.predictive":
    "Predictive Engine™",
} as const satisfies Readonly<
  Record<
    EngineInstrumentId,
    string
  >
>;


export const RESERVED_INSTRUMENT_IDS =
  Object.freeze(
    Object.keys(
      RESERVED_INSTRUMENT_NAMES,
    ) as ReservedInstrumentId[],
  );


export const ENGINE_INSTRUMENT_IDS =
  Object.freeze(
    Object.keys(
      ENGINE_INSTRUMENT_NAMES,
    ) as EngineInstrumentId[],
  );


export function isReservedInstrumentId(
  id: string,
): id is ReservedInstrumentId {
  return (
    id in RESERVED_INSTRUMENT_NAMES
  );
}


export function isEngineInstrumentId(
  id: string,
): id is EngineInstrumentId {
  return (
    id in ENGINE_INSTRUMENT_NAMES
  );
}
