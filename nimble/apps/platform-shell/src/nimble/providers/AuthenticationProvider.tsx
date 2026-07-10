import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import type {
  PropsWithChildren,
} from "react";
import {
  useQueryClient,
} from "@tanstack/react-query";

import {
  clearAuthenticationMetadataCache,
} from "../api/apiTransport";
import {
  useAuthenticationMetadata,
} from "../api/authQueries";
import {
  identityQueryKeys,
} from "../api/identityQueries";
import {
  oidcBrowserSession,
} from "../api/oidcSession";
import type {
  OidcSessionSnapshot,
} from "../api/oidcSession";

interface AuthenticationContextValue {
  readonly mode:
    | "local"
    | "oidc"
    | "unknown";

  readonly session:
    OidcSessionSnapshot;

  readonly requiresAuthentication: boolean;
  readonly authenticated: boolean;
  readonly isPending: boolean;
  readonly error: Error | null;

  signIn(): Promise<void>;
  signOut(): Promise<void>;
  clearSession(): Promise<void>;
}

const AuthenticationContext =
  createContext<
    AuthenticationContextValue | undefined
  >(undefined);

const initialSession:
  OidcSessionSnapshot = {
    state: "anonymous",
    user: null,
    error: null,
  };

export function AuthenticationProvider({
  children,
}: PropsWithChildren) {
  const queryClient = useQueryClient();

  const {
    data,
    error,
    isPending,
  } = useAuthenticationMetadata();

  const [session, setSession] =
    useState<OidcSessionSnapshot>(
      initialSession,
    );

  useEffect(() => {
    return oidcBrowserSession.subscribe(
      setSession,
    );
  }, []);

  useEffect(() => {
    if (data?.mode === "oidc") {
      void oidcBrowserSession.initialize();
    }
  }, [data?.mode]);

  const refreshIdentity =
    useCallback(async () => {
      await queryClient.invalidateQueries({
        queryKey:
          identityQueryKeys.current,
      });
    }, [queryClient]);

  const signIn = useCallback(async () => {
    await oidcBrowserSession.signIn();
  }, []);

  const signOut = useCallback(async () => {
    await oidcBrowserSession.signOut();
  }, []);

  const clearSession =
    useCallback(async () => {
      await oidcBrowserSession.removeUser();
      await refreshIdentity();
    }, [refreshIdentity]);

  const mode:
    AuthenticationContextValue["mode"] =
      data?.mode ?? "unknown";

  useEffect(() => {
    function handleAuthenticationRequired() {
      if (mode === "oidc") {
        void oidcBrowserSession.removeUser();
      }
    }

    window.addEventListener(
      "aletheus:authentication-required",
      handleAuthenticationRequired,
    );

    return () => {
      window.removeEventListener(
        "aletheus:authentication-required",
        handleAuthenticationRequired,
      );
    };
  }, [mode]);

  useEffect(() => {
    if (
      session.state === "authenticated"
      || session.state === "anonymous"
      || session.state === "expired"
    ) {
      void refreshIdentity();
    }
  }, [
    refreshIdentity,
    session.state,
  ]);

  const value =
    useMemo<AuthenticationContextValue>(
      () => ({
        mode,
        session,
        requiresAuthentication:
          mode === "oidc",
        authenticated:
          mode === "local"
          || session.state
            === "authenticated",
        isPending,
        error,
        signIn,
        signOut,
        clearSession,
      }),
      [
        clearSession,
        error,
        isPending,
        mode,
        session,
        signIn,
        signOut,
      ],
    );

  return (
    <AuthenticationContext.Provider
      value={value}
    >
      {children}
    </AuthenticationContext.Provider>
  );
}

export function useAuthentication():
  AuthenticationContextValue {
  const context = useContext(
    AuthenticationContext,
  );

  if (!context) {
    throw new Error(
      "useAuthentication must be used inside AuthenticationProvider.",
    );
  }

  return context;
}

export function resetAuthenticationTransport():
  void {
  clearAuthenticationMetadataCache();
}
