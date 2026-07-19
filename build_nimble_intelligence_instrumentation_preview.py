#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REACT_ROOT = ROOT / "nimble/packages/react/src"
INSTRUMENTATION_ROOT = REACT_ROOT / "instrumentation"

SHELL_ROOT = ROOT / "nimble/apps/platform-shell"

VALIDATOR = (
    ROOT
    / "validate_nimble_instrumentation_preview.py"
)

TEST_FILE = (
    ROOT
    / "tests/nimble/test_instrumentation_preview.py"
)


REQUIRED_DEPENDENCIES = [
    ROOT
    / "nimble/packages/react/src/primitives/Instrument.tsx",

    ROOT
    / "nimble/packages/react/src/primitives/Meter.tsx",

    ROOT
    / "nimble/packages/core/src/experience/index.ts",

    ROOT
    / "nimble/orchestrator/manifest.py",
]


INSTRUMENTATION_FILES: dict[str, str] = {
    "contracts.ts": r'''
export type InstrumentStatus =
  | "initializing"
  | "healthy"
  | "attention"
  | "review"
  | "critical"
  | "unavailable";


export type InstrumentTrend =
  | "increasing"
  | "stable"
  | "declining"
  | "unknown";


export type ReservedInstrumentId =
  | "instrument.aletheus-index"
  | "instrument.thorx";


export type EngineInstrumentId =
  | "engine.evidence"
  | "engine.knowledge"
  | "engine.reason"
  | "engine.memory"
  | "engine.bias"
  | "engine.risk"
  | "engine.predictive";


export type InstrumentId =
  | ReservedInstrumentId
  | EngineInstrumentId
  | `application.${string}`;


export interface InstrumentTelemetryEntry {
  readonly id: string;
  readonly label: string;
  readonly value: string | number;
  readonly unit?: string;
}


export interface InstrumentTelemetry {
  readonly latencyMs?: number;
  readonly confidence?: number;
  readonly sourceCount?: number;
  readonly updatedAt: string;
  readonly warnings?: readonly string[];
  readonly notes?: readonly string[];
  readonly entries?: readonly InstrumentTelemetryEntry[];
}


export interface InstrumentState {
  readonly id: InstrumentId;
  readonly canonicalName: string;
  readonly displayName?: string;
  readonly value: number | string;
  readonly displayValue: string;
  readonly status: InstrumentStatus;
  readonly trend: InstrumentTrend;
  readonly confidence?: number;
  readonly telemetry: InstrumentTelemetry;
  readonly reserved: boolean;
  readonly metadata?: Readonly<Record<string, unknown>>;
}


export interface InstrumentationSnapshot {
  readonly schemaVersion: "1.0";
  readonly capturedAt: string;
  readonly instruments: readonly InstrumentState[];
}


export type InstrumentationListener = (
  snapshot: InstrumentationSnapshot,
) => void;
''',

    "canonical.ts": r'''
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
''',

    "formatting.ts": r'''
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
''',

    "validation.ts": r'''
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
''',

    "registry.ts": r'''
import type {
  InstrumentState,
  InstrumentationListener,
  InstrumentationSnapshot,
} from "./contracts";

import {
  validateInstrumentState,
} from "./validation";


export class InstrumentationRegistry {
  readonly #instruments = new Map<
    string,
    InstrumentState
  >();

  readonly #listeners = new Set<
    InstrumentationListener
  >();


  register(
    instrument: InstrumentState,
  ): void {
    if (
      this.#instruments.has(
        instrument.id,
      )
    ) {
      throw new Error(
        `Duplicate instrument: ${instrument.id}`,
      );
    }

    const validation =
      validateInstrumentState(
        instrument,
      );

    if (!validation.valid) {
      throw new Error(
        [
          "Instrument validation failed:",
          ...validation.failures,
        ].join("\n"),
      );
    }

    this.#instruments.set(
      instrument.id,
      Object.freeze({
        ...instrument,
      }),
    );

    this.#emit();
  }


  update(
    instrument: InstrumentState,
  ): void {
    if (
      !this.#instruments.has(
        instrument.id,
      )
    ) {
      throw new Error(
        `Unknown instrument: ${instrument.id}`,
      );
    }

    const validation =
      validateInstrumentState(
        instrument,
      );

    if (!validation.valid) {
      throw new Error(
        [
          "Instrument validation failed:",
          ...validation.failures,
        ].join("\n"),
      );
    }

    this.#instruments.set(
      instrument.id,
      Object.freeze({
        ...instrument,
      }),
    );

    this.#emit();
  }


  resolve(
    id: string,
  ): InstrumentState {
    const instrument =
      this.#instruments.get(id);

    if (!instrument) {
      throw new Error(
        `Unknown instrument: ${id}`,
      );
    }

    return instrument;
  }


  has(
    id: string,
  ): boolean {
    return this.#instruments.has(id);
  }


  list(): readonly InstrumentState[] {
    return Object.freeze(
      [
        ...this.#instruments.values(),
      ],
    );
  }


  snapshot(): InstrumentationSnapshot {
    return Object.freeze({
      schemaVersion: "1.0",
      capturedAt:
        new Date().toISOString(),
      instruments: this.list(),
    });
  }


  subscribe(
    listener: InstrumentationListener,
  ): () => void {
    this.#listeners.add(listener);

    listener(this.snapshot());

    return () => {
      this.#listeners.delete(
        listener,
      );
    };
  }


  #emit(): void {
    const snapshot =
      this.snapshot();

    for (
      const listener
      of this.#listeners
    ) {
      listener(snapshot);
    }
  }
}
''',

    "fixtures.ts": r'''
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
''',

    "context.tsx": r'''
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
''',

    "hooks.ts": r'''
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
''',

    "index.ts": r'''
export * from "./canonical";
export * from "./context";
export * from "./contracts";
export * from "./fixtures";
export * from "./formatting";
export * from "./hooks";
export * from "./registry";
export * from "./validation";
''',
}


SHELL_FILES: dict[str, str] = {
    "src/nimble/showcase/IntelligenceInstrumentationShowcase.tsx": r'''
import {
  AletheusIndexInstrument,
  Badge,
  Grid,
  Instrument,
  Meter,
  Panel,
  Signal,
  Stack,
  Surface,
  Text,
  ThorxInstrument,
} from "@aletheus/nimble-react";

import {
  ENGINE_INSTRUMENT_IDS,
  InstrumentationProvider,
  canonicalInstrumentationFixtures,
  useEngineInstrument,
  useReservedInstrument,
} from "@aletheus/nimble-react";

import type {
  EngineInstrumentId,
  InstrumentState,
} from "@aletheus/nimble-react";

import "./instrumentation-preview.css";


const ENGINE_ACCENTS = {
  "engine.evidence":
    "instrumentation.engine.evidence",

  "engine.knowledge":
    "instrumentation.engine.knowledge",

  "engine.reason":
    "instrumentation.engine.reason",

  "engine.memory":
    "instrumentation.engine.memory",

  "engine.bias":
    "instrumentation.engine.bias",

  "engine.risk":
    "instrumentation.engine.risk",

  "engine.predictive":
    "instrumentation.engine.predictive",
} as const;


function TelemetrySummary({
  instrument,
}: {
  readonly instrument:
    InstrumentState;
}) {
  return (
    <div className="telemetry-summary">
      {instrument.confidence !== undefined ? (
        <span>
          Confidence{" "}
          {instrument.confidence.toFixed(1)}
        </span>
      ) : null}

      {instrument.telemetry.latencyMs !== undefined ? (
        <span>
          Latency{" "}
          {instrument.telemetry.latencyMs}
          {" "}ms
        </span>
      ) : null}

      <span>
        Trend{" "}
        {instrument.trend}
      </span>
    </div>
  );
}


function ReservedInstruments() {
  const index =
    useReservedInstrument(
      "instrument.aletheus-index",
    );

  const thorx =
    useReservedInstrument(
      "instrument.thorx",
    );

  return (
    <Grid
      columns="minmax(0, 1.35fr) minmax(280px, 0.65fr)"
      gap="lg"
      className="reserved-grid"
    >
      <AletheusIndexInstrument
        value={
          index.displayValue
        }
        numericValue={
          typeof index.value === "number"
            ? index.value
            : undefined
        }
        status={
          index.status
        }
        density="founder"
        kind="gauge"
        detail={
          <TelemetrySummary
            instrument={index}
          />
        }
        footer={
          <Stack
            direction="row"
            spacing="sm"
            wrap
          >
            {index.telemetry.entries?.map(
              (entry) => (
                <Badge
                  key={entry.id}
                  intent="authority"
                >
                  {entry.label}{" "}
                  {entry.value}
                  {entry.unit ?? ""}
                </Badge>
              ),
            )}
          </Stack>
        }
      />

      <ThorxInstrument
        value={
          thorx.displayValue
        }
        status={
          thorx.status
        }
        density="founder"
        detail={
          <Stack spacing="xs">
            {thorx.telemetry.entries?.map(
              (entry) => (
                <Text
                  key={entry.id}
                  variant="telemetry"
                >
                  {entry.label}
                  {" · "}
                  {entry.value}
                </Text>
              ),
            )}
          </Stack>
        }
        footer={
          <Badge intent="healthy">
            CONSTITUTIONAL RELEASE VALID
          </Badge>
        }
      />
    </Grid>
  );
}


function EngineInstrumentCard({
  id,
}: {
  readonly id:
    EngineInstrumentId;
}) {
  const instrument =
    useEngineInstrument(id);

  return (
    <Instrument
      id={instrument.id}
      label={
        instrument.displayName
        ?? instrument.canonicalName
      }
      value={
        instrument.displayValue
      }
      numericValue={
        typeof instrument.value === "number"
          ? instrument.value
          : undefined
      }
      status={
        instrument.status
      }
      density="enterprise"
      kind="meter"
      accentToken={
        ENGINE_ACCENTS[id]
      }
      detail={
        <TelemetrySummary
          instrument={instrument}
        />
      }
    />
  );
}


function EngineGrid() {
  return (
    <Panel
      title="Individual Engine Grades"
      description={
        "Independent instruments—not a leaderboard and not a collapsed consensus score."
      }
    >
      <Grid
        minColumnWidth={250}
        gap="md"
      >
        {ENGINE_INSTRUMENT_IDS.map(
          (id) => (
            <EngineInstrumentCard
              key={id}
              id={id}
            />
          ),
        )}
      </Grid>
    </Panel>
  );
}


function StateGallery() {
  const states = [
    "initializing",
    "healthy",
    "attention",
    "review",
    "critical",
    "unavailable",
  ] as const;

  return (
    <Panel
      title="Signal and Status Language"
      description={
        "One canonical operational vocabulary across every AletheusOS application."
      }
    >
      <Grid
        minColumnWidth={170}
        gap="md"
      >
        {states.map(
          (status) => (
            <Surface
              key={status}
              variant="instrument"
              className="state-tile"
            >
              <Stack spacing="sm">
                <Signal
                  status={status}
                />

                <Badge
                  intent={
                    status === "healthy"
                      ? "healthy"
                      : status === "critical"
                        ? "critical"
                        : status === "attention"
                          || status === "review"
                            ? "attention"
                            : "neutral"
                  }
                >
                  {status}
                </Badge>
              </Stack>
            </Surface>
          ),
        )}
      </Grid>
    </Panel>
  );
}


function MeterGallery() {
  return (
    <Panel
      title="Professional Meter Language"
      description={
        "High-resolution instrumentation inspired by professional control surfaces."
      }
    >
      <Stack spacing="lg">
        {[34, 61, 82, 96].map(
          (value) => (
            <div
              key={value}
              className="meter-gallery-row"
            >
              <Text
                variant="telemetry"
                muted
              >
                SIGNAL {value.toFixed(1)}
              </Text>

              <Meter
                value={value}
                label={
                  `Signal meter ${value}`
                }
              />
            </div>
          ),
        )}
      </Stack>
    </Panel>
  );
}


function PreviewContent() {
  return (
    <main className="instrumentation-preview">
      <Stack spacing="2xl">
        <header className="instrumentation-header">
          <div>
            <Text
              as="div"
              variant="caption"
              muted
              className="instrumentation-eyebrow"
            >
              ALETHEUSOS™ · NIMBLE™
            </Text>

            <Text
              as="h1"
              variant="display"
              className="instrumentation-title"
            >
              Intelligence Instrumentation™
            </Text>

            <Text
              as="p"
              muted
              className="instrumentation-subtitle"
            >
              The constitutional visual language
              for observable, measurable, and
              professionally instrumented intelligence.
            </Text>
          </div>

          <div className="instrumentation-live">
            <span
              className="instrumentation-live-light"
            />

            SYSTEM LIVE
          </div>
        </header>

        <ReservedInstruments />

        <EngineGrid />

        <Grid
          columns="minmax(0, 1fr) minmax(0, 1fr)"
          gap="lg"
          className="gallery-grid"
        >
          <MeterGallery />
          <StateGallery />
        </Grid>

        <footer className="instrumentation-footer">
          <Text
            variant="telemetry"
            muted
          >
            Complex beneath. Clear above.
            Alive throughout.
          </Text>

          <Text
            variant="telemetry"
            muted
          >
            PREVIEW DATA · GENESIS 8
          </Text>
        </footer>
      </Stack>
    </main>
  );
}


export function IntelligenceInstrumentationShowcase() {
  return (
    <InstrumentationProvider
      instruments={
        canonicalInstrumentationFixtures
      }
    >
      <PreviewContent />
    </InstrumentationProvider>
  );
}
''',

    "src/nimble/showcase/instrumentation-preview.css": r'''
:root {
  color-scheme: dark;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}

* {
  box-sizing: border-box;
}

html,
body,
#instrumentation-root {
  margin: 0;
  min-height: 100%;
}

body {
  background:
    radial-gradient(
      circle at 18% -4%,
      rgba(217, 175, 72, 0.14),
      transparent 34rem
    ),
    radial-gradient(
      circle at 90% 12%,
      rgba(83, 166, 255, 0.09),
      transparent 30rem
    ),
    #080d16;
}

.instrumentation-preview {
  min-height: 100vh;
  padding:
    clamp(
      24px,
      4vw,
      64px
    );
}

.instrumentation-header {
  align-items: flex-start;
  display: flex;
  gap: 32px;
  justify-content: space-between;
}

.instrumentation-eyebrow {
  letter-spacing: 0.18em;
  margin-bottom: 10px !important;
}

.instrumentation-title {
  font-size:
    clamp(
      38px,
      6vw,
      74px
    ) !important;
  letter-spacing: -0.05em;
  line-height: 0.96 !important;
  max-width: 1040px;
}

.instrumentation-subtitle {
  font-size:
    clamp(
      15px,
      2vw,
      19px
    ) !important;
  margin-top: 18px !important;
  max-width: 760px;
}

.instrumentation-live {
  align-items: center;
  border:
    1px solid
    rgba(
      66,
      207,
      138,
      0.34
    );
  border-radius: 999px;
  color: #42cf8a;
  display: inline-flex;
  flex: none;
  font:
    600 11px/1
    "IBM Plex Mono",
    "SFMono-Regular",
    monospace;
  gap: 9px;
  letter-spacing: 0.12em;
  padding: 11px 15px;
}

.instrumentation-live-light {
  animation:
    instrumentation-pulse
    1.8s
    ease-in-out
    infinite;
  background: #42cf8a;
  border-radius: 50%;
  height: 7px;
  width: 7px;
}

.reserved-grid > *,
.gallery-grid > * {
  min-width: 0;
}

.telemetry-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
}

.state-tile {
  padding: 18px;
}

.meter-gallery-row {
  display: grid;
  gap: 9px;
}

.instrumentation-footer {
  align-items: center;
  border-top:
    1px solid
    rgba(
      152,
      162,
      179,
      0.14
    );
  display: flex;
  gap: 24px;
  justify-content: space-between;
  padding-top: 20px;
}

@keyframes instrumentation-pulse {
  0%,
  100% {
    box-shadow:
      0 0 0 0
      rgba(
        66,
        207,
        138,
        0
      );
    opacity: 0.7;
  }

  50% {
    box-shadow:
      0 0 0 8px
      rgba(
        66,
        207,
        138,
        0.08
      );
    opacity: 1;
  }
}

@media (max-width: 900px) {
  .reserved-grid,
  .gallery-grid {
    grid-template-columns:
      1fr !important;
  }

  .instrumentation-header,
  .instrumentation-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 560px) {
  .instrumentation-preview {
    padding: 18px;
  }

  .instrumentation-title {
    font-size: 39px !important;
  }
}

@media (
  prefers-reduced-motion:
  reduce
) {
  *,
  *::before,
  *::after {
    animation-duration:
      0.01ms !important;
    animation-iteration-count:
      1 !important;
    scroll-behavior:
      auto !important;
    transition-duration:
      0.01ms !important;
  }
}
''',

    "src/instrumentation-preview.tsx": r'''
import {
  StrictMode,
} from "react";

import {
  createRoot,
} from "react-dom/client";

import {
  IntelligenceInstrumentationShowcase,
} from "./nimble/showcase/IntelligenceInstrumentationShowcase";


const root =
  document.getElementById(
    "instrumentation-root",
  );


if (!root) {
  throw new Error(
    "Instrumentation preview root is missing.",
  );
}


createRoot(root).render(
  <StrictMode>
    <IntelligenceInstrumentationShowcase />
  </StrictMode>,
);
''',

    "instrumentation.html": r'''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />

    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0"
    />

    <meta
      name="theme-color"
      content="#080d16"
    />

    <title>
      AletheusOS Intelligence Instrumentation
    </title>
  </head>

  <body>
    <div id="instrumentation-root"></div>

    <script
      type="module"
      src="/src/instrumentation-preview.tsx"
    ></script>
  </body>
</html>
''',

    "vite.instrumentation.config.ts": r'''
import {
  resolve,
} from "node:path";

import react from "@vitejs/plugin-react";

import {
  defineConfig,
} from "vite";


export default defineConfig({
  plugins: [
    react(),
  ],

  build: {
    emptyOutDir: true,

    outDir:
      "dist-instrumentation",

    rollupOptions: {
      input: resolve(
        __dirname,
        "instrumentation.html",
      ),
    },
  },
});
''',
}


def write_new(
    path: Path,
    content: str,
) -> None:
    if path.exists():
        raise RuntimeError(
            "Refusing to overwrite existing file: "
            + str(path.relative_to(ROOT))
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content.strip() + "\n",
        encoding="utf-8",
    )


def patch_react_index() -> None:
    path = (
        REACT_ROOT
        / "index.ts"
    )

    export_line = (
        'export * from "./instrumentation";'
    )

    text = path.read_text(
        encoding="utf-8",
    )

    if export_line not in text:
        path.write_text(
            text.rstrip()
            + "\n\n"
            + export_line
            + "\n",
            encoding="utf-8",
        )


def patch_shell_manifest() -> None:
    path = (
        SHELL_ROOT
        / "package.json"
    )

    package = json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )

    scripts = package.setdefault(
        "scripts",
        {},
    )

    scripts[
        "build:instrumentation"
    ] = (
        "vite build "
        "--config "
        "vite.instrumentation.config.ts"
    )

    dependencies = package.setdefault(
        "dependencies",
        {},
    )

    dependencies.setdefault(
        "@aletheus/nimble-react",
        "0.1.0",
    )

    path.write_text(
        json.dumps(
            package,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def write_validator() -> None:
    write_new(
        VALIDATOR,
        r'''
#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REACT = (
    ROOT
    / "nimble/packages/react/src/instrumentation"
)

SHELL = (
    ROOT
    / "nimble/apps/platform-shell"
)

REPORT = (
    ROOT
    / "reports/nimble/experience/"
    "instrumentation-preview-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required_react = [
        "canonical.ts",
        "context.tsx",
        "contracts.ts",
        "fixtures.ts",
        "formatting.ts",
        "hooks.ts",
        "index.ts",
        "registry.ts",
        "validation.ts",
    ]

    required_shell = [
        "instrumentation.html",
        "vite.instrumentation.config.ts",
        "src/instrumentation-preview.tsx",
        "src/nimble/showcase/IntelligenceInstrumentationShowcase.tsx",
        "src/nimble/showcase/instrumentation-preview.css",
    ]

    for relative in required_react:
        if not (
            REACT / relative
        ).is_file():
            failures.append(
                "Missing instrumentation framework file: "
                + relative
            )

    for relative in required_shell:
        if not (
            SHELL / relative
        ).is_file():
            failures.append(
                "Missing instrumentation preview file: "
                + relative
            )

    combined = "\n".join(
        path.read_text(
            encoding="utf-8"
        )
        for root in [
            REACT,
            SHELL
            / "src/nimble/showcase",
        ]
        if root.exists()
        for path in root.rglob("*")
        if (
            path.is_file()
            and path.suffix
            in {
                ".ts",
                ".tsx",
                ".css",
            }
        )
    )

    concepts = [
        "Aletheus Index™",
        "THORᵡ",
        "Evidence Engine™",
        "Knowledge Engine™",
        "Reason Engine™",
        "Memory Engine™",
        "Bias Engine™",
        "Risk Engine™",
        "Predictive Engine™",
        "Individual Engine Grades",
        "InstrumentationRegistry",
        "Reserved instrument cannot be renamed",
        "prefers-reduced-motion",
    ]

    for concept in concepts:
        if concept not in combined:
            failures.append(
                "Missing instrumentation concept: "
                + concept
            )

    commands = [
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-react",
        ],
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-shell",
        ],
        [
            "npm",
            "run",
            "build:instrumentation",
            "--workspace",
            "@aletheus/nimble-shell",
        ],
    ]

    results: list[
        dict[str, object]
    ] = []

    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT / "nimble",
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )

        results.append(
            {
                "command":
                    " ".join(command),

                "returncode":
                    result.returncode,

                "stdout":
                    result.stdout.strip(),

                "stderr":
                    result.stderr.strip(),
            }
        )

        if result.returncode != 0:
            failures.append(
                "Command failed: "
                + " ".join(command)
            )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            {
                "schema_version":
                    "1.0",

                "generated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                "status":
                    status,

                "failures":
                    failures,

                "commands":
                    results,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(
        "NIMBLE™ INTELLIGENCE INSTRUMENTATION PREVIEW"
    )
    print("=" * 72)
    print(
        f"Failures: {len(failures)}"
    )
    print(
        f"Status: {status}"
    )
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(
            f"- {failure}"
        )

    if failures:
        for result in results:
            if result[
                "returncode"
            ] != 0:
                print()
                print(
                    result["command"]
                )
                print(
                    result["stdout"]
                )
                print(
                    result["stderr"]
                )

    return (
        0
        if status == "PASS"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )


def write_tests() -> None:
    write_new(
        TEST_FILE,
        r'''
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

INSTRUMENTATION = (
    ROOT
    / "nimble/packages/react/src/instrumentation"
)

SHOWCASE = (
    ROOT
    / "nimble/apps/platform-shell/src/nimble/"
    "showcase/IntelligenceInstrumentationShowcase.tsx"
)

CSS = SHOWCASE.with_name(
    "instrumentation-preview.css"
)


def read(
    relative: str,
) -> str:
    return (
        INSTRUMENTATION / relative
    ).read_text(
        encoding="utf-8"
    )


def test_instrumentation_is_exported() -> None:
    index = (
        ROOT
        / "nimble/packages/react/src/index.ts"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        'export * from "./instrumentation";'
        in index
    )


def test_reserved_instrument_names_are_canonical() -> None:
    canonical = read(
        "canonical.ts"
    )

    assert (
        '"Aletheus Index™"'
        in canonical
    )

    assert (
        '"THORᵡ"'
        in canonical
    )


def test_engine_identities_are_canonical() -> None:
    canonical = read(
        "canonical.ts"
    )

    for engine in [
        "Evidence Engine™",
        "Knowledge Engine™",
        "Reason Engine™",
        "Memory Engine™",
        "Bias Engine™",
        "Risk Engine™",
        "Predictive Engine™",
    ]:
        assert engine in canonical


def test_registry_rejects_duplicates() -> None:
    registry = read(
        "registry.ts"
    )

    assert (
        "Duplicate instrument"
        in registry
    )


def test_reserved_identity_is_protected() -> None:
    validation = read(
        "validation.ts"
    )

    assert (
        "Reserved instrument cannot be renamed"
        in validation
    )


def test_formatting_is_deterministic() -> None:
    formatting = read(
        "formatting.ts"
    )

    assert (
        'return value.toFixed(1);'
        in formatting
    )

    assert (
        'toFixed(1)}%`'
        in formatting
    )


def test_showcase_separates_top_level_instruments() -> None:
    text = SHOWCASE.read_text(
        encoding="utf-8"
    )

    assert (
        "AletheusIndexInstrument"
        in text
    )

    assert (
        "ThorxInstrument"
        in text
    )

    assert (
        "Council Consensus"
        not in text
    )


def test_showcase_contains_engine_grid() -> None:
    text = SHOWCASE.read_text(
        encoding="utf-8"
    )

    assert (
        "ENGINE_INSTRUMENT_IDS"
        in text
    )

    assert (
        "Individual Engine Grades"
        in text
    )


def test_preview_is_responsive_and_accessible() -> None:
    css = CSS.read_text(
        encoding="utf-8"
    )

    assert (
        "@media (max-width: 900px)"
        in css
    )

    assert (
        "prefers-reduced-motion"
        in css
    )


def test_instrumentation_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_instrumentation_preview.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=360,
    )

    assert result.returncode == 0, (
        result.stdout
        + result.stderr
    )

    assert (
        "Status: PASS"
        in result.stdout
    )
''',
    )


def run(
    command: list[str],
) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            result.returncode
        )


def main() -> int:
    for dependency in (
        REQUIRED_DEPENDENCIES
    ):
        if not dependency.is_file():
            raise RuntimeError(
                "Missing required dependency: "
                + str(
                    dependency.relative_to(
                        ROOT
                    )
                )
            )

    if INSTRUMENTATION_ROOT.exists():
        existing = [
            path
            for path
            in INSTRUMENTATION_ROOT.rglob(
                "*"
            )
            if path.is_file()
        ]

        if existing:
            raise RuntimeError(
                "Refusing to overwrite existing "
                "instrumentation framework."
            )

    for relative, content in (
        INSTRUMENTATION_FILES.items()
    ):
        write_new(
            INSTRUMENTATION_ROOT
            / relative,
            content,
        )

    for relative, content in (
        SHELL_FILES.items()
    ):
        write_new(
            SHELL_ROOT / relative,
            content,
        )

    patch_react_index()
    patch_shell_manifest()
    write_validator()
    write_tests()

    run(
        [
            "python",
            "-m",
            "py_compile",
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            "-m",
            "pytest",
            "-q",
            str(TEST_FILE),
        ]
    )

    run(
        [
            "python",
            "-m",
            "nimble.orchestrator",
        ]
    )

    print()
    print("=" * 72)
    print(
        "INTELLIGENCE INSTRUMENTATION PREVIEW BUILD COMPLETE"
    )
    print("=" * 72)
    print(
        "Run preview:"
    )
    print(
        "cd nimble && "
        "npm run dev --workspace "
        "@aletheus/nimble-shell"
    )
    print(
        "Open:"
    )
    print(
        "http://localhost:5173/"
        "instrumentation.html"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
