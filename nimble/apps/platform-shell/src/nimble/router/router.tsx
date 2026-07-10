import {
  createBrowserRouter,
  Navigate,
} from "react-router";

import { PlatformShell } from "../components/PlatformShell";
import { RouteError } from "../components/feedback/RouteError";
import { OverviewRoute } from "../routes/OverviewRoute";
import { PlaceholderRoute } from "../routes/PlaceholderRoute";

export const nimbleRouter = createBrowserRouter([
  {
    path: "/",
    element: <PlatformShell />,
    errorElement: <RouteError />,
    children: [
      {
        index: true,
        element: <OverviewRoute />,
      },
      {
        path: "overview",
        element: <Navigate to="/" replace />,
      },
      {
        path: "intelligence",
        element: <PlaceholderRoute />,
      },
      {
        path: "missions",
        element: <PlaceholderRoute />,
      },
      {
        path: "workflows",
        element: <PlaceholderRoute />,
      },
      {
        path: "agents",
        element: <PlaceholderRoute />,
      },
      {
        path: "memory",
        element: <PlaceholderRoute />,
      },
      {
        path: "knowledge-graph",
        element: <PlaceholderRoute />,
      },
      {
        path: "council",
        element: <PlaceholderRoute />,
      },
      {
        path: "runtime",
        element: <PlaceholderRoute />,
      },
      {
        path: "*",
        element: <Navigate to="/" replace />,
      },
    ],
  },
]);
