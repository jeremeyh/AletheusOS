import {
  lazy,
  Suspense,
} from "react";

import {
  preloadCommandSurface,
} from "../prefetch";
import {
  useNimble,
} from "../providers/NimbleProvider";
import {
  NimbleErrorBoundary,
} from "./NimbleErrorBoundary";

const CommandSurface = lazy(
  async () => {
    const module =
      await preloadCommandSurface();

    return {
      default: module.CommandSurface,
    };
  },
);

export function LazyCommandSurface() {
  const {
    commandOpen,
  } = useNimble();

  if (!commandOpen) {
    return null;
  }

  return (
    <NimbleErrorBoundary
      scope="governed command surface"
    >
      <Suspense
      fallback={
        <div
          className="nimble-command-loading"
          role="status"
        >
          Loading governed commands…
        </div>
      }
    >
        <CommandSurface />
      </Suspense>
    </NimbleErrorBoundary>
  );
}
