import { motion } from "motion/react";

import { useRuntimeOverview } from "../api/runtimeQueries";
import { EmptyState } from "../components/feedback/EmptyState";
import { RoutePending } from "../components/feedback/RoutePending";
import { useNimble } from "../providers/NimbleProvider";

export function OverviewRoute() {
  const {
    data,
    error,
    isPending,
    isFetching,
    refetch,
  } = useRuntimeOverview();

  const {
    setCommandOpen,
    notify,
  } = useNimble();

  if (isPending) {
    return (
      <RoutePending label="Reconciling AletheusOS state" />
    );
  }

  if (error) {
    throw error;
  }

  if (!data) {
    return (
      <EmptyState
        title="No runtime overview is available"
        description="The runtime returned no overview payload."
      />
    );
  }

  const fixtureMode =
    data.health.truth.state === "development_fixture";

  return (
    <main id="nimble-main" className="nimble-main">
      <motion.section
        className="nimble-hero"
        initial={{
          opacity: 0,
          y: 18,
        }}
        animate={{
          opacity: 1,
          y: 0,
        }}
      >
        <div>
          <p className="nimble-eyebrow">
            AletheusOS · Executive Intelligence
          </p>

          <h1>
            Good afternoon, <span>Jeremey.</span>
          </h1>

          <p>
            {data.health.summary}
          </p>

          {fixtureMode && (
            <div className="nimble-source-disclosure">
              <strong>Development fixture</strong>
              <span>
                Live runtime data is not currently connected.
              </span>
            </div>
          )}
        </div>

        <div className="nimble-hero__actions">
          <button
            className="nimble-button nimble-button--primary"
            type="button"
            onClick={() => {
              setCommandOpen(true);
            }}
          >
            ✦ Begin a command
          </button>

          <button
            className="nimble-button nimble-button--secondary"
            type="button"
            disabled={isFetching}
            onClick={() => {
              void refetch().then(() => {
                notify(
                  "Runtime refreshed",
                  "The current overview query completed.",
                );
              });
            }}
          >
            {isFetching ? "Refreshing…" : "Refresh state"}
          </button>
        </div>
      </motion.section>

      <section
        className="nimble-metrics"
        aria-label="Runtime metrics"
      >
        <MetricCard
          label="Runtime integrity"
          value={`${data.health.passingChecks}/${data.health.totalChecks}`}
          detail={`${data.health.warningCount} warnings`}
        />

        <MetricCard
          label="Active missions"
          value={String(
            data.missions.filter(
              (mission) => mission.state === "active",
            ).length,
          )}
          detail={`${data.missions.length} total missions`}
        />

        <MetricCard
          label="Runtime state"
          value={data.health.state}
          detail={
            fixtureMode
              ? "Verified fixture, not live state"
              : "Live AletheusOS runtime"
          }
        />
      </section>

      <section className="nimble-workspace-grid">
        <motion.article
          className="nimble-panel nimble-panel--intelligence"
          layout
        >
          <header className="nimble-panel__header">
            <div>
              <p className="nimble-panel__eyebrow">
                Principle X
              </p>
              <h2>Runtime truth</h2>
            </div>

            <strong className="nimble-confidence">
              {
                data.health.truth.confidence
                  ? `${Math.round(
                      data.health.truth.confidence.value * 100,
                    )}%`
                  : "Unknown"
              }
            </strong>
          </header>

          <p className="nimble-truth-summary">
            {data.health.truth.explanation}
          </p>

          <div className="nimble-runtime-checks">
            {data.health.checks.map((check) => (
              <article key={check.id}>
                <span
                  className={`nimble-status-dot ${
                    check.state === "healthy"
                      ? "nimble-status-dot--success"
                      : "nimble-status-dot--active"
                  }`}
                  aria-hidden="true"
                />

                <div>
                  <strong>{check.name}</strong>
                  <p>{check.detail}</p>
                </div>

                <time dateTime={check.checkedAt}>
                  {check.latencyMs
                    ? `${check.latencyMs} ms`
                    : "Verified"}
                </time>
              </article>
            ))}
          </div>
        </motion.article>

        <motion.article
          className="nimble-panel"
          layout
        >
          <header className="nimble-panel__header">
            <div>
              <p className="nimble-panel__eyebrow">
                Operations
              </p>
              <h2>Active missions</h2>
            </div>
          </header>

          <div className="nimble-mission-list">
            {data.missions.map((mission) => (
              <button
                key={mission.id}
                className="nimble-mission"
                type="button"
                onClick={() => {
                  notify(
                    mission.name,
                    `${mission.description} — ${mission.progress}% complete.`,
                  );
                }}
              >
                <span className="nimble-mission__icon">
                  {mission.name.at(0)}
                </span>

                <span className="nimble-mission__body">
                  <strong>{mission.name}</strong>
                  <small>
                    {mission.state} · {mission.description}
                  </small>

                  <span className="nimble-progress">
                    <span
                      style={{
                        width: `${mission.progress}%`,
                      }}
                    />
                  </span>
                </span>

                <span>{mission.progress}%</span>
              </button>
            ))}
          </div>
        </motion.article>

        <motion.article
          className="nimble-panel nimble-panel--wide"
          layout
        >
          <header className="nimble-panel__header">
            <div>
              <p className="nimble-panel__eyebrow">
                Provenance
              </p>
              <h2>Current evidence</h2>
            </div>
          </header>

          <div className="nimble-provenance-list">
            {data.health.truth.provenance?.map((source) => (
              <article key={source.sourceId}>
                <strong>{source.label}</strong>
                <span>{source.sourceType}</span>
                <time dateTime={source.observedAt}>
                  {source.observedAt
                    ? new Date(source.observedAt).toLocaleString()
                    : "Observation time unavailable"}
                </time>
              </article>
            ))}

            {!data.health.truth.provenance?.length && (
              <EmptyState
                title="No provenance disclosed"
                description="The runtime response did not include evidence sources."
              />
            )}
          </div>
        </motion.article>
      </section>
    </main>
  );
}

function MetricCard({
  label,
  value,
  detail,
}: {
  readonly label: string;
  readonly value: string;
  readonly detail: string;
}) {
  return (
    <motion.article
      className="nimble-metric"
      whileHover={{
        y: -4,
        scale: 1.01,
      }}
    >
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{detail}</p>
    </motion.article>
  );
}
