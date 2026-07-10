import { motion } from "motion/react";

import { navigationGroups } from "../data/shellData";
import { useNimble } from "../providers/NimbleProvider";

export function GlobalNavigation() {
  const {
    navigationExpanded,
    toggleNavigation,
    notify,
  } = useNimble();

  return (
    <motion.aside
      className="nimble-navigation"
      aria-label="Global navigation"
      animate={{
        width: navigationExpanded ? 272 : 76,
      }}
      transition={{
        type: "spring",
        stiffness: 180,
        damping: 28,
        mass: 1.2,
      }}
    >
      <header className="nimble-brand">
        <button
          className="nimble-brand__mark"
          type="button"
          aria-label="Open application switcher"
          onClick={() => {
            notify(
              "Application switcher",
              "AletheusOS applications will inherit this Nimble surface.",
            );
          }}
        >
          A
        </button>

        {navigationExpanded && (
          <motion.div
            className="nimble-brand__identity"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <strong>AletheusOS</strong>
            <span>Nimble™ Experience</span>
          </motion.div>
        )}

        <button
          className="nimble-icon-button"
          type="button"
          aria-label={
            navigationExpanded
              ? "Collapse navigation"
              : "Expand navigation"
          }
          aria-expanded={navigationExpanded}
          onClick={toggleNavigation}
        >
          {navigationExpanded ? "‹" : "›"}
        </button>
      </header>

      <nav className="nimble-navigation__body">
        {navigationGroups.map((group) => (
          <section key={group.id}>
            {navigationExpanded && (
              <p className="nimble-navigation__label">
                {group.label}
              </p>
            )}

            {group.items.map((item) => (
              <button
                key={item.id}
                type="button"
                className={`nimble-nav-item ${
                  item.id === "overview" ? "is-active" : ""
                }`}
                onClick={() => {
                  notify(
                    item.label,
                    `${item.label} is registered but not yet routed.`,
                  );
                }}
              >
                <span
                  className="nimble-nav-item__icon"
                  aria-hidden="true"
                >
                  {item.icon}
                </span>

                {navigationExpanded && (
                  <span className="nimble-nav-item__label">
                    {item.label}
                  </span>
                )}

                {navigationExpanded && item.count && (
                  <span className="nimble-nav-item__count">
                    {item.count}
                  </span>
                )}

                {navigationExpanded && item.status === "healthy" && (
                  <span
                    className="nimble-status-dot nimble-status-dot--success"
                    aria-label="Healthy"
                  />
                )}

                {navigationExpanded && item.status === "active" && (
                  <span
                    className="nimble-status-dot nimble-status-dot--active"
                    aria-label="Active"
                  />
                )}
              </button>
            ))}
          </section>
        ))}
      </nav>

      <footer className="nimble-navigation__footer">
        <button
          className="nimble-user"
          type="button"
          onClick={() => {
            notify(
              "Personalization",
              "Preferences remain visible, editable, and resettable.",
            );
          }}
        >
          <span className="nimble-user__avatar">JH</span>

          {navigationExpanded && (
            <span className="nimble-user__identity">
              <strong>Jeremey</strong>
              <small>Platform Architect</small>
            </span>
          )}
        </button>
      </footer>
    </motion.aside>
  );
}
