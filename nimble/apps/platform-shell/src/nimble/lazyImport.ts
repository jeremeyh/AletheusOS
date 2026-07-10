export interface LazyImportOptions {
  readonly retries?: number;
  readonly retryDelayMs?: number;
}

export async function lazyImportWithRetry<T>(
  importer: () => Promise<T>,
  options: LazyImportOptions = {},
): Promise<T> {
  const retries = options.retries ?? 2;
  const retryDelayMs =
    options.retryDelayMs ?? 250;

  let lastError: unknown;

  for (
    let attempt = 0;
    attempt <= retries;
    attempt += 1
  ) {
    try {
      return await importer();
    } catch (error) {
      lastError = error;

      if (attempt >= retries) {
        break;
      }

      await delay(
        retryDelayMs
        * (attempt + 1),
      );
    }
  }

  throw lastError;
}

function delay(
  milliseconds: number,
): Promise<void> {
  return new Promise((resolve) => {
    window.setTimeout(
      resolve,
      milliseconds,
    );
  });
}
