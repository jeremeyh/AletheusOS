import {
  apiRequest,
} from "./apiTransport";
import type {
  CurrentPrincipal,
} from "./identityTypes";

export function getCurrentPrincipal(
  signal?: AbortSignal,
): Promise<CurrentPrincipal> {
  return apiRequest<CurrentPrincipal>(
    "/api/identity/me",
    {
      method: "GET",
      signal,
    },
  );
}
