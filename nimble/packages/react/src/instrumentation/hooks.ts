import type {
  EngineInstrumentId,
  ReservedInstrumentId,
} from "./contracts";

import {
  useInstrumentationContext,
} from "./context";


export function useInstrumentation() {
  return useInstrumentationContext();
}


export function useInstrument(
  id: string,
) {
  const {
    registry,
    snapshot,
  } = useInstrumentationContext();

  return snapshot.instruments.find(
    (instrument) =>
      instrument.id === id,
  ) ?? registry.resolve(id);
}


export function useEngineInstrument(
  id: EngineInstrumentId,
) {
  return useInstrument(id);
}


export function useReservedInstrument(
  id: ReservedInstrumentId,
) {
  return useInstrument(id);
}
