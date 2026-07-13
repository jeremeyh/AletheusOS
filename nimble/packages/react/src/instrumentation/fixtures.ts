import {
  ENGINE_INSTRUMENT_NAMES,
  RESERVED_INSTRUMENT_NAMES,
} from "./canonical";

import {
  formatInstrumentNumber,
} from "./formatting";

import type {
  EngineInstrumentId,
  InstrumentState,
} from "./contracts";


const UPDATED_AT =
  "2026-07-12T12:00:00.000Z";


const ENGINE_VALUES: Readonly<
  Record<
    EngineInstrumentId,
    {
      readonly value: number;
      readonly confidence: number;
      readonly trend:
        | "increasing"
        | "stable"
        | "declining";
      readonly latencyMs: number;
    }
  >
> = {
  "engine.evidence": {
    value: 95.4,
    confidence: 97.1,
    trend: "increasing",
    latencyMs: 14,
  },

  "engine.knowledge": {
    value: 97.8,
    confidence: 98.3,
    trend: "stable",
    latencyMs: 11,
  },

  "engine.reason": {
    value: 94.9,
    confidence: 96.2,
    trend: "increasing",
    latencyMs: 16,
  },

  "engine.memory": {
    value: 98.2,
    confidence: 99.0,
    trend: "stable",
    latencyMs: 9,
  },

  "engine.bias": {
    value: 93.5,
    confidence: 95.4,
    trend: "declining",
    latencyMs: 18,
  },

  "engine.risk": {
    value: 91.2,
    confidence: 94.1,
    trend: "increasing",
    latencyMs: 17,
  },

  "engine.predictive": {
    value: 94.8,
    confidence: 92.7,
    trend: "increasing",
    latencyMs: 22,
  },
};


export const canonicalInstrumentationFixtures:
  readonly InstrumentState[] = [
    {
      id:
        "instrument.aletheus-index",

      canonicalName:
        RESERVED_INSTRUMENT_NAMES[
          "instrument.aletheus-index"
        ],

      value: 94.6,

      displayValue:
        formatInstrumentNumber(
          94.6,
        ),

      status: "healthy",

      trend: "increasing",

      confidence: 95.8,

      telemetry: {
        latencyMs: 19,
        confidence: 95.8,
        sourceCount: 27,
        updatedAt: UPDATED_AT,

        entries: [
          {
            id: "trajectory",
            label: "Trajectory",
            value: "+2.7",
          },
          {
            id: "stability",
            label: "Stability",
            value: 96.8,
          },
          {
            id: "horizon",
            label: "Horizon",
            value: 12,
            unit: "mo",
          },
        ],
      },

      reserved: true,
    },

    {
      id:
        "instrument.thorx",

      canonicalName:
        RESERVED_INSTRUMENT_NAMES[
          "instrument.thorx"
        ],

      value:
        "AUTHORIZED",

      displayValue:
        "AUTHORIZED",

      status:
        "healthy",

      trend:
        "stable",

      telemetry: {
        latencyMs: 8,
        updatedAt: UPDATED_AT,

        entries: [
          {
            id: "principle-x",
            label: "Principle X",
            value: "PASS",
          },
          {
            id: "constitution",
            label: "Constitution",
            value: "PASS",
          },
          {
            id: "governance",
            label: "Governance",
            value: "PASS",
          },
        ],
      },

      reserved: true,
    },

    ...(
      Object.entries(
        ENGINE_VALUES,
      ) as [
        EngineInstrumentId,
        (
          typeof ENGINE_VALUES
        )[EngineInstrumentId],
      ][]
    ).map(
      (
        [
          id,
          definition,
        ],
      ): InstrumentState => ({
        id,

        canonicalName:
          ENGINE_INSTRUMENT_NAMES[
            id
          ],

        value:
          definition.value,

        displayValue:
          formatInstrumentNumber(
            definition.value,
          ),

        status:
          definition.value >= 95
            ? "healthy"
            : "attention",

        trend:
          definition.trend,

        confidence:
          definition.confidence,

        telemetry: {
          latencyMs:
            definition.latencyMs,

          confidence:
            definition.confidence,

          sourceCount:
            Math.round(
              definition.value / 4,
            ),

          updatedAt:
            UPDATED_AT,
        },

        reserved:
          false,
      }),
    ),
  ];
