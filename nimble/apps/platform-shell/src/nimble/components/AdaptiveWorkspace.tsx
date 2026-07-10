import { motion } from "motion/react";

import { missions } from "../data/shellData";
import { useNimble } from "../providers/NimbleProvider";

const briefItems = [
  {
    id: "foundation",
    title: "Nimble foundation is structurally valid",
    detail:
      "Architecture, tokens, interaction, accessibility, workspace, and personalization contracts are aligned.",
    confidence: "99%",
  },
  {
    id: "renderer",
    title: "Production rendering boundary is active",
    detail:
      "React, TypeScript, Vite, Motion, Radix, routing, and query boundaries are established.",
    confidence: "97%",
  },
  {
    id: "inheritance",
    title: "Applications can inherit without architectural forks",
    detail:
      "Card Hawk and future products can extend Nimble through bounded application surfaces.",
    confidence: "95%",
  },
] as const;

export function AdaptiveWorkspace() {
  const {
    setCommandOpen,
    notify,
  } = useNimble();

  return (
    <main id="nimble-main" className="nimble-main">
      <motion.section
        className="nimble-hero"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div>
          <p className="nimble-eyebrow">
            AletheusOS · Executive Intelligence
          </p>

          <h1>
            Good afternoon, <span>Jeremey.</span>
          </h1>

          <p>
            The runtime is stable, validation systems are clear,
            and the Nimble production experience layer is online.
          </p>
        </div>

        <button
          className="nimble-button nimble-button--primary"
          type="button"
          onClick={() => {
            setCommandOpen(true);
          }}
        >
          ✦ Begin a command
        </button>
      </motion.section>

      <section
        className="nimble-metrics"
        aria-label="Platform metrics"
      >
        <MetricCard
          label="Runtime integrity"
          value="100%"
          detail="246 tests passing · zero warnings"
        />

        <MetricCard
          label="Experience engines"
          value="10"
          detail="All core contracts registered"
        />

        <MetricCard
          label="Decision confidence"
          value="97%"
          detail="Architecture boundaries aligned"
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
                Intelligence
              </p>
              <h2>Executive brief</h2>
            </div>

            <button
              className="nimble-icon-button"
              type="button"
              aria-label="Refresh executive brief"
              onClick={() => {
                notify(
                  "Synthesis refreshed",
                  "The executive brief is current and reconciled.",
                );
              }}
            >
              ↻
            </button>
          </header>

          <div className="nimble-intelligence-state">
            <span className="nimble-intelligence-state__core">
              <i />
              <i />
              <i />
            </span>

            <div>
              <strong>System synthesis complete</strong>
              <p>
                Runtime, governance, mission, and experience states
                have been reconciled.
              </p>
            </div>
          </div>

          <div className="nimble-brief">
            {briefItems.map((item, index) => (
              <article key={item.id}>
                <span>{String(index + 1).padStart(2, "0")}</span>

                <div>
                  <h3>{item.title}</h3>
                  <p>{item.detail}</p>
                </div>

                <strong className="nimble-confidence">
                  {item.confidence}
                </strong>
              </article>
            ))}
          </div>
        </motion.article>

        <motion.article className="nimble-panel" layout>
          <header className="nimble-panel__header">
            <div>
              <p className="nimble-panel__eyebrow">
                Operations
              </p>
              <h2>Active missions</h2>
            </div>
          </header>

          <div className="nimble-mission-list">
            {missions.map((mission) => (
              <button
                key={mission.id}
                className="nimble-mission"
                type="button"
                onClick={() => {
                  notify(
                    mission.name,
                    `${mission.description}: ${mission.progress}% complete.`,
                  );
                }}
              >
                <span className="nimble-mission__icon">
                  {mission.name[0]}
                </span>

                <span className="nimble-mission__body">
                  <strong>{mission.name}</strong>
                  <small>{mission.description}</small>
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
                Live state
              </p>
              <h2>System activity</h2>
            </div>
          </header>

          <div className="nimble-activity">
            {[
              "Foundation validation completed",
              "Production TypeScript boundary passed",
              "Runtime regression remained clean",
              "Application inheritance activated",
            ].map((activity, index) => (
              <motion.div
                key={activity}
                className="nimble-activity__item"
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{
                  delay: index * 0.08,
                }}
              >
                <span
                  className="nimble-status-dot nimble-status-dot--active"
                  aria-hidden="true"
                />
                <strong>{activity}</strong>
                <time>{index === 0 ? "Now" : `${index * 2}m`}</time>
              </motion.div>
            ))}
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
      transition={{
        type: "spring",
        stiffness: 420,
        damping: 34,
      }}
    >
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{detail}</p>
    </motion.article>
  );
}
