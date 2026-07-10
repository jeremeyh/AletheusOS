import { AnimatePresence, motion } from "motion/react";

import { useNimble } from "../providers/NimbleProvider";

export function TruthInspector() {
  const {
    inspectorOpen,
    toggleInspector,
    reset,
  } = useNimble();

  return (
    <AnimatePresence initial={false}>
      {inspectorOpen && (
        <motion.aside
          className="nimble-inspector"
          aria-label="Principle X truth inspector"
          initial={{
            width: 0,
            opacity: 0,
            x: 40,
          }}
          animate={{
            width: 352,
            opacity: 1,
            x: 0,
          }}
          exit={{
            width: 0,
            opacity: 0,
            x: 40,
          }}
          transition={{
            type: "spring",
            stiffness: 180,
            damping: 28,
            mass: 1.2,
          }}
        >
          <header className="nimble-inspector__header">
            <div>
              <p className="nimble-panel__eyebrow">
                Principle X
              </p>
              <h2>System truth</h2>
            </div>

            <button
              className="nimble-icon-button"
              type="button"
              aria-label="Close truth inspector"
              onClick={toggleInspector}
            >
              ×
            </button>
          </header>

          <section className="nimble-truth-card">
            <header>
              <span>Current state</span>
              <strong className="nimble-confidence">
                Verified
              </strong>
            </header>

            <dl>
              <div>
                <dt>Runtime</dt>
                <dd>Stable</dd>
              </div>
              <div>
                <dt>Tests</dt>
                <dd>246 / 246</dd>
              </div>
              <div>
                <dt>Warnings</dt>
                <dd>0</dd>
              </div>
              <div>
                <dt>Known uncertainty</dt>
                <dd>Live API integration</dd>
              </div>
            </dl>
          </section>

          <section className="nimble-inspector__section">
            <h3>Why this state exists</h3>
            <p>
              The React production shell now inherits Nimble’s
              architecture, token, motion, interaction, workspace,
              accessibility, and transparency contracts.
            </p>
          </section>

          <section className="nimble-inspector__section">
            <h3>Next consequence</h3>
            <p>
              Static platform data will be replaced by typed runtime
              adapters and route-owned server state.
            </p>
          </section>

          <section className="nimble-inspector__section">
            <h3>Reversibility</h3>
            <p>
              Theme, navigation, inspector, command, and local shell
              preferences can be reset without affecting runtime state.
            </p>

            <button
              className="nimble-button nimble-button--secondary"
              type="button"
              onClick={reset}
            >
              Reset shell state
            </button>
          </section>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
