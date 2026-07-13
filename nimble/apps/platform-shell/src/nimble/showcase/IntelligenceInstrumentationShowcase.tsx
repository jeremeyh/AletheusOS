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
