import type {
  AuthenticationMetadata,
} from "./authTypes";
import {
  sessionTokenProvider,
} from "./tokenProvider";

const apiBaseUrl =
  import.meta.env.VITE_ALETHEUS_API_URL?.trim()
  || "http://127.0.0.1:8000";

let cachedAuthenticationMetadata:
  AuthenticationMetadata | null = null;

interface ApiFailurePayload {
  readonly detail?: string;
}

export class ApiResponseError extends Error {
  readonly status: number;
  readonly detail: string;

  constructor(
    message: string,
    status: number,
    detail: string,
  ) {
    super(message);
    this.name = "ApiResponseError";
    this.status = status;
    this.detail = detail;
  }
}

export async function getAuthenticationMetadata(
  signal?: AbortSignal,
): Promise<AuthenticationMetadata> {
  if (cachedAuthenticationMetadata) {
    return cachedAuthenticationMetadata;
  }

  const response = await fetch(
    `${apiBaseUrl}/api/auth/config`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal,
    },
  );

  if (!response.ok) {
    throw await createResponseError(response);
  }

  const metadata: AuthenticationMetadata =
    await response.json();

  cachedAuthenticationMetadata = metadata;

  return metadata;
}

export async function apiRequest<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const metadata =
    await getAuthenticationMetadata(
      init?.signal ?? undefined,
    );

  const headers =
    new Headers(init?.headers);

  headers.set(
    "Accept",
    "application/json",
  );

  if (
    init?.body !== undefined
    && !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }

  if (metadata.mode === "oidc") {
    const token =
      await sessionTokenProvider
        .getAccessToken();

    if (!token) {
      throw new ApiResponseError(
        "Authentication is required.",
        401,
        "No OIDC access token is available.",
      );
    }

    headers.set(
      "Authorization",
      `Bearer ${token}`,
    );
  }

  const response = await fetch(
    `${apiBaseUrl}${path}`,
    {
      ...init,
      headers,
    },
  );

  if (!response.ok) {
    const error =
      await createResponseError(
        response,
      );

    if (error.status === 401) {
      window.dispatchEvent(
        new CustomEvent(
          "aletheus:authentication-required",
          {
            detail: {
              path,
              reason: error.detail,
            },
          },
        ),
      );
    }

    throw error;
  }

  return await response.json() as T;
}

export function clearAuthenticationMetadataCache():
  void {
  cachedAuthenticationMetadata = null;
}

async function createResponseError(
  response: Response,
): Promise<ApiResponseError> {
  let detail = response.statusText;

  try {
    const payload: ApiFailurePayload =
      await response.json();

    detail = payload.detail || detail;
  } catch {
    // Preserve the HTTP status text.
  }

  return new ApiResponseError(
    `Aletheus API returned HTTP ${response.status}.`,
    response.status,
    detail,
  );
}
