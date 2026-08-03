import type { Principal } from "../types.js";

const FALLBACK_PRINCIPAL: Principal = {
  subject: "local-operator",
  displayName: "Local Operator",
  claims: ["standard_user", "workspace_composer"],
};

export function resolvePrincipal(): Principal {
  const injected = (window as Window & { __ALETHEUS_PRINCIPAL__?: Principal }).__ALETHEUS_PRINCIPAL__;
  return injected ?? FALLBACK_PRINCIPAL;
}

export function canAccessFounderObservatory(principal: Principal): boolean {
  return principal.claims.includes("founder_root");
}
