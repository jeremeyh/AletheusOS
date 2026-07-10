import type {
  CurrentPrincipal,
} from "./identityTypes";

const apiBaseUrl =
  import.meta.env.VITE_ALETHEUS_API_URL?.trim()
  || "http://127.0.0.1:8000";

export async function getCurrentPrincipal(
  signal?: AbortSignal,
): Promise<CurrentPrincipal> {
  const response = await fetch(
    `${apiBaseUrl}/api/identity/me`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal,
    },
  );

  if (!response.ok) {
    throw new Error(
      `Identity gateway returned HTTP ${response.status}.`,
    );
  }

  return await response.json() as CurrentPrincipal;
}
