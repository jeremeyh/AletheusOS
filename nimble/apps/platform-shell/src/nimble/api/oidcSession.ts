import type {
  User,
  UserManager,
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
  private readonly listeners =
    new Set<SessionListener>();

  private managerPromise:
    Promise<UserManager | null> | null = null;

  private eventsRegistered = false;

  private snapshot: OidcSessionSnapshot = {
    state: "anonymous",
    user: null,
    error: null,
  };

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
    const manager = await this.getManager();

    if (!manager) {
      this.update({
        state: "unconfigured",
        user: null,
        error: null,
      });

      return;
    }

    try {
      const user = await manager.getUser();

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
    const manager = await this.requireManager();

    this.update({
      state: "authenticating",
      user: null,
      error: null,
    });

    try {
      const user =
        await manager.signinRedirectCallback();

      this.update({
        state: user.expired
          ? "expired"
          : "authenticated",
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
    const manager = await this.requireManager();

    this.update({
      state: "authenticating",
      user: null,
      error: null,
    });

    await manager.signinRedirect();
  }

  async signOut(): Promise<void> {
    const manager = await this.getManager();

    if (!manager) {
      return;
    }

    await manager.signoutRedirect();
  }

  async getAccessToken():
    Promise<string | null> {
    const manager = await this.getManager();

    if (!manager) {
      return null;
    }

    let user = await manager.getUser();

    if (!user) {
      return null;
    }

    if (user.expired) {
      try {
        user = await manager.signinSilent();
      } catch (error) {
        this.update({
          state: "expired",
          user,
          error:
            error instanceof Error
              ? error.message
              : "The OIDC session could not be renewed.",
        });

        return null;
      }
    }

    if (!user) {
      return null;
    }

    this.update({
      state: "authenticated",
      user,
      error: null,
    });

    return user.access_token || null;
  }

  async removeUser(): Promise<void> {
    const manager = await this.getManager();

    if (!manager) {
      return;
    }

    await manager.removeUser();

    this.update({
      state: "anonymous",
      user: null,
      error: null,
    });
  }

  private getManager():
    Promise<UserManager | null> {
    if (!this.managerPromise) {
      this.managerPromise =
        this.createManager();
    }

    return this.managerPromise;
  }

  private async requireManager():
    Promise<UserManager> {
    const manager = await this.getManager();

    if (!manager) {
      throw new Error(
        "Browser OIDC is not configured.",
      );
    }

    return manager;
  }

  private async createManager():
    Promise<UserManager | null> {
    const config =
      loadBrowserOidcConfiguration();

    if (!config) {
      return null;
    }

    const {
      Log,
      UserManager,
      WebStorageStateStore,
    } = await import("oidc-client-ts");

    const manager = new UserManager({
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

    if (import.meta.env.DEV) {
      Log.setLogger(console);
      Log.setLevel(Log.WARN);
    }

    this.registerEvents(manager);

    return manager;
  }

  private registerEvents(
    manager: UserManager,
  ): void {
    if (this.eventsRegistered) {
      return;
    }

    this.eventsRegistered = true;

    manager.events.addUserLoaded(
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

    manager.events.addUserUnloaded(
      () => {
        this.update({
          state: "anonymous",
          user: null,
          error: null,
        });
      },
    );

    manager.events.addAccessTokenExpired(
      () => {
        this.update({
          state: "expired",
          user: this.snapshot.user,
          error:
            "The OIDC access token has expired.",
        });
      },
    );

    manager.events.addSilentRenewError(
      (error) => {
        this.update({
          state: "error",
          user: this.snapshot.user,
          error:
            `Silent renewal failed: ${error.message}`,
        });
      },
    );
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
