import { describe, expect, it } from "vitest";

import { structureSodText } from "./sodStructure";

describe("structureSodText", () => {
  it("structures nested findings and joins wrapped PDF lines", () => {
    const blocks = structureSodText([
      "Based on interviews and document review, the",
      "facility failed to monitor patient status.",
      "Findings include:",
      "1. The facility failed to ensure patient care",
      "technicians reported changes.",
      "A. Medical Record Review",
      "i. Patient #1 had an abnormal reading.",
      "a. The provider was not notified.",
    ].join("\n"));

    expect(blocks).toEqual([
      {
        kind: "narrative",
        text: "Based on interviews and document review, the facility failed to monitor patient status.",
      },
      { kind: "heading", text: "Findings include:" },
      {
        kind: "point",
        marker: "1.",
        level: 1,
        text: "The facility failed to ensure patient care technicians reported changes.",
      },
      { kind: "point", marker: "A.", level: 2, text: "Medical Record Review" },
      {
        kind: "point",
        marker: "i.",
        level: 3,
        text: "Patient #1 had an abnormal reading.",
      },
      {
        kind: "point",
        marker: "a.",
        level: 4,
        text: "The provider was not notified.",
      },
    ]);
  });

  it("keeps an unmarked SOD as complete narrative text", () => {
    expect(structureSodText("First wrapped line\ncontinues here.")).toEqual([
      { kind: "narrative", text: "First wrapped line continues here." },
    ]);
  });
});