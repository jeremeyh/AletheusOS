(async () => {
  "use strict";

  const normalize = value =>
    String(value || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();

  let map;

  try {
    const response =
      await fetch("./mc85e2-semantic-map.json", {
        cache: "no-store"
      });

    map = await response.json();
  } catch (error) {
    console.error(
      "[MC85E2] Semantic map unavailable",
      error
    );
    return;
  }

  const candidates = [
    ...document.querySelectorAll(
      "button, a, [role='button'], nav *, input"
    )
  ];

  const resolution = [];

  for (const surface of map.surfaces) {
    let matched = null;
    let matchedAlias = null;

    for (const alias of surface.aliases) {
      const needle = normalize(alias);

      matched = candidates.find(node => {
        const values = [
          node.textContent,
          node.getAttribute("aria-label"),
          node.getAttribute("title"),
          node.getAttribute("placeholder")
        ];

        return values.some(value =>
          normalize(value).includes(needle)
        );
      });

      if (matched) {
        matchedAlias = alias;
        break;
      }
    }

    if (!matched) {
      resolution.push({
        id: surface.id,
        canonicalName: surface.canonicalName,
        status: "unresolved"
      });

      continue;
    }

    /*
     * Semantic identity only.
     *
     * No class is added.
     * No inline style is added.
     * No visible text is replaced.
     * No event listener is replaced.
     */

    matched.dataset.aletheusSemanticId = surface.id;
    matched.dataset.aletheusCanonicalName =
      surface.canonicalName;

    if (!matched.getAttribute("aria-label")) {
      matched.setAttribute(
        "aria-label",
        surface.canonicalName
      );
    }

    resolution.push({
      id: surface.id,
      canonicalName: surface.canonicalName,
      alias: matchedAlias,
      status: "resolved"
    });
  }

  window.__ALETHEUSOS_MC85E2__ = {
    authority: map.authority,
    resolution
  };

  console.group(
    "[MC85E2] Direct authentic surface semantic convergence"
  );

  console.table(resolution);

  console.log(
    "Visual authority:",
    map.authority.visual
  );

  console.log(
    "Semantic authority:",
    map.authority.semantic
  );

  console.log(
    "No historical control geometry was replaced."
  );

  console.groupEnd();
})();
/* ALETHEUSOS_WORKSPACE_STUDIO_READ_ONLY_BINDING_V1 */
(async function bindWorkspaceStudioReadOnly() {
  "use strict";

  const WORKSPACE_SCHEMA =
    "aletheusos.workspace-studio.read-model.v1";

  const WORKSPACE_SURFACE_ID =
    "workspace-studio";

  const SNAPSHOT_PATH =
    "./src/workspace_studio_read_model.generated.json";

  const ADAPTER_PATH =
    "./workspace_studio_read_model_adapter.js";

  const EVENT_NAME =
    "aletheusos:workspace-studio-inspect";

  function normalize(value) {
    return String(value || "")
      .trim()
      .replace(/\s+/g, " ")
      .toLowerCase();
  }

  function dispatchInspection(
    detail
  ) {
    document.dispatchEvent(
      new CustomEvent(
        EVENT_NAME,
        {
          detail
        }
      )
    );
  }

  try {
    const [
      adapterModule,
      snapshotResponse
    ] = await Promise.all([
      import(ADAPTER_PATH),

      fetch(
        SNAPSHOT_PATH,
        {
          cache: "no-store"
        }
      )
    ]);

    if (!snapshotResponse.ok) {
      throw new Error(
        "Workspace Studio read model unavailable"
      );
    }

    const snapshot =
      await snapshotResponse.json();

    if (
      snapshot.schema !==
      WORKSPACE_SCHEMA
    ) {
      throw new Error(
        "Workspace Studio schema mismatch"
      );
    }

    const adapter =
      adapterModule
        .createWorkspaceStudioAdapter(
          snapshot
        );

    const api = Object.freeze({
      surfaceId:
        WORKSPACE_SURFACE_ID,

      status:
        adapter.status,

      inspect(operation) {
        const result =
          adapter.inspect(
            operation
          );

        dispatchInspection(
          result
        );

        return result;
      },

      snapshot() {
        return adapter.snapshot();
      }
    });

    Object.defineProperty(
      window,
      "AletheusOSWorkspaceStudio",
      {
        value: api,
        configurable: false,
        writable: false,
        enumerable: false
      }
    );

    const aliases =
      new Set([
        "workspace studio",
        "workspace"
      ]);

    const candidates =
      document.querySelectorAll(
        [
          "button",
          "[role='button']",
          "a",
          "[data-surface]",
          "[data-destination]",
          "[data-action]"
        ].join(",")
      );

    for (
      const control
      of candidates
    ) {
      const values = [
        control.textContent,
        control.getAttribute(
          "aria-label"
        ),
        control.getAttribute(
          "title"
        ),
        control.getAttribute(
          "data-surface"
        ),
        control.getAttribute(
          "data-destination"
        ),
        control.getAttribute(
          "data-action"
        )
      ];

      const matches =
        values.some(
          value =>
            aliases.has(
              normalize(value)
            )
        );

      if (!matches) {
        continue;
      }

      if (
        control.dataset
          .aletheusWorkspaceStudioBound
        === "true"
      ) {
        continue;
      }

      control.dataset
        .aletheusWorkspaceStudioBound =
          "true";

      control.addEventListener(
        "click",
        () => {
          api.inspect(
            "inspect_workspace_state"
          );
        },
        {
          passive: true
        }
      );
    }

    dispatchInspection(
      Object.freeze({
        status: "READ_ONLY",
        operation:
          "workspace_studio_binding_ready",
        section: "runtime",
        data: snapshot.runtime
      })
    );
  } catch (error) {
    console.error(
      "[MC85E2] Workspace Studio "
      + "read-only binding unavailable",
      error
    );

    dispatchInspection(
      Object.freeze({
        status:
          "DEGRADED_READ_ONLY",

        operation:
          "workspace_studio_binding",

        reason:
          String(
            error &&
            error.message
              ? error.message
              : error
          )
      })
    );
  }
})();
