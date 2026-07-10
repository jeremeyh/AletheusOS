import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type {
  NimbleDensity,
  NimbleDisclosureLevel,
  NimbleMotionPreference,
  NimbleTheme,
} from "@aletheus/nimble-core";

export interface NimbleToast {
  readonly id: string;
  readonly title: string;
  readonly message: string;
}

interface NimbleState {
  readonly theme: NimbleTheme;
  readonly density: NimbleDensity;
  readonly motion: NimbleMotionPreference;
  readonly disclosure: NimbleDisclosureLevel;
  readonly navigationExpanded: boolean;
  readonly inspectorOpen: boolean;
  readonly commandOpen: boolean;
}

interface NimbleContextValue extends NimbleState {
  readonly toasts: readonly NimbleToast[];
  readonly setTheme: (theme: NimbleTheme) => void;
  readonly toggleTheme: () => void;
  readonly toggleNavigation: () => void;
  readonly toggleInspector: () => void;
  readonly setCommandOpen: (open: boolean) => void;
  readonly notify: (title: string, message: string) => void;
  readonly dismissToast: (id: string) => void;
  readonly reset: () => void;
}

const STORAGE_KEY = "aletheus.nimble.shell.v0.1";

const defaultState: NimbleState = {
  theme: "dark",
  density: "balanced",
  motion: "system",
  disclosure: "complete",
  navigationExpanded: true,
  inspectorOpen: true,
  commandOpen: false,
};

const NimbleContext = createContext<NimbleContextValue | null>(null);

function loadState(): NimbleState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);

    if (!stored) {
      return defaultState;
    }

    const parsed = JSON.parse(stored) as Partial<NimbleState>;

    return {
      ...defaultState,
      ...parsed,
      commandOpen: false,
    };
  } catch {
    return defaultState;
  }
}

export function NimbleProvider({
  children,
}: {
  readonly children: ReactNode;
}) {
  const [state, setState] = useState<NimbleState>(loadState);
  const [toasts, setToasts] = useState<readonly NimbleToast[]>([]);

  useEffect(() => {
    document.documentElement.dataset.nimbleTheme = state.theme;

    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        ...state,
        commandOpen: false,
      }),
    );
  }, [state]);

  const update = useCallback((patch: Partial<NimbleState>) => {
    setState((current) => ({
      ...current,
      ...patch,
    }));
  }, []);

  const dismissToast = useCallback((id: string) => {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }, []);

  const notify = useCallback(
    (title: string, message: string) => {
      const id = crypto.randomUUID();

      setToasts((current) => [
        ...current,
        {
          id,
          title,
          message,
        },
      ]);

      window.setTimeout(() => {
        dismissToast(id);
      }, 4200);
    },
    [dismissToast],
  );

  const value = useMemo<NimbleContextValue>(
    () => ({
      ...state,
      toasts,

      setTheme: (theme) => update({ theme }),

      toggleTheme: () => {
        update({
          theme: state.theme === "dark" ? "light" : "dark",
        });
      },

      toggleNavigation: () => {
        update({
          navigationExpanded: !state.navigationExpanded,
        });
      },

      toggleInspector: () => {
        update({
          inspectorOpen: !state.inspectorOpen,
        });
      },

      setCommandOpen: (commandOpen) => {
        update({ commandOpen });
      },

      notify,
      dismissToast,

      reset: () => {
        setState(defaultState);
        notify(
          "Shell restored",
          "Theme, navigation, inspector, and disclosure state were reset.",
        );
      },
    }),
    [
      dismissToast,
      notify,
      state,
      toasts,
      update,
    ],
  );

  return (
    <NimbleContext.Provider value={value}>
      {children}
    </NimbleContext.Provider>
  );
}

export function useNimble(): NimbleContextValue {
  const value = useContext(NimbleContext);

  if (!value) {
    throw new Error(
      "useNimble must be used within NimbleProvider.",
    );
  }

  return value;
}
