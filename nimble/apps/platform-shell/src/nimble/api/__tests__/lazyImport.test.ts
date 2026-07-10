import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  lazyImportWithRetry,
} from "../../lazyImport";

describe("lazy import retry", () => {
  it("returns the imported module", async () => {
    const importer = vi.fn()
      .mockResolvedValue({
        value: 42,
      });

    await expect(
      lazyImportWithRetry(importer),
    ).resolves.toEqual({
      value: 42,
    });

    expect(importer).toHaveBeenCalledTimes(1);
  });

  it("retries transient failures", async () => {
    const importer = vi.fn()
      .mockRejectedValueOnce(
        new Error("temporary failure"),
      )
      .mockResolvedValue({
        value: "loaded",
      });

    await expect(
      lazyImportWithRetry(
        importer,
        {
          retries: 1,
          retryDelayMs: 0,
        },
      ),
    ).resolves.toEqual({
      value: "loaded",
    });

    expect(importer).toHaveBeenCalledTimes(2);
  });

  it("throws after retry exhaustion", async () => {
    const importer = vi.fn()
      .mockRejectedValue(
        new Error("permanent failure"),
      );

    await expect(
      lazyImportWithRetry(
        importer,
        {
          retries: 2,
          retryDelayMs: 0,
        },
      ),
    ).rejects.toThrow(
      "permanent failure",
    );

    expect(importer).toHaveBeenCalledTimes(3);
  });
});
