import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { StageTimeline } from "./StageTimeline";

describe("StageTimeline", () => {
  it("presents required failed stages as failed", () => {
    render(
      <StageTimeline
        stages={[
          { id: "upload", label: "Upload validation", detail: "Accepted", status: "complete" },
          { id: "ocr", label: "OCR fallback", detail: "Pages 29-31", status: "failed" },
        ]}
      />,
    );

    expect(screen.getByText("OCR fallback")).toBeInTheDocument();
    expect(screen.getByText("Failed")).toBeInTheDocument();
    expect(screen.getAllByText("Complete")).toHaveLength(1);
  });
});