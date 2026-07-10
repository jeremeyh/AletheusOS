import "./App.css";

import { PlatformShell } from "./nimble/components/PlatformShell";
import { NimbleProvider } from "./nimble/providers/NimbleProvider";

export default function App() {
  return (
    <NimbleProvider>
      <PlatformShell />
    </NimbleProvider>
  );
}
