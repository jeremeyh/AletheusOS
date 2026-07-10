import type {
  RuntimeHealthSnapshot,
  RuntimeMission,
  RuntimeOverview,
} from "./runtimeTypes";

const DEFAULT_TIMEOUT_MS = 5000;

const apiBaseUrl =
  import.meta.env.VITE_ALETHEUS_API_URL?.trim()
  || "http://127.0.0.1:8000";

export class NimbleApiError extends Error {
  readonly status?: number;
  readonly causeDetail?: string;

  constructor(
    message: string,
    options?: {
      readonly status?: number;
      readonly causeDetail?: string;
    },
  ) {
    super(message);
    this.name = "NimbleApiError";
    this.status = options?.status;
    this.causeDetail = options?.causeDetail;
  }
}

async function requestJson<T>(
  path: string,
  signal?: AbortSignal,
): Promise<T> {
  const timeoutController = new AbortController();

  const timeoutId = window.setTimeout(() => {
    timeoutController.abort();
  }, DEFAULT_TIMEOUT_MS);

  const combinedSignal = signal
    ? AbortSignal.any([
        signal,
        timeoutController.signal,
      ])
    : timeoutController.signal;

  try {
    const response = await fetch(
      `${apiBaseUrl}${path}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
        signal: combinedSignal,
      },
    );

    if (!response.ok) {
      throw new NimbleApiError(
        `AletheusOS returned HTTP ${response.status}.`,
        {
          status: response.status,
          causeDetail: response.statusText,
        },
      );
    }

    return await response.json() as T;
  } catch (error) {
    if (error instanceof NimbleApiError) {
      throw error;
    }

    if (
      error instanceof DOMException
      && error.name === "AbortError"
    ) {
      throw new NimbleApiError(
        "The AletheusOS request timed out or was cancelled.",
        {
          causeDetail: error.message,
        },
      );
    }

    throw new NimbleApiError(
      "The AletheusOS runtime could not be reached.",
      {
        causeDetail:
          error instanceof Error
            ? error.message
            : String(error),
      },
    );
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function getRuntimeHealth(
  signal?: AbortSignal,
): Promise<RuntimeHealthSnapshot> {
  return requestJson<RuntimeHealthSnapshot>(
    "/api/runtime/health",
    signal,
  );
}

export async function getRuntimeMissions(
  signal?: AbortSignal,
): Promise<readonly RuntimeMission[]> {
  return requestJson<readonly RuntimeMission[]>(
    "/api/missions",
    signal,
  );
}

export async function getRuntimeOverview(
  signal?: AbortSignal,
): Promise<RuntimeOverview> {
  const [health, missions] = await Promise.all([
    getRuntimeHealth(signal),
    getRuntimeMissions(signal),
  ]);

  return {
    health,
    missions,
    generatedAt: new Date().toISOString(),
  };
}
