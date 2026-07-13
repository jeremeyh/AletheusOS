import {
  ENGINE_INSTRUMENT_NAMES,
  RESERVED_INSTRUMENT_NAMES,
  isEngineInstrumentId,
  isReservedInstrumentId,
} from "./canonical";

import type {
  InstrumentState,
} from "./contracts";


const VALID_STATUSES = new Set([
  "initializing",
  "healthy",
  "attention",
  "review",
  "critical",
  "unavailable",
]);


const VALID_TRENDS = new Set([
  "increasing",
  "stable",
  "declining",
  "unknown",
]);


export interface InstrumentValidationResult {
  readonly valid: boolean;
  readonly failures: readonly string[];
}


export function validateInstrumentState(
  instrument: InstrumentState,
): InstrumentValidationResult {
  const failures: string[] = [];

  if (!instrument.id.trim()) {
    failures.push(
      "Instrument id cannot be empty.",
    );
  }

  if (!instrument.canonicalName.trim()) {
    failures.push(
      `Instrument has no canonical name: ${instrument.id}`,
    );
  }

  if (!VALID_STATUSES.has(instrument.status)) {
    failures.push(
      `Unknown instrument status: ${instrument.status}`,
    );
  }

  if (!VALID_TRENDS.has(instrument.trend)) {
    failures.push(
      `Unknown instrument trend: ${instrument.trend}`,
    );
  }

  if (
    instrument.confidence !== undefined
    && (
      instrument.confidence < 0
      || instrument.confidence > 100
    )
  ) {
    failures.push(
      `Instrument confidence must be between 0 and 100: ${instrument.id}`,
    );
  }

  if (
    isReservedInstrumentId(
      instrument.id,
    )
  ) {
    const expectedName =
      RESERVED_INSTRUMENT_NAMES[
        instrument.id
      ];

    if (
      instrument.canonicalName
      !== expectedName
    ) {
      failures.push(
        `Reserved instrument cannot be renamed: ${instrument.id}`,
      );
    }

    if (!instrument.reserved) {
      failures.push(
        `Reserved instrument must be marked reserved: ${instrument.id}`,
      );
    }
  }

  if (
    isEngineInstrumentId(
      instrument.id,
    )
  ) {
    const expectedName =
      ENGINE_INSTRUMENT_NAMES[
        instrument.id
      ];

    if (
      instrument.canonicalName
      !== expectedName
    ) {
      failures.push(
        `Canonical engine identity mismatch: ${instrument.id}`,
      );
    }
  }

  if (
    Number.isNaN(
      Date.parse(
        instrument.telemetry.updatedAt,
      ),
    )
  ) {
    failures.push(
      `Invalid telemetry timestamp: ${instrument.id}`,
    );
  }

  return {
    valid:
      failures.length === 0,

    failures,
  };
}
