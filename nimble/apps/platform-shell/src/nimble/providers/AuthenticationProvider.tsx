import {
  createContext,
  useCallback,
  useContext,
  useMemo,
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
  sessionTokenProvider,
} from "../api/tokenProvider";

interface AuthenticationContextValue {
  readonly mode:
    | "local"
    | "oidc"
    | "unknown";
  readonly requiresToken: boolean;
  readonly isPending: boolean;
  readonly error: Error | null;
  setAccessToken(token: string): Promise<void>;
  clearAccessToken(): Promise<void>;
}

const AuthenticationContext =
  createContext<
    AuthenticationContextValue | undefined
  >(undefined);

export function AuthenticationProvider({
  children,
}: PropsWithChildren) {
  const queryClient = useQueryClient();

  const {
    data,
    error,
    isPending,
  } = useAuthenticationMetadata();

  const setAccessToken = useCallback(
    async (token: string) => {
      sessionTokenProvider
        .setAccessToken(token.trim());

      await queryClient.invalidateQueries({
        queryKey:
          identityQueryKeys.current,
      });
    },
    [queryClient],
  );

  const clearAccessToken = useCallback(
    async () => {
      sessionTokenProvider
        .clearAccessToken();

      await queryClient.invalidateQueries({
        queryKey:
          identityQueryKeys.current,
      });
    },
    [queryClient],
  );

  const value = useMemo(
    () => ({
      mode: data?.mode ?? "unknown",
      requiresToken:
        data?.mode === "oidc",
      isPending,
      error,
      setAccessToken,
      clearAccessToken,
    }),
    [
      clearAccessToken,
      data?.mode,
      error,
      isPending,
      setAccessToken,
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

export function resetAuthenticationTransport(): void {
  clearAuthenticationMetadataCache();
}
