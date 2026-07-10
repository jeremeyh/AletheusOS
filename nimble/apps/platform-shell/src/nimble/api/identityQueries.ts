import {
  useQuery,
} from "@tanstack/react-query";

import {
  getCurrentPrincipal,
} from "./identityClient";

export const identityQueryKeys = {
  current: ["aletheus-identity", "current"] as const,
};

export function useCurrentPrincipal() {
  return useQuery({
    queryKey: identityQueryKeys.current,
    queryFn: ({ signal }) =>
      getCurrentPrincipal(signal),
    staleTime: 60_000,
    retry: 1,
  });
}
