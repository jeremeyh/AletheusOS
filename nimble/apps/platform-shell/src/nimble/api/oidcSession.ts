import {
  Log,
  User,
  UserManager,
  WebStorageStateStore,
} from "oidc-client-ts";

import {
  loadBrowserOidcConfiguration,
} from "./oidcConfig";

export type OidcSessionState =
  | "unconfigured"
  | "anonymous"
  | "authenticating"
  | "authenticated"
  | "expired"
  | "error";

export interface OidcSessionSnapshot {
  readonly state: OidcSessionState;
  readonly user: User | null;
  readonly error: string | null;
}

type SessionListener = (
  snapshot: OidcSessionSnapshot,
) => void;

class OidcBrowserSession {
  private readonly manager:
    UserManager | null;

  private readonly listeners =
    new Set<SessionListener>();

  private snapshot: OidcSessionSnapshot;

  constructor() {
    const config =
      loadBrowserOidcConfiguration();

    if (!config) {
      this.manager = null;

      this.snapshot = {
        state: "unconfigured",
        user: null,
        error: null,
      };

      return;
    }

    this.manager = new UserManager({
      authority: config.authority,
      client_id: config.clientId,
      redirect_uri: config.redirectUri,
      post_logout_redirect_uri:
        config.postLogoutRedirectUri,
      response_type: "code",
      scope: config.scope,

      userStore: new WebStorageStateStore({
        store: window.sessionStorage,
      }),

      stateStore: new WebStorageStateStore({
        store: window.sessionStorage,
      }),

      automaticSilentRenew: true,
      monitorSession: true,
      loadUserInfo: true,
      revokeTokensOnSignout: true,
    });

    this.snapshot = {
      state: "anonymous",
      user: null,
      error: null,
    };

    this.manager.events.addUserLoaded(
      (user) => {
        this.update({
          state: user.expired
            ? "expired"
            : "authenticated",
          user,
          error: null,
        });
      },
    );

    this.manager.events.addUserUnloaded(
      () => {
        this.update({
          state: "anonymous",
          user: null,
          error: null,
        });
      },
    );

    this.manager.events.addAccessTokenExpired(
      () => {
        this.update({
          state: "expired",
          user: this.snapshot.user,
          error:
            "The OIDC access token has expired.",
        });
      },
    );

    this.manager.events.addSilentRenewError(
      (error) => {
        this.update({
          state: "error",
          user: this.snapshot.user,
          error:
            `Silent renewal failed: ${error.message}`,
        });
      },
    );

    if (import.meta.env.DEV) {
      Log.setLogger(console);
      Log.setLevel(Log.WARN);
    }
  }

  subscribe(
    listener: SessionListener,
  ): () => void {
    this.listeners.add(listener);
    listener(this.snapshot);

    return () => {
      this.listeners.delete(listener);
    };
  }

  getSnapshot(): OidcSessionSnapshot {
    return this.snapshot;
  }

  async initialize(): Promise<void> {
    if (!this.manager) {
      return;
    }

    try {
      const user =
        await this.manager.getUser();

      this.update({
        state:
          user && !user.expired
            ? "authenticated"
            : user?.expired
              ? "expired"
              : "anonymous",
        user,
        error: null,
      });
    } catch (error) {
      this.fail(error);
    }
  }

  async handleCallback(): Promise<User> {
    if (!this.manager) {
      throw new Error(
        "Browser OIDC is not configured.",
      );
    }

    this.update({
      state: "authenticating",
      user: null,
      error: null,
    });

    try {
      const user =
        await this.manager
          .signinRedirectCallback();

      this.update({
        state: "authenticated",
        user,
        error: null,
      });

      return user;
    } catch (error) {
      this.fail(error);
      throw error;
    }
  }

  async signIn(): Promise<void> {
    if (!this.manager) {
      throw new Error(
        "Browser OIDC is not configured.",
      );
    }

    this.update({
      state: "authenticating",
      user: null,
      error: null,
    });

    await this.manager.signinRedirect();
  }

  async signOut(): Promise<void> {
    if (!this.manager) {
      return;
    }

    await this.manager.signoutRedirect();
  }

  async getAccessToken():
    Promise<string | null> {
    if (!this.manager) {
      return null;
    }

    let user =
      await this.manager.getUser();

    if (!user) {
      return null;
    }

    if (user.expired) {
      try {
        user =
          await this.manager.signinSilent();
      } catch {
        this.update({
          state: "expired",
          user,
          error:
            "The session expired and could not be renewed.",
        });

        return null;
      }
    }

    if (!user) {
      return null;
    }

    return user.access_token || null;
  }

  async removeUser(): Promise<void> {
    if (!this.manager) {
      return;
    }

    await this.manager.removeUser();

    this.update({
      state: "anonymous",
      user: null,
      error: null,
    });
  }

  private update(
    snapshot: OidcSessionSnapshot,
  ): void {
    this.snapshot = snapshot;

    for (const listener of this.listeners) {
      listener(snapshot);
    }
  }

  private fail(error: unknown): void {
    this.update({
      state: "error",
      user: null,
      error:
        error instanceof Error
          ? error.message
          : String(error),
    });
  }
}

export const oidcBrowserSession =
  new OidcBrowserSession();
