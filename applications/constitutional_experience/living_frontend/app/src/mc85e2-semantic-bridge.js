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
