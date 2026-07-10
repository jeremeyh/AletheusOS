export function preloadCommandSurface():
  Promise<unknown> {
  return import(
    "./components/CommandSurface"
  );
}

export function preloadCommandHistory():
  Promise<unknown> {
  return import(
    "./routes/CommandHistoryRoute"
  );
}

export function preloadPrincipalPanel():
  Promise<unknown> {
  return import(
    "./components/PrincipalPanel"
  );
}

export function preloadOidcCallback():
  Promise<unknown> {
  return import(
    "./routes/OidcCallbackRoute"
  );
}
