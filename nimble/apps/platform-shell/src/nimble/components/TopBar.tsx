import { useNimble } from "../providers/NimbleProvider";

export function TopBar() {
  const {
    setCommandOpen,
    toggleTheme,
    toggleInspector,
    notify,
  } = useNimble();

  return (
    <header className="nimble-topbar">
      <div className="nimble-context">
        <span>Active workspace</span>
        <strong>Executive Command</strong>
      </div>

      <button
        className="nimble-command-trigger"
        type="button"
        onClick={() => {
          setCommandOpen(true);
        }}
      >
        <span aria-hidden="true">⌘</span>
        <span>Ask or command AletheusOS</span>
        <kbd>⌘ K</kbd>
      </button>

      <div className="nimble-topbar__actions">
        <button
          className="nimble-icon-button"
          type="button"
          aria-label="Toggle visual theme"
          onClick={toggleTheme}
        >
          ◐
        </button>

        <button
          className="nimble-icon-button"
          type="button"
          aria-label="Show notifications"
          onClick={() => {
            notify(
              "Notifications",
              "Three informational events are available.",
            );
          }}
        >
          ♢
        </button>

        <button
          className="nimble-system-health"
          type="button"
          onClick={toggleInspector}
        >
          <span
            className="nimble-status-dot nimble-status-dot--success"
            aria-hidden="true"
          />

          <span>
            <strong>Operational</strong>
            <small>246 checks passing</small>
          </span>
        </button>
      </div>
    </header>
  );
}
