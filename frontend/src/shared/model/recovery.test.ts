import { describe, expect, it } from "vitest";

import { selectRecoveryAction } from "./recovery";

describe("selectRecoveryAction", () => {
  it.each([
    [{ retryable: true, replacementRequired: false, providerExhausted: false }, "retry"],
    [{ retryable: false, replacementRequired: true, providerExhausted: false }, "replace"],
    [{ retryable: true, replacementRequired: false, providerExhausted: true }, "retry-later"],
    [{ retryable: false, replacementRequired: false, providerExhausted: false }, "return"],
  ] as const)("selects the valid primary action", (context, expected) => {
    expect(selectRecoveryAction(context).kind).toBe(expected);
  });
});