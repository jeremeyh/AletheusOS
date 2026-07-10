const root = document.documentElement;
const shell = document.querySelector(".nimble-shell");
const commandDialog = document.querySelector("[data-command-dialog]");
const commandInput = document.querySelector("#nimble-command-input");
const commandResults = [
  ...document.querySelectorAll("[data-command-result]"),
];
const toastRegion = document.querySelector("[data-toast-region]");

const STORAGE_KEY = "nimble-reference-shell-v0.1";

const defaultState = Object.freeze({
  theme: "dark",
  navigation: "expanded",
  inspector: "open",
});

let state = loadState();
let selectedCommandIndex = 0;

function loadState() {
  try {
    const stored = JSON.parse(
      localStorage.getItem(STORAGE_KEY) || "{}",
    );

    return {
      ...defaultState,
      ...stored,
    };
  } catch {
    return { ...defaultState };
  }
}

function persistState() {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(state),
  );
}

function renderState() {
  root.dataset.nimbleTheme = state.theme;
  shell.dataset.navigation = state.navigation;
  shell.dataset.inspector = state.inspector;

  const collapseButton = document.querySelector(
    '[data-action="toggle-navigation"]',
  );

  collapseButton?.setAttribute(
    "aria-expanded",
    String(state.navigation === "expanded"),
  );

  collapseButton?.setAttribute(
    "aria-label",
    state.navigation === "expanded"
      ? "Collapse navigation"
      : "Expand navigation",
  );
}

function updateState(patch) {
  state = {
    ...state,
    ...patch,
  };

  persistState();
  renderState();
}

function showToast(title, message) {
  const toast = document.createElement("div");
  toast.className = "nimble-toast";

  const strong = document.createElement("strong");
  strong.textContent = title;

  const span = document.createElement("span");
  span.textContent = message;

  toast.append(strong, span);
  toastRegion.append(toast);

  window.setTimeout(() => {
    toast.animate(
      [
        {
          opacity: 1,
          transform: "translateX(0)",
        },
        {
          opacity: 0,
          transform: "translateX(1rem)",
        },
      ],
      {
        duration: 180,
        easing: "ease-out",
        fill: "forwards",
      },
    ).finished.then(() => toast.remove());
  }, 3600);
}

function openCommand() {
  if (!commandDialog.open) {
    commandDialog.showModal();
  }

  commandInput.focus();
  selectedCommandIndex = 0;
  renderCommandSelection();
}

function closeCommand() {
  if (commandDialog.open) {
    commandDialog.close();
  }
}

function renderCommandSelection() {
  commandResults.forEach((result, index) => {
    result.classList.toggle(
      "is-selected",
      index === selectedCommandIndex,
    );
  });
}

function executeSelectedCommand() {
  const selected = commandResults[selectedCommandIndex];

  if (!selected) {
    return;
  }

  const label = selected.querySelector("strong")?.textContent
    || "Command";

  closeCommand();

  showToast(
    "Command preview",
    `${label} is ready for execution. No destructive action occurred.`,
  );
}

function toggleTheme() {
  updateState({
    theme: state.theme === "dark"
      ? "light"
      : "dark",
  });

  showToast(
    "Theme updated",
    `Nimble is now using the ${state.theme} theme.`,
  );
}

function toggleNavigation() {
  updateState({
    navigation: state.navigation === "expanded"
      ? "collapsed"
      : "expanded",
  });
}

function toggleInspector() {
  updateState({
    inspector: state.inspector === "open"
      ? "closed"
      : "open",
  });
}

function resetShell() {
  state = { ...defaultState };
  persistState();
  renderState();

  showToast(
    "Shell restored",
    "Theme, navigation, and inspector state were reset.",
  );
}

function handleAction(action) {
  const handlers = {
    "open-command": openCommand,
    "toggle-theme": toggleTheme,
    "toggle-navigation": toggleNavigation,
    "toggle-inspector": toggleInspector,
    "reset-shell": resetShell,

    "refresh-brief": () => {
      showToast(
        "Synthesis refreshed",
        "The executive brief is current and fully reconciled.",
      );
    },

    "inspect-confidence": () => {
      updateState({ inspector: "open" });
      showToast(
        "Confidence disclosed",
        "Seven aligned evidence sources support the current 92% confidence.",
      );
    },

    "decision-trace": () => {
      updateState({ inspector: "open" });
      showToast(
        "Decision trace opened",
        "Reasoning, provenance, uncertainty, and reversibility are visible.",
      );
    },

    "customize-workspace": () => {
      showToast(
        "Workspace controls",
        "Panel composition and saved layouts will activate in the workspace engine.",
      );
    },

    "system-health": () => {
      updateState({ inspector: "open" });
      showToast(
        "System health",
        "Runtime stable: 246 checks passing with zero warnings.",
      );
    },

    notifications: () => {
      showToast(
        "Three notifications",
        "All notifications are informational; none require immediate action.",
      );
    },

    "application-switcher": () => {
      showToast(
        "Application switcher",
        "AletheusOS and inherited applications will appear here.",
      );
    },

    "workspace-menu": () => {
      showToast(
        "Executive Command",
        "This workspace is active and its layout state is preserved locally.",
      );
    },

    "user-menu": () => {
      showToast(
        "Personalization",
        "Preferences remain visible, editable, and resettable.",
      );
    },

    "expand-panel": () => {
      showToast(
        "Panel expansion",
        "Structural expansion is defined but has not changed the workspace.",
      );
    },
  };

  handlers[action]?.();
}

document.addEventListener("click", (event) => {
  const actionTarget = event.target.closest("[data-action]");

  if (actionTarget) {
    handleAction(actionTarget.dataset.action);
  }

  const segmentedButton = event.target.closest(
    ".nimble-segmented-control button",
  );

  if (segmentedButton) {
    segmentedButton
      .parentElement
      .querySelectorAll("button")
      .forEach((button) => {
        button.classList.toggle(
          "is-active",
          button === segmentedButton,
        );
      });
  }
});

document.addEventListener("keydown", (event) => {
  const commandShortcut = (
    event.metaKey || event.ctrlKey
  ) && event.key.toLowerCase() === "k";

  if (commandShortcut) {
    event.preventDefault();

    if (commandDialog.open) {
      closeCommand();
    } else {
      openCommand();
    }

    return;
  }

  if (!commandDialog.open) {
    return;
  }

  if (event.key === "ArrowDown") {
    event.preventDefault();
    selectedCommandIndex = (
      selectedCommandIndex + 1
    ) % commandResults.length;
    renderCommandSelection();
  }

  if (event.key === "ArrowUp") {
    event.preventDefault();
    selectedCommandIndex = (
      selectedCommandIndex - 1
      + commandResults.length
    ) % commandResults.length;
    renderCommandSelection();
  }

  if (event.key === "Enter") {
    event.preventDefault();
    executeSelectedCommand();
  }
});

commandResults.forEach((result, index) => {
  result.addEventListener("mouseenter", () => {
    selectedCommandIndex = index;
    renderCommandSelection();
  });

  result.addEventListener("click", () => {
    selectedCommandIndex = index;
    executeSelectedCommand();
  });
});

commandDialog.addEventListener("click", (event) => {
  if (event.target === commandDialog) {
    closeCommand();
  }
});

renderState();
