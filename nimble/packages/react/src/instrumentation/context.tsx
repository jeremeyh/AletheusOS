import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type {
  InstrumentState,
  InstrumentationSnapshot,
} from "./contracts";

import {
  InstrumentationRegistry,
} from "./registry";


interface InstrumentationContextValue {
  readonly registry:
    InstrumentationRegistry;

  readonly snapshot:
    InstrumentationSnapshot;
}


const InstrumentationContext =
  createContext<
    InstrumentationContextValue
    | undefined
  >(undefined);


export interface InstrumentationProviderProps {
  readonly instruments:
    readonly InstrumentState[];

  readonly children:
    ReactNode;
}


export function InstrumentationProvider({
  instruments,
  children,
}: InstrumentationProviderProps) {
  const registry = useMemo(
    () => {
      const nextRegistry =
        new InstrumentationRegistry();

      for (
        const instrument
        of instruments
      ) {
        nextRegistry.register(
          instrument,
        );
      }

      return nextRegistry;
    },
    [instruments],
  );

  const [
    snapshot,
    setSnapshot,
  ] = useState<
    InstrumentationSnapshot
  >(
    registry.snapshot(),
  );

  useEffect(
    () => registry.subscribe(
      setSnapshot,
    ),
    [registry],
  );

  return (
    <InstrumentationContext.Provider
      value={{
        registry,
        snapshot,
      }}
    >
      {children}
    </InstrumentationContext.Provider>
  );
}


export function useInstrumentationContext():
  InstrumentationContextValue {
  const context = useContext(
    InstrumentationContext,
  );

  if (!context) {
    throw new Error(
      "Instrumentation hooks must be used inside InstrumentationProvider.",
    );
  }

  return context;
}
