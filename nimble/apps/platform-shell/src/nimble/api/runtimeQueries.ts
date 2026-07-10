import {
  queryOptions,
  useQuery,
} from "@tanstack/react-query";

import {
  getRuntimeHealth,
  getRuntimeMissions,
  getRuntimeOverview,
  NimbleApiError,
} from "./runtimeClient";

import {
  runtimeHealthFixture,
  runtimeMissionFixture,
  runtimeOverviewFixture,
} from "./runtimeFixture";

const useFixtures =
  import.meta.env.VITE_NIMBLE_USE_FIXTURES !== "false";

export const runtimeQueryKeys = {
  root: ["aletheus-runtime"] as const,
  overview: () => [
    ...runtimeQueryKeys.root,
    "overview",
  ] as const,
  health: () => [
    ...runtimeQueryKeys.root,
    "health",
  ] as const,
  missions: () => [
    ...runtimeQueryKeys.root,
    "missions",
  ] as const,
};

async function withFixtureFallback<T>(
  liveRequest: () => Promise<T>,
  fixture: T,
): Promise<T> {
  try {
    return await liveRequest();
  } catch (error) {
    if (
      useFixtures
      && error instanceof NimbleApiError
    ) {
      return fixture;
    }

    throw error;
  }
}

export const runtimeOverviewQueryOptions = queryOptions({
  queryKey: runtimeQueryKeys.overview(),
  queryFn: ({ signal }) => withFixtureFallback(
    () => getRuntimeOverview(signal),
    runtimeOverviewFixture,
  ),
  staleTime: 15_000,
  refetchInterval: 30_000,
  retry: 1,
});

export const runtimeHealthQueryOptions = queryOptions({
  queryKey: runtimeQueryKeys.health(),
  queryFn: ({ signal }) => withFixtureFallback(
    () => getRuntimeHealth(signal),
    runtimeHealthFixture,
  ),
  staleTime: 10_000,
  refetchInterval: 20_000,
  retry: 1,
});

export const runtimeMissionsQueryOptions = queryOptions({
  queryKey: runtimeQueryKeys.missions(),
  queryFn: ({ signal }) => withFixtureFallback(
    () => getRuntimeMissions(signal),
    runtimeMissionFixture,
  ),
  staleTime: 30_000,
  retry: 1,
});

export function useRuntimeOverview() {
  return useQuery(runtimeOverviewQueryOptions);
}

export function useRuntimeHealth() {
  return useQuery(runtimeHealthQueryOptions);
}

export function useRuntimeMissions() {
  return useQuery(runtimeMissionsQueryOptions);
}
