import {
  useQuery,
} from "@tanstack/react-query";

import {
  getAuthenticationMetadata,
} from "./apiTransport";

export const authenticationQueryKeys = {
  metadata: [
    "aletheus-authentication",
    "metadata",
  ] as const,
};

export function useAuthenticationMetadata() {
  return useQuery({
    queryKey:
      authenticationQueryKeys.metadata,
    queryFn: ({ signal }) =>
      getAuthenticationMetadata(signal),
    staleTime: Number.POSITIVE_INFINITY,
    retry: 1,
  });
}
