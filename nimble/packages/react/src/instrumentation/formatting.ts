export type InstrumentNumberFormat =
  | "score"
  | "percentage"
  | "integer"
  | "latency";


export function formatInstrumentNumber(
  value: number,
  format: InstrumentNumberFormat = "score",
): string {
  if (!Number.isFinite(value)) {
    throw new Error(
      "Instrument value must be finite.",
    );
  }

  switch (format) {
    case "percentage":
      return `${(
        value <= 1
          ? value * 100
          : value
      ).toFixed(1)}%`;

    case "integer":
      return Math.round(value).toString();

    case "latency":
      return `${Math.round(value)} ms`;

    case "score":
      return value.toFixed(1);
  }
}
