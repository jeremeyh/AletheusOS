import {
  useCallback,
  useState,
} from "react";

import {
  useAuthorizeCommand,
  useExecuteCommand,
  usePreviewCommand,
  useReverseCommand,
} from "./commandQueries";

import type {
  CommandAuthorization,
  CommandDefinition,
  CommandExecution,
  CommandPreview,
} from "./commandTypes";

export type CommandTransactionStage =
  | "idle"
  | "previewing"
  | "preview"
  | "authorizing"
  | "executing"
  | "complete"
  | "reversing"
  | "reversed"
  | "failed";

export function useCommandTransaction() {
  const previewMutation = usePreviewCommand();
  const authorizationMutation =
    useAuthorizeCommand();
  const executionMutation =
    useExecuteCommand();
  const reversalMutation =
    useReverseCommand();

  const [stage, setStage] =
    useState<CommandTransactionStage>("idle");

  const [definition, setDefinition] =
    useState<CommandDefinition | null>(null);

  const [preview, setPreview] =
    useState<CommandPreview | null>(null);

  const [authorization, setAuthorization] =
    useState<CommandAuthorization | null>(null);

  const [execution, setExecution] =
    useState<CommandExecution | null>(null);

  const [failure, setFailure] =
    useState<string | null>(null);

  const begin = useCallback(
    async (
      command: CommandDefinition,
      argumentsValue: Readonly<Record<string, unknown>>,
    ) => {
      setDefinition(command);
      setFailure(null);
      setAuthorization(null);
      setExecution(null);
      setStage("previewing");

      try {
        const nextPreview =
          await previewMutation.mutateAsync({
            command_id: command.id,
            arguments: argumentsValue,
            idempotency_key: crypto.randomUUID(),
          });

        setPreview(nextPreview);
        setStage("preview");

        return nextPreview;
      } catch (error) {
        setFailure(
          error instanceof Error
            ? error.message
            : String(error),
        );

        setStage("failed");
        throw error;
      }
    },
    [previewMutation],
  );

  const approveAndExecute = useCallback(
    async () => {
      if (!preview) {
        throw new Error(
          "No command preview is active.",
        );
      }

      try {
        let nextAuthorization:
          | CommandAuthorization
          | null = null;

        if (preview.authorization_required) {
          setStage("authorizing");

          nextAuthorization =
            await authorizationMutation.mutateAsync({
              previewId: preview.preview_id,
            });

          setAuthorization(nextAuthorization);
        }

        setStage("executing");

        const nextExecution =
          await executionMutation.mutateAsync({
            preview_id: preview.preview_id,
            authorization_id:
              nextAuthorization?.authorization_id
              ?? null,
            idempotency_key:
              `nimble:${preview.preview_id}`,
          });

        setExecution(nextExecution);

        if (nextExecution.state === "failed") {
          setFailure(
            nextExecution.failure
            ?? "Command execution failed.",
          );
          setStage("failed");
        } else {
          setStage("complete");
        }

        return nextExecution;
      } catch (error) {
        setFailure(
          error instanceof Error
            ? error.message
            : String(error),
        );

        setStage("failed");
        throw error;
      }
    },
    [
      authorizationMutation,
      executionMutation,
      preview,
    ],
  );

  const reverse = useCallback(async () => {
    if (
      !execution
      || !execution.reversal_token
    ) {
      throw new Error(
        "The current execution cannot be reversed.",
      );
    }

    setStage("reversing");

    try {
      const reversed =
        await reversalMutation.mutateAsync({
          execution_id: execution.execution_id,
          reversal_token:
            execution.reversal_token,
        });

      setExecution(reversed);
      setStage("reversed");

      return reversed;
    } catch (error) {
      setFailure(
        error instanceof Error
          ? error.message
          : String(error),
      );

      setStage("failed");
      throw error;
    }
  }, [execution, reversalMutation]);

  const reset = useCallback(() => {
    setStage("idle");
    setDefinition(null);
    setPreview(null);
    setAuthorization(null);
    setExecution(null);
    setFailure(null);

    previewMutation.reset();
    authorizationMutation.reset();
    executionMutation.reset();
    reversalMutation.reset();
  }, [
    authorizationMutation,
    executionMutation,
    previewMutation,
    reversalMutation,
  ]);

  return {
    stage,
    definition,
    preview,
    authorization,
    execution,
    failure,
    begin,
    approveAndExecute,
    reverse,
    reset,
  };
}
