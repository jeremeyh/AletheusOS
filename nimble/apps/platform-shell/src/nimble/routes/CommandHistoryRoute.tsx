import { motion } from "motion/react";

import {
  useCommandHistory,
} from "../api/commandQueries";
import type {
  CommandExecution,
} from "../api/commandTypes";
import { EmptyState } from "../components/feedback/EmptyState";
import { RoutePending } from "../components/feedback/RoutePending";

export function CommandHistoryRoute() {
  const {
    data,
    error,
    isPending,
    isFetching,
    refetch,
  } = useCommandHistory();

  if (isPending) {
    return (
      <RoutePending label="Loading command audit history" />
    );
  }

  if (error) {
    throw error;
  }

  const executions = [...(data ?? [])].sort(
    (left, right) =>
      new Date(right.executed_at).getTime()
      - new Date(left.executed_at).getTime(),
  );

  return (
    <main id="nimble-main" className="nimble-main">
      <section className="nimble-route-header">
        <div>
          <p className="nimble-eyebrow">
            Governance · Command Gateway
          </p>

          <h1>Command audit history</h1>

          <p>
            Every bounded execution returned by the command
            gateway, including failures, reversals, and results.
          </p>
        </div>

        <button
          className="nimble-button nimble-button--secondary"
          type="button"
          disabled={isFetching}
          onClick={() => {
            void refetch();
          }}
        >
          {isFetching ? "Refreshing…" : "Refresh history"}
        </button>
      </section>

      {executions.length === 0 ? (
        <EmptyState
          title="No commands have been executed"
          description="Previewed commands do not appear here until execution is attempted."
        />
      ) : (
        <section className="nimble-history-list">
          {executions.map((execution, index) => (
            <CommandHistoryItem
              key={execution.execution_id}
              execution={execution}
              index={index}
            />
          ))}
        </section>
      )}
    </main>
  );
}

function CommandHistoryItem({
  execution,
  index,
}: {
  readonly execution: CommandExecution;
  readonly index: number;
}) {
  return (
    <motion.article
      className="nimble-history-item"
      initial={{
        opacity: 0,
        y: 12,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      transition={{
        delay: Math.min(index * 0.04, 0.28),
      }}
    >
      <header className="nimble-history-item__header">
        <div>
          <p className="nimble-panel__eyebrow">
            {execution.command_id}
          </p>

          <h2>
            {formatCommandName(execution.command_id)}
          </h2>
        </div>

        <span
          className={`nimble-execution-state nimble-execution-state--${execution.state}`}
        >
          {execution.state}
        </span>
      </header>

      <dl className="nimble-history-metadata">
        <div>
          <dt>Execution ID</dt>
          <dd>{execution.execution_id}</dd>
        </div>

        <div>
          <dt>Requested by</dt>
          <dd>{execution.requested_by}</dd>
        </div>

        <div>
          <dt>Executed</dt>
          <dd>
            <time dateTime={execution.executed_at}>
              {new Date(
                execution.executed_at,
              ).toLocaleString()}
            </time>
          </dd>
        </div>

        <div>
          <dt>Authorization</dt>
          <dd>
            {execution.authorization_id
              ? "Authorized"
              : "Not required"}
          </dd>
        </div>

        <div>
          <dt>Reversible</dt>
          <dd>
            {execution.reversible
              ? "Supported"
              : "No"}
          </dd>
        </div>

        <div>
          <dt>Reversal available</dt>
          <dd>
            {execution.reversal_token
              ? "Yes"
              : "No"}
          </dd>
        </div>
      </dl>

      {execution.failure ? (
        <section className="nimble-history-failure">
          <h3>Failure</h3>
          <p>{execution.failure}</p>
        </section>
      ) : (
        <section>
          <h3>Bounded result</h3>

          <pre className="nimble-command-json">
            {JSON.stringify(
              execution.result,
              null,
              2,
            )}
          </pre>
        </section>
      )}
    </motion.article>
  );
}

function formatCommandName(
  commandId: string,
): string {
  return commandId
    .split(".")
    .map((part) =>
      part.replace(
        /\b\w/g,
        (character) =>
          character.toUpperCase(),
      )
    )
    .join(" · ");
}
