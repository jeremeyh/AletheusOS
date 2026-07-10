import * as Popover from "@radix-ui/react-popover";

import {
  useCurrentPrincipal,
} from "../api/identityQueries";

export function PrincipalPanel() {
  const {
    data: principal,
    error,
    isPending,
  } = useCurrentPrincipal();

  return (
    <Popover.Root>
      <Popover.Trigger asChild>
        <button
          className="nimble-principal-trigger"
          type="button"
          aria-label="Open authenticated principal details"
        >
          <span className="nimble-user__avatar">
            {principal
              ? initials(principal.displayName)
              : "?"}
          </span>

          <span className="nimble-principal-trigger__identity">
            <strong>
              {principal?.displayName
                ?? (isPending ? "Resolving…" : "Unknown")}
            </strong>

            <small>
              {principal?.roles
                .map(formatRole)
                .join(", ")
                ?? "Identity unavailable"}
            </small>
          </span>
        </button>
      </Popover.Trigger>

      <Popover.Portal>
        <Popover.Content
          className="nimble-principal-panel"
          sideOffset={10}
          align="end"
        >
          <header>
            <p className="nimble-panel__eyebrow">
              Authenticated principal
            </p>

            <h2>
              {principal?.displayName
                ?? "Identity unavailable"}
            </h2>
          </header>

          {error && (
            <section className="nimble-command-failure">
              <h3>Identity resolution failed</h3>
              <p>{error.message}</p>
            </section>
          )}

          {principal && (
            <>
              <dl>
                <div>
                  <dt>Subject</dt>
                  <dd>{principal.subjectId}</dd>
                </div>

                <div>
                  <dt>Authentication</dt>
                  <dd>{principal.authenticationMethod}</dd>
                </div>

                <div>
                  <dt>Status</dt>
                  <dd>
                    {principal.authenticated
                      ? "Authenticated"
                      : "Unauthenticated"}
                  </dd>
                </div>
              </dl>

              <section>
                <h3>Roles</h3>

                <div className="nimble-principal-tags">
                  {principal.roles.map((role) => (
                    <span key={role}>
                      {formatRole(role)}
                    </span>
                  ))}
                </div>
              </section>

              <section>
                <h3>Entitlements</h3>

                {principal.entitlements.length ? (
                  <div className="nimble-principal-tags">
                    {principal.entitlements.map(
                      (entitlement) => (
                        <span key={entitlement}>
                          {entitlement}
                        </span>
                      ),
                    )}
                  </div>
                ) : (
                  <p>
                    No command entitlements were disclosed.
                  </p>
                )}
              </section>
            </>
          )}

          <Popover.Arrow className="nimble-principal-panel__arrow" />
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );
}

function initials(value: string): string {
  return value
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("");
}

function formatRole(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
}
