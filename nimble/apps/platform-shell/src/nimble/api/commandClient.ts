import {
  apiRequest,
  ApiResponseError,
} from "./apiTransport";

import type {
  CommandAuthorization,
  CommandDefinition,
  CommandExecution,
  CommandExecutionRequest,
  CommandPreview,
  CommandPreviewRequest,
  CommandReversalRequest,
} from "./commandTypes";

export {
  ApiResponseError as CommandApiError,
};

export function getCommands(
  signal?: AbortSignal,
): Promise<readonly CommandDefinition[]> {
  return apiRequest<
    readonly CommandDefinition[]
  >(
    "/api/commands",
    {
      method: "GET",
      signal,
    },
  );
}

export function previewCommand(
  request: CommandPreviewRequest,
): Promise<CommandPreview> {
  return apiRequest<CommandPreview>(
    "/api/commands/preview",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export function authorizeCommand(
  previewId: string,
): Promise<CommandAuthorization> {
  return apiRequest<CommandAuthorization>(
    "/api/commands/authorize",
    {
      method: "POST",
      body: JSON.stringify({
        preview_id: previewId,
      }),
    },
  );
}

export function executeCommand(
  request: CommandExecutionRequest,
): Promise<CommandExecution> {
  return apiRequest<CommandExecution>(
    "/api/commands/execute",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export function reverseCommand(
  request: CommandReversalRequest,
): Promise<CommandExecution> {
  return apiRequest<CommandExecution>(
    "/api/commands/reverse",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export function getCommandHistory(
  signal?: AbortSignal,
): Promise<readonly CommandExecution[]> {
  return apiRequest<
    readonly CommandExecution[]
  >(
    "/api/commands/history",
    {
      method: "GET",
      signal,
    },
  );
}
