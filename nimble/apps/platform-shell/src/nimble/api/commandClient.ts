import type {
  CommandApiFailure,
  CommandAuthorization,
  CommandDefinition,
  CommandExecution,
  CommandExecutionRequest,
  CommandPreview,
  CommandPreviewRequest,
  CommandReversalRequest,
} from "./commandTypes";

const apiBaseUrl =
  import.meta.env.VITE_ALETHEUS_API_URL?.trim()
  || "http://127.0.0.1:8000";

export class CommandApiError extends Error {
  readonly status: number;
  readonly detail: string;

  constructor(
    message: string,
    status: number,
    detail: string,
  ) {
    super(message);
    this.name = "CommandApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function requestJson<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(
    `${apiBaseUrl}${path}`,
    {
      ...init,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...init?.headers,
      },
    },
  );

  if (!response.ok) {
    let detail = response.statusText;

    try {
      const payload =
        await response.json() as CommandApiFailure;

      detail = payload.detail || detail;
    } catch {
      // Preserve the HTTP status text.
    }

    throw new CommandApiError(
      `Command gateway returned HTTP ${response.status}.`,
      response.status,
      detail,
    );
  }

  return await response.json() as T;
}

export function getCommands(
  signal?: AbortSignal,
): Promise<readonly CommandDefinition[]> {
  return requestJson<readonly CommandDefinition[]>(
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
  return requestJson<CommandPreview>(
    "/api/commands/preview",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export function authorizeCommand(
  previewId: string,
  _authorizedBy?: string,
): Promise<CommandAuthorization> {
  return requestJson<CommandAuthorization>(
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
  return requestJson<CommandExecution>(
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
  return requestJson<CommandExecution>(
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
  return requestJson<readonly CommandExecution[]>(
    "/api/commands/history",
    {
      method: "GET",
      signal,
    },
  );
}
