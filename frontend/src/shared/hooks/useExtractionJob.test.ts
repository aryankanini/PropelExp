import { describe, expect, it } from "vitest";

import { advanceEstimatedProgress } from "./useExtractionJob";

describe("advanceEstimatedProgress", () => {
  it("moves generation progress without reaching completion", () => {
    expect(advanceEstimatedProgress(85)).toBe(86);
    expect(advanceEstimatedProgress(97)).toBe(98);
    expect(advanceEstimatedProgress(98)).toBe(98);
  });
});