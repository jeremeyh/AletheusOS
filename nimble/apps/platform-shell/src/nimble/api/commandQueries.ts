import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  authorizeCommand,
  executeCommand,
  getCommandHistory,
  getCommands,
  previewCommand,
  reverseCommand,
} from "./commandClient";

import type {
  CommandExecutionRequest,
  CommandPreviewRequest,
  CommandReversalRequest,
} from "./commandTypes";

export const commandQueryKeys = {
  root: ["aletheus-commands"] as const,
  definitions: () => [
    ...commandQueryKeys.root,
    "definitions",
  ] as const,
  history: () => [
    ...commandQueryKeys.root,
    "history",
  ] as const,
};

export function useCommandDefinitions() {
  return useQuery({
    queryKey: commandQueryKeys.definitions(),
    queryFn: ({ signal }) => getCommands(signal),
    staleTime: 60_000,
    retry: 1,
  });
}

export function useCommandHistory() {
  return useQuery({
    queryKey: commandQueryKeys.history(),
    queryFn: ({ signal }) => getCommandHistory(signal),
    staleTime: 5_000,
    retry: 1,
  });
}

export function usePreviewCommand() {
  return useMutation({
    mutationFn: (
      request: CommandPreviewRequest,
    ) => previewCommand(request),
  });
}

export function useAuthorizeCommand() {
  return useMutation({
    mutationFn: ({
      previewId,
    }: {
      readonly previewId: string;
    }) => authorizeCommand(
      previewId,
    ),
  });
}

export function useExecuteCommand() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (
      request: CommandExecutionRequest,
    ) => executeCommand(request),

    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: commandQueryKeys.history(),
      });
    },
  });
}

export function useReverseCommand() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (
      request: CommandReversalRequest,
    ) => reverseCommand(request),

    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: commandQueryKeys.history(),
      });
    },
  });
}
