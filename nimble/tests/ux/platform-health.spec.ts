import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import {
  runtimeHealthFixture,
  runtimeMissionFixture,
} from "../../apps/platform-shell/src/nimble/api/runtimeFixture";

const routes = ["/"];

async function installUxApiMocks(
  page: import("@playwright/test").Page,
) {
  await page.route(
    "http://127.0.0.1:8000/api/runtime/health",
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(runtimeHealthFixture),
      });
    },
  );

  await page.route(
    "http://127.0.0.1:8000/api/missions",
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(runtimeMissionFixture),
      });
    },
  );

  await page.route(
    "http://127.0.0.1:8000/api/auth/config",
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          mode: "local",
          enabled: false,
          issuer: null,
          client_id: null,
          redirect_uri: null,
          scopes: [],
        }),
      });
    },
  );
}

for (const route of routes) {
  test.describe(`Nimble UX health: ${route}`, () => {
    test.beforeEach(async ({ page }) => {
      await installUxApiMocks(page);
      await page.goto(route);
      await page.waitForLoadState("networkidle");
    });

    test("loads without browser errors", async ({ page }) => {
      const errors: string[] = [];
      const failedRequests: string[] = [];

      page.on("console", (message) => {
        if (message.type() === "error") {
          errors.push(message.text());
        }
      });

      page.on("pageerror", (error) => {
        errors.push(error.message);
      });

      page.on("requestfailed", (request) => {
        failedRequests.push(
          `${request.method()} ${request.url()} :: ${
            request.failure()?.errorText ?? "unknown failure"
          }`,
        );
      });

      await page.reload();
      await page.waitForLoadState("networkidle");

      expect(
        failedRequests,
        `Failed requests:\n${failedRequests.join("\n")}`,
      ).toEqual([]);

      expect(
        errors,
        `Browser errors:\n${errors.join("\n")}`,
      ).toEqual([]);
    });

    test("has valid page structure", async ({ page }) => {
      await expect(page.locator("body")).toBeVisible();

      const main = page.locator("main");

      await expect(
        main,
        "Every application route should expose a main landmark.",
      ).toHaveCount(1);

      await expect(
        page.locator("h1"),
        "Every primary route should have one visible H1.",
      ).toHaveCount(1);

      await expect(page.locator("h1")).toBeVisible();
    });

    test("has no serious accessibility violations", async ({ page }) => {
      const results = await new AxeBuilder({ page })
        .withTags([
          "wcag2a",
          "wcag2aa",
          "wcag21a",
          "wcag21aa",
          "wcag22aa",
        ])
        .analyze();

      const blockingViolations = results.violations.filter(
        (violation) =>
          violation.impact === "critical" ||
          violation.impact === "serious",
      );

      expect(blockingViolations).toEqual([]);
    });

    test("does not overflow horizontally", async ({ page }) => {
      const overflow = await page.evaluate(() => {
        const viewportWidth =
          document.documentElement.clientWidth;

        const offenders = Array.from(
          document.querySelectorAll<HTMLElement>("body *"),
        )
          .map((element) => {
            const rect = element.getBoundingClientRect();
            const style = window.getComputedStyle(element);

            return {
              tag: element.tagName.toLowerCase(),
              id: element.id,
              className:
                typeof element.className === "string"
                  ? element.className
                  : "",
              left: Math.round(rect.left),
              right: Math.round(rect.right),
              width: Math.round(rect.width),
              minWidth: style.minWidth,
              overflowX: style.overflowX,
              text: element.textContent
                ?.trim()
                .replace(/\s+/g, " ")
                .slice(0, 100),
            };
          })
          .filter(
            (element) =>
              element.right > viewportWidth + 1 ||
              element.left < -1 ||
              element.width > viewportWidth + 1,
          )
          .sort((a, b) => b.width - a.width)
          .slice(0, 25);

        return {
          viewportWidth,
          contentWidth:
            document.documentElement.scrollWidth,
          offenders,
        };
      });

      expect(
        overflow.contentWidth,
        `Horizontal overflow detected:\n${JSON.stringify(
          overflow,
          null,
          2,
        )}`,
      ).toBeLessThanOrEqual(
        overflow.viewportWidth + 1,
      );
    });

    test("interactive controls have accessible names", async ({ page }) => {
      const unnamedControls = await page
        .locator(
          [
            "button:not([aria-label]):not([aria-labelledby])",
            "a:not([aria-label]):not([aria-labelledby])",
            "input:not([aria-label]):not([aria-labelledby])",
          ].join(","),
        )
        .evaluateAll((elements) =>
          elements
            .filter((element) => {
              const text = element.textContent?.trim() ?? "";
              const title = element.getAttribute("title") ?? "";
              const placeholder =
                element.getAttribute("placeholder") ?? "";

              return !text && !title && !placeholder;
            })
            .map((element) => element.outerHTML),
        );

      expect(unnamedControls).toEqual([]);
    });

    test("supports keyboard focus", async ({ page }) => {
      await page.keyboard.press("Tab");

      const focused = await page.evaluate(() => {
        const element = document.activeElement;

        return {
          tag: element?.tagName ?? null,
          bodyFocused: element === document.body,
        };
      });

      expect(focused.bodyFocused).toBe(false);
      expect(focused.tag).not.toBeNull();
    });
  });
}
