import {
  lazyImportWithRetry,
} from "./lazyImport";

export function preloadCommandSurface():
  Promise<typeof import(
    "./components/CommandSurface"
  )> {
  return lazyImportWithRetry(
    () => import(
      "./components/CommandSurface"
    ),
  );
}

export function preloadCommandHistory():
  Promise<typeof import(
    "./routes/CommandHistoryRoute"
  )> {
  return lazyImportWithRetry(
    () => import(
      "./routes/CommandHistoryRoute"
    ),
  );
}

export function preloadPrincipalPanel():
  Promise<typeof import(
    "./components/PrincipalPanel"
  )> {
  return lazyImportWithRetry(
    () => import(
      "./components/PrincipalPanel"
    ),
  );
}

export function preloadOidcCallback():
  Promise<typeof import(
    "./routes/OidcCallbackRoute"
  )> {
  return lazyImportWithRetry(
    () => import(
      "./routes/OidcCallbackRoute"
    ),
  );
}
