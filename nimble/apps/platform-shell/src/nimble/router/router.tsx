import {
  lazy,
  Suspense,
} from "react";
import type {
  ReactNode,
} from "react";
import {
  createBrowserRouter,
} from "react-router";
import {
  preloadCommandHistory,
  preloadOidcCallback,
} from "../prefetch";

import { OverviewRoute } from "../routes/OverviewRoute";
import { RouteError } from "../routes/RouteError";
import { PlaceholderRoute } from "../routes/PlaceholderRoute";
import { RoutePending } from "../components/feedback/RoutePending";

const OidcCallbackRoute = lazy(
  async () => {
    const module =
      await preloadOidcCallback();

    return {
      default: (
        module as typeof import(
          "../routes/OidcCallbackRoute"
        )
      ).OidcCallbackRoute,
    };
  },
);

const CommandHistoryRoute = lazy(
  async () => {
    const module =
      await preloadCommandHistory();

    return {
      default: (
        module as typeof import(
          "../routes/CommandHistoryRoute"
        )
      ).CommandHistoryRoute,
    };
  },
);

function LazyRoute({
  children,
}: {
  readonly children: ReactNode;
}) {
  return (
    <Suspense
      fallback={
        <RoutePending label="Loading workspace" />
      }
    >
      {children}
    </Suspense>
  );
}

export const nimbleRouter = createBrowserRouter([
  {
    path: "/",
    element: <OverviewRoute />,
    errorElement: <RouteError />,
  },
  {
    path: "/runtime",
    element: <PlaceholderRoute />,
  },
  {
    path: "/auth/callback",
    element: (
      <LazyRoute>
        <OidcCallbackRoute />
      </LazyRoute>
    ),
  },
  {
    path: "/command-history",
    element: (
      <LazyRoute>
        <CommandHistoryRoute />
      </LazyRoute>
    ),
  },
  {
    path: "*",
    element: <PlaceholderRoute />,
  },
]);
