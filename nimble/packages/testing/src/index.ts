export interface NimbleAccessibilityAssertion {
  readonly name: string;
  readonly passed: boolean;
  readonly details?: string;
}

export function requirePassingAssertions(
  assertions: readonly NimbleAccessibilityAssertion[],
): void {
  const failures = assertions.filter(
    (assertion) => !assertion.passed,
  );

  if (failures.length > 0) {
    throw new Error(
      `Nimble validation failed: ${failures
        .map((failure) => failure.name)
        .join(", ")}`,
    );
  }
}
