import * as Dialog from "@radix-ui/react-dialog";
import {
  useState,
} from "react";

import {
  useAuthentication,
} from "../providers/AuthenticationProvider";

export function AuthenticationPanel() {
  const authentication =
    useAuthentication();

  const [open, setOpen] =
    useState(false);

  const [token, setToken] =
    useState("");

  if (
    authentication.isPending
    || authentication.mode !== "oidc"
  ) {
    return null;
  }

  async function saveToken() {
    const normalized = token.trim();

    if (!normalized) {
      return;
    }

    await authentication
      .setAccessToken(normalized);

    setToken("");
    setOpen(false);
  }

  return (
    <Dialog.Root
      open={open}
      onOpenChange={setOpen}
    >
      <Dialog.Trigger asChild>
        <button
          className="nimble-button nimble-button--secondary"
          type="button"
        >
          Authenticate
        </button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay
          className="nimble-command__overlay"
        />

        <Dialog.Content
          className="nimble-auth-dialog"
          aria-describedby="nimble-auth-description"
        >
          <header>
            <Dialog.Title>
              OIDC access token
            </Dialog.Title>

            <Dialog.Close asChild>
              <button
                className="nimble-icon-button"
                type="button"
                aria-label="Close authentication dialog"
              >
                ×
              </button>
            </Dialog.Close>
          </header>

          <Dialog.Description
            id="nimble-auth-description"
          >
            Enter a bearer access token issued for
            the configured AletheusOS API audience.
          </Dialog.Description>

          <label>
            Access token

            <textarea
              value={token}
              onChange={(event) => {
                setToken(
                  event.target.value,
                );
              }}
              rows={8}
              autoComplete="off"
              spellCheck={false}
            />
          </label>

          <p className="nimble-auth-warning">
            This temporary development surface stores
            the token in browser session storage. It is
            cleared when the browser session ends.
          </p>

          <footer>
            <button
              className="nimble-button nimble-button--secondary"
              type="button"
              onClick={() => {
                void authentication
                  .clearAccessToken();

                setToken("");
              }}
            >
              Clear token
            </button>

            <button
              className="nimble-button nimble-button--primary"
              type="button"
              disabled={!token.trim()}
              onClick={() => {
                void saveToken();
              }}
            >
              Use token
            </button>
          </footer>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
