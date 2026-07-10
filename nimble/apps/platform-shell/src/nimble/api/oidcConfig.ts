export interface BrowserOidcConfiguration {
  readonly authority: string;
  readonly clientId: string;
  readonly redirectUri: string;
  readonly postLogoutRedirectUri: string;
  readonly scope: string;
}

export function loadBrowserOidcConfiguration():
  BrowserOidcConfiguration | null {
  const authority =
    import.meta.env.VITE_OIDC_AUTHORITY?.trim();

  const clientId =
    import.meta.env.VITE_OIDC_CLIENT_ID?.trim();

  if (!authority || !clientId) {
    return null;
  }

  return {
    authority,
    clientId,
    redirectUri:
      import.meta.env.VITE_OIDC_REDIRECT_URI?.trim()
      || `${window.location.origin}/auth/callback`,
    postLogoutRedirectUri:
      import.meta.env
        .VITE_OIDC_POST_LOGOUT_REDIRECT_URI
        ?.trim()
      || `${window.location.origin}/`,
    scope:
      import.meta.env.VITE_OIDC_SCOPE?.trim()
      || "openid profile email",
  };
}
