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

const CommandSurface = lazy(
  async () => {
    const module =
      await preloadCommandSurface();

    return {
      default: (
        module as typeof import(
          "./CommandSurface"
        )
      ).CommandSurface,
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
    <Suspense fallback={null}>
      <CommandSurface />
    </Suspense>
  );
}
