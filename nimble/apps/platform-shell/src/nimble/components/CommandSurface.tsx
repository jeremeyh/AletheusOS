import * as Dialog from "@radix-ui/react-dialog";
import { AnimatePresence, motion } from "motion/react";
import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useCommandDefinitions,
} from "../api/commandQueries";
import {
  evaluateCommandEligibility,
} from "../api/commandEligibility";
import {
  useCurrentPrincipal,
} from "../api/identityQueries";
import {
  useCommandTransaction,
} from "../api/useCommandTransaction";
import type {
  CommandDefinition,
} from "../api/commandTypes";
import { useNimble } from "../providers/NimbleProvider";

export function CommandSurface() {
  const {
    commandOpen,
    setCommandOpen,
    notify,
  } = useNimble();

  const {
    data: commands,
    error,
    isPending,
  } = useCommandDefinitions();

  const {
    data: principal,
    error: principalError,
    isPending: principalPending,
  } = useCurrentPrincipal();

  const transaction =
    useCommandTransaction();

  const [query, setQuery] = useState("");
  const [selectedArguments, setSelectedArguments] =
    useState<Record<string, unknown>>({});

  useEffect(() => {
    function handleShortcut(event: KeyboardEvent) {
      if (
        (event.metaKey || event.ctrlKey)
        && event.key.toLowerCase() === "k"
      ) {
        event.preventDefault();
        setCommandOpen(!commandOpen);
      }
    }

    window.addEventListener(
      "keydown",
      handleShortcut,
    );

    return () => {
      window.removeEventListener(
        "keydown",
        handleShortcut,
      );
    };
  }, [commandOpen, setCommandOpen]);

  useEffect(() => {
    if (!commandOpen) {
      window.setTimeout(() => {
        transaction.reset();
        setQuery("");
        setSelectedArguments({});
      }, 180);
    }
  }, [
    commandOpen,
    transaction.reset,
  ]);

  const filteredCommands = useMemo(() => {
    if (!commands) {
      return [];
    }

    const normalized = query
      .trim()
      .toLowerCase();

    if (!normalized) {
      return commands;
    }

    return commands.filter((command) => {
      const searchable = [
        command.name,
        command.description,
        command.id,
        ...command.effects,
      ]
        .join(" ")
        .toLowerCase();

      return searchable.includes(normalized);
    });
  }, [
    commands,
    query,
  ]);

  async function selectCommand(
    command: CommandDefinition,
  ) {
    const argumentsValue =
      createDefaultArguments(command);

    setSelectedArguments(argumentsValue);

    try {
      await transaction.begin(
        command,
        argumentsValue,
      );
    } catch {
      notify(
        "Preview failed",
        "The command gateway could not create a preview.",
      );
    }
  }

  async function executePreview() {
    try {
      const execution =
        await transaction.approveAndExecute();

      notify(
        execution.state === "executed"
          ? "Command executed"
          : "Command failed",
        execution.state === "executed"
          ? "The governed execution completed and was recorded."
          : execution.failure
            ?? "The command did not complete.",
      );
    } catch {
      notify(
        "Execution failed",
        "The governed command transaction did not complete.",
      );
    }
  }

  async function reverseExecution() {
    try {
      await transaction.reverse();

      notify(
        "Command reversed",
        "The registered reversal handler restored the prior state.",
      );
    } catch {
      notify(
        "Reversal failed",
        "The command could not be reversed.",
      );
    }
  }

  return (
    <Dialog.Root
      open={commandOpen}
      onOpenChange={setCommandOpen}
    >
      <Dialog.Portal>
        <AnimatePresence>
          {commandOpen && (
            <>
              <Dialog.Overlay asChild>
                <motion.div
                  className="nimble-command__overlay"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                />
              </Dialog.Overlay>

              <Dialog.Content asChild>
                <motion.section
                  className="nimble-command nimble-command--governed"
                  aria-describedby="nimble-command-description"
                  initial={{
                    opacity: 0,
                    y: 28,
                    scale: 0.96,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                    scale: 1,
                  }}
                  exit={{
                    opacity: 0,
                    y: 18,
                    scale: 0.98,
                  }}
                  transition={{
                    type: "spring",
                    stiffness: 260,
                    damping: 24,
                  }}
                >
                  <header className="nimble-command__header">
                    <span aria-hidden="true">✦</span>

                    <Dialog.Title>
                      Governed command gateway
                    </Dialog.Title>

                    <Dialog.Close asChild>
                      <button
                        className="nimble-icon-button"
                        type="button"
                        aria-label="Close command surface"
                      >
                        ×
                      </button>
                    </Dialog.Close>
                  </header>

                  <Dialog.Description
                    id="nimble-command-description"
                    className="visually-hidden"
                  >
                    Discover, preview, authorize, execute,
                    and reverse bounded AletheusOS commands.
                  </Dialog.Description>

                  {transaction.stage === "idle" && (
                    <CommandDiscovery
                      query={query}
                      setQuery={setQuery}
                      commands={filteredCommands}
                      isPending={isPending}
                      error={error}
                      principal={principal}
                      principalError={principalError}
                      principalPending={principalPending}
                      onSelect={selectCommand}
                    />
                  )}

                  {transaction.stage === "previewing" && (
                    <CommandProgress
                      title="Creating preview"
                      detail="The gateway is resolving risk, effects, authorization, and reversibility."
                    />
                  )}

                  {transaction.preview && (
                    <>
                      {transaction.stage === "preview" && (
                        <CommandPreviewPanel
                          preview={transaction.preview}
                          argumentsValue={
                            selectedArguments
                          }
                          onExecute={
                            executePreview
                          }
                          onCancel={
                            transaction.reset
                          }
                        />
                      )}

                      {(
                        transaction.stage
                          === "authorizing"
                        || transaction.stage
                          === "executing"
                      ) && (
                        <CommandProgress
                          title={
                            transaction.stage
                              === "authorizing"
                              ? "Authorizing command"
                              : "Executing bounded handler"
                          }
                          detail={
                            transaction.stage
                              === "authorizing"
                              ? "The authorization is being bound to this exact preview."
                              : "The command is executing through its registered handler."
                          }
                        />
                      )}
                    </>
                  )}

                  {transaction.execution
                    && transaction.stage === "complete"
                    && (
                      <CommandResultPanel
                        execution={
                          transaction.execution
                        }
                        onReverse={
                          reverseExecution
                        }
                        onDone={() => {
                          transaction.reset();
                          setCommandOpen(false);
                        }}
                      />
                    )}

                  {transaction.stage === "reversing" && (
                    <CommandProgress
                      title="Reversing command"
                      detail="The registered reversal handler is restoring the prior state."
                    />
                  )}

                  {transaction.execution
                    && transaction.stage === "reversed"
                    && (
                      <CommandResultPanel
                        execution={
                          transaction.execution
                        }
                        onDone={() => {
                          transaction.reset();
                          setCommandOpen(false);
                        }}
                      />
                    )}

                  {transaction.stage === "failed" && (
                    <CommandFailurePanel
                      failure={
                        transaction.failure
                        ?? "The command transaction failed."
                      }
                      onReset={
                        transaction.reset
                      }
                    />
                  )}
                </motion.section>
              </Dialog.Content>
            </>
          )}
        </AnimatePresence>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

function CommandDiscovery({
  query,
  setQuery,
  commands,
  isPending,
  error,
  principal,
  principalError,
  principalPending,
  onSelect,
}: {
  readonly query: string;
  readonly setQuery: (value: string) => void;
  readonly commands:
    readonly CommandDefinition[];
  readonly isPending: boolean;
  readonly error: Error | null;
  readonly principal:
    import("../api/identityTypes").CurrentPrincipal | undefined;
  readonly principalError: Error | null;
  readonly principalPending: boolean;
  readonly onSelect: (
    command: CommandDefinition,
  ) => void;
}) {
  return (
    <>
      <input
        className="nimble-command__input"
        autoFocus
        value={query}
        onChange={(event) => {
          setQuery(event.target.value);
        }}
        placeholder="Search registered commands…"
      />

      <div className="nimble-command__context">
        <span>
          Mode: Preview before execute
        </span>
        <span>
          Source: Governed command registry
        </span>
      </div>

      <div className="nimble-command__results">
        {isPending && (
          <p className="nimble-command__empty">
            Loading registered commands…
          </p>
        )}

        {error && (
          <p className="nimble-command__failure">
            The command registry could not be reached:
            {" "}
            {error.message}
          </p>
        )}

        {principalPending && (
          <p className="nimble-command__empty">
            Resolving command identity…
          </p>
        )}

        {principalError && (
          <p className="nimble-command__failure">
            Identity could not be resolved:
            {" "}
            {principalError.message}
          </p>
        )}

        {!isPending
          && !error
          && principal
          && commands.map((command) => {
            const eligibility =
              evaluateCommandEligibility(
                command,
                principal,
              );

            return (
            <button
              key={command.id}
              type="button"
              className={
                eligibility.eligible
                  ? undefined
                  : "is-command-denied"
              }
              aria-disabled={!eligibility.eligible}
              onClick={() => {
                if (eligibility.eligible) {
                  onSelect(command);
                }
              }}
            >
              <span className="nimble-command__result-icon">
                {command.risk === "read_only"
                  ? "◉"
                  : "◇"}
              </span>

              <span>
                <strong>{command.name}</strong>
                <small>
                  {command.description}
                </small>
              </span>

              <span className="nimble-command-access">
                <span
                  className={
                    `nimble-risk nimble-risk--${command.risk}`
                  }
                >
                  {formatRisk(command.risk)}
                </span>

                <small>
                  {eligibility.eligible
                    ? "Allowed"
                    : eligibility.reason}
                </small>
              </span>
            </button>
            );
          })}

        {!isPending
          && !error
          && commands.length === 0
          && (
            <p className="nimble-command__empty">
              No registered command matches this search.
            </p>
          )}
      </div>
    </>
  );
}

function CommandPreviewPanel({
  preview,
  argumentsValue,
  onExecute,
  onCancel,
}: {
  readonly preview: {
    readonly name: string;
    readonly description: string;
    readonly risk: string;
    readonly effects: readonly string[];
    readonly required_entitlements?: readonly string[];
    readonly reversible: boolean;
    readonly authorization_required: boolean;
    readonly expires_at: string;
  };
  readonly argumentsValue:
    Readonly<Record<string, unknown>>;
  readonly onExecute: () => void;
  readonly onCancel: () => void;
}) {
  return (
    <div className="nimble-command-transaction">
      <header>
        <p className="nimble-panel__eyebrow">
          Principle X · Preview
        </p>
        <h2>{preview.name}</h2>
        <p>{preview.description}</p>
      </header>

      <section className="nimble-command-disclosure">
        <DisclosureRow
          label="Risk"
          value={formatRisk(preview.risk)}
        />
        <DisclosureRow
          label="Authorization"
          value={
            preview.authorization_required
              ? "Required"
              : "Not required"
          }
        />
        <DisclosureRow
          label="Reversible"
          value={
            preview.reversible
              ? "Yes"
              : "No"
          }
        />
        <DisclosureRow
          label="Preview expires"
          value={
            new Date(
              preview.expires_at,
            ).toLocaleTimeString()
          }
        />
      </section>

      <section>
        <h3>Required entitlements</h3>

        <div className="nimble-principal-tags">
          {(preview.required_entitlements ?? []).length
            ? (preview.required_entitlements ?? []).map(
                (entitlement) => (
                  <span key={entitlement}>
                    {entitlement}
                  </span>
                ),
              )
            : (
                <span>None</span>
              )}
        </div>
      </section>

      <section>
        <h3>Expected effects</h3>
        <ul className="nimble-effect-list">
          {preview.effects.map((effect) => (
            <li key={effect}>{effect}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Arguments</h3>
        <pre className="nimble-command-json">
          {JSON.stringify(
            argumentsValue,
            null,
            2,
          )}
        </pre>
      </section>

      <footer className="nimble-command-actions">
        <button
          className="nimble-button nimble-button--secondary"
          type="button"
          onClick={onCancel}
        >
          Cancel
        </button>

        <button
          className="nimble-button nimble-button--primary"
          type="button"
          onClick={onExecute}
        >
          {preview.authorization_required
            ? "Authorize and execute"
            : "Execute command"}
        </button>
      </footer>
    </div>
  );
}

function CommandProgress({
  title,
  detail,
}: {
  readonly title: string;
  readonly detail: string;
}) {
  return (
    <div className="nimble-command-progress">
      <motion.span
        animate={{ rotate: 360 }}
        transition={{
          duration: 1.4,
          repeat: Number.POSITIVE_INFINITY,
          ease: "linear",
        }}
        aria-hidden="true"
      >
        ✦
      </motion.span>

      <strong>{title}</strong>
      <p>{detail}</p>
    </div>
  );
}

function CommandResultPanel({
  execution,
  onReverse,
  onDone,
}: {
  readonly execution: {
    readonly execution_id: string;
    readonly state: string;
    readonly result:
      Readonly<Record<string, unknown>>;
    readonly reversible: boolean;
    readonly reversal_token: string | null;
    readonly executed_at: string;
  };
  readonly onReverse?: () => void;
  readonly onDone: () => void;
}) {
  const canReverse = Boolean(
    onReverse
    && execution.reversible
    && execution.reversal_token
    && execution.state === "executed",
  );

  return (
    <div className="nimble-command-transaction">
      <header>
        <p className="nimble-panel__eyebrow">
          Principle X · Confirmed
        </p>

        <h2>
          {execution.state === "reversed"
            ? "Command reversed"
            : "Command executed"}
        </h2>

        <p>
          The transaction was recorded by the command
          gateway and returned a bounded result.
        </p>
      </header>

      <section className="nimble-command-disclosure">
        <DisclosureRow
          label="State"
          value={execution.state}
        />
        <DisclosureRow
          label="Execution"
          value={execution.execution_id}
        />
        <DisclosureRow
          label="Executed"
          value={
            new Date(
              execution.executed_at,
            ).toLocaleString()
          }
        />
        <DisclosureRow
          label="Reversible"
          value={
            canReverse
              ? "Available"
              : "Unavailable"
          }
        />
      </section>

      <section>
        <h3>Result</h3>
        <pre className="nimble-command-json">
          {JSON.stringify(
            execution.result,
            null,
            2,
          )}
        </pre>
      </section>

      <footer className="nimble-command-actions">
        {canReverse && (
          <button
            className="nimble-button nimble-button--secondary"
            type="button"
            onClick={onReverse}
          >
            Reverse command
          </button>
        )}

        <button
          className="nimble-button nimble-button--primary"
          type="button"
          onClick={onDone}
        >
          Done
        </button>
      </footer>
    </div>
  );
}

function CommandFailurePanel({
  failure,
  onReset,
}: {
  readonly failure: string;
  readonly onReset: () => void;
}) {
  return (
    <div className="nimble-command-transaction">
      <header>
        <p className="nimble-panel__eyebrow">
          Principle X · Failure disclosed
        </p>
        <h2>Command transaction failed</h2>
      </header>

      <section className="nimble-command-failure">
        <h3>What happened</h3>
        <p>{failure}</p>
      </section>

      <section>
        <h3>Impact</h3>
        <p>
          The command did not produce a confirmed successful
          execution. No success state is being inferred.
        </p>
      </section>

      <footer className="nimble-command-actions">
        <button
          className="nimble-button nimble-button--primary"
          type="button"
          onClick={onReset}
        >
          Return to commands
        </button>
      </footer>
    </div>
  );
}

function DisclosureRow({
  label,
  value,
}: {
  readonly label: string;
  readonly value: string;
}) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}

function createDefaultArguments(
  command: CommandDefinition,
): Record<string, unknown> {
  if (
    command.id
    === "experience.inspector.set"
  ) {
    return {
      open: false,
    };
  }

  if (
    command.id
    === "runtime.describe"
  ) {
    return {
      scope: "platform",
    };
  }

  if (
    command.id
    === "providers.refresh"
  ) {
    return {
      scope: "all",
    };
  }

  return Object.fromEntries(
    command.requiredArguments.map(
      (argument) => [
        argument,
        null,
      ],
    ),
  );
}

function formatRisk(risk: string): string {
  return risk
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
}
