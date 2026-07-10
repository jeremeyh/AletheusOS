const storageKey = "nimble-reference-shell";

const defaultState = {
  theme: "dark",
  navigationCollapsed: false,
  inspectorCollapsed: false,
  selectedCommand: "runtime.describe",
};

let state = loadState();

const root = document.documentElement;
const body = document.body;
const commandDialog = document.querySelector(
  "[data-command-dialog]",
);
const liveRegion = document.querySelector(
  "[data-live-region]",
);
const themeValue = document.querySelector(
  "[data-theme-value]",
);
const navigationValue = document.querySelector(
  "[data-navigation-value]",
);
const stateValue = document.querySelector(
  "[data-state-value]",
);

function loadState() {
  try {
    const stored =
      localStorage.getItem(storageKey);

    if (!stored) {
      return { ...defaultState };
    }

    return {
      ...defaultState,
      ...JSON.parse(stored),
    };
  } catch (error) {
    console.error(
      "Nimble shell state could not be restored.",
      error,
    );

    return { ...defaultState };
  }
}

function saveState() {
  localStorage.setItem(
    storageKey,
    JSON.stringify(state),
  );
}

function announce(message) {
  if (!liveRegion) {
    return;
  }

  liveRegion.textContent = message;
  liveRegion.dataset.visible = "true";

  window.setTimeout(() => {
    liveRegion.dataset.visible = "false";
  }, 2200);
}

function renderState() {
  root.dataset.theme = state.theme;

  body.dataset.navigationCollapsed =
    String(state.navigationCollapsed);

  body.dataset.inspectorCollapsed =
    String(state.inspectorCollapsed);

  if (themeValue) {
    themeValue.textContent =
      state.theme === "dark"
        ? "Dark"
        : "Light";
  }

  if (navigationValue) {
    navigationValue.textContent =
      state.navigationCollapsed
        ? "Collapsed"
        : "Expanded";
  }

  if (stateValue) {
    stateValue.textContent =
      "Ready";
  }

  document
    .querySelectorAll("[data-command]")
    .forEach((button) => {
      button.setAttribute(
        "aria-selected",
        String(
          button.dataset.command
            === state.selectedCommand,
        ),
      );
    });

  saveState();
}

function toggleTheme() {
  state = {
    ...state,
    theme:
      state.theme === "dark"
        ? "light"
        : "dark",
  };

  renderState();
  announce(`Theme changed to ${state.theme}.`);
}

function toggleNavigation() {
  state = {
    ...state,
    navigationCollapsed:
      !state.navigationCollapsed,
  };

  renderState();

  announce(
    state.navigationCollapsed
      ? "Global navigation collapsed."
      : "Global navigation expanded.",
  );
}

function toggleInspector() {
  state = {
    ...state,
    inspectorCollapsed:
      !state.inspectorCollapsed,
  };

  renderState();

  announce(
    state.inspectorCollapsed
      ? "Context inspector collapsed."
      : "Context inspector expanded.",
  );
}

function resetShell() {
  state = {
    ...defaultState,
  };

  localStorage.removeItem(storageKey);
  renderState();
  announce("Nimble reference shell reset.");
}

function openCommand() {
  if (!(commandDialog instanceof HTMLDialogElement)) {
    return;
  }

  commandDialog.showModal();

  const selected =
    commandDialog.querySelector(
      '[aria-selected="true"]',
    );

  selected?.focus();
}

function executeSelectedCommand() {
  const command =
    state.selectedCommand;

  if (command === "experience.inspector.set") {
    toggleInspector();
  } else if (command === "providers.refresh") {
    announce(
      "Provider refresh simulated successfully.",
    );
  } else {
    announce(
      "Runtime description command completed.",
    );
  }

  if (commandDialog instanceof HTMLDialogElement) {
    commandDialog.close();
  }
}

document.addEventListener(
  "click",
  (event) => {
    const target = event.target;

    if (!(target instanceof HTMLElement)) {
      return;
    }

    const actionElement =
      target.closest("[data-action]");

    if (actionElement instanceof HTMLElement) {
      const action =
        actionElement.dataset.action;

      if (action === "toggle-theme") {
        toggleTheme();
      }

      if (action === "toggle-navigation") {
        toggleNavigation();
      }

      if (action === "toggle-inspector") {
        toggleInspector();
      }

      if (action === "reset-shell") {
        resetShell();
      }

      if (action === "open-command") {
        openCommand();
      }

      if (action === "execute-command") {
        executeSelectedCommand();
      }
    }

    const commandElement =
      target.closest("[data-command]");

    if (commandElement instanceof HTMLElement) {
      state = {
        ...state,
        selectedCommand:
          commandElement.dataset.command
          ?? defaultState.selectedCommand,
      };

      renderState();
    }
  },
);

document.addEventListener(
  "keydown",
  (event) => {
    const commandShortcut =
      (event.metaKey || event.ctrlKey)
      && event.key.toLowerCase() === "k";

    if (commandShortcut) {
      event.preventDefault();
      openCommand();
    }

    if (
      event.key === "Enter"
      && commandDialog?.open
      && document.activeElement?.matches(
        "[data-command]",
      )
    ) {
      executeSelectedCommand();
    }
  },
);

renderState();

export {
  executeSelectedCommand,
  openCommand,
  resetShell,
  toggleInspector,
  toggleNavigation,
  toggleTheme,
};
