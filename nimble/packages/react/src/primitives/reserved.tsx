import {
  Instrument,
  type InstrumentProps,
} from "./Instrument";


type ReservedInstrumentProps =
  Omit<
    InstrumentProps,
    | "id"
    | "label"
    | "accentToken"
  >;


export function AletheusIndexInstrument(
  props: ReservedInstrumentProps,
) {
  return (
    <Instrument
      {...props}
      id="instrument.aletheus-index"
      label="Aletheus Index™"
      accentToken={
        "instrumentation.aletheus-index.primary"
      }
    />
  );
}


export function ThorxInstrument(
  props: ReservedInstrumentProps,
) {
  return (
    <Instrument
      {...props}
      id="instrument.thorx"
      label="THORᵡ"
      kind="authority"
      accentToken={
        "instrumentation.thorx.guard"
      }
    />
  );
}
