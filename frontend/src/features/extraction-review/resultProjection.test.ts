import { describe, expect, it } from "vitest";

import { projectReviewResults } from "./resultProjection";

describe("projectReviewResults", () => {
  it("retains confirmed work and omits failed unconfirmed content", () => {
    const projected = projectReviewResults(
      [
        { pageNumber: 1, content: "reviewed", confirmed: true },
        { pageNumber: 2, content: "failed draft", confirmed: false },
        { pageNumber: 3, content: "ready", confirmed: false },
      ],
      new Set([2]),
    );

    expect(projected.map((result) => result.pageNumber)).toEqual([1, 3]);
  });
});