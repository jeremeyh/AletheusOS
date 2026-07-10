import { LazyCommandSurface } from "./nimble/components/LazyCommandSurface";
import { AuthenticationProvider } from "./nimble/providers/AuthenticationProvider";
import "./App.css";

import { RouterProvider } from "react-router";

import { NimbleProvider } from "./nimble/providers/NimbleProvider";
import { RuntimeQueryProvider } from "./nimble/providers/RuntimeQueryProvider";
import { nimbleRouter } from "./nimble/router/router";

export default function App() {
  return (
    <RuntimeQueryProvider>
      <AuthenticationProvider>
        <NimbleProvider>
        <RouterProvider router={nimbleRouter} />
              <LazyCommandSurface />
      </NimbleProvider>
      </AuthenticationProvider>
    </RuntimeQueryProvider>
  );
}
