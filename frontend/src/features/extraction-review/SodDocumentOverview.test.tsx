import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { SodDocumentOverview } from "./SodDocumentOverview";
import type { ReviewField } from "./types";

function makeField(fieldId: string, label: string, value: string, pocSuggestion: string): ReviewField {
  return {
    fieldId,
    deficiencyId: fieldId,
    label,
    fieldType: "sod",
    candidates: [],
    revisions: [{
      revisionId: `${fieldId}-revision`,
      revisionNumber: 1,
      value,
      origin: "Extracted",
      evidence: null,
      current: true,
    }],
    evidenceItems: [{
      pageNumber: fieldId === "deficiency-1" ? 4 : 9,
      fullSnippet: `${label} complete source page text`,
      source: "native-text",
      highlight: { x: 0, y: 0, width: 1, height: 1 },
    }],
    currentRevisionId: `${fieldId}-revision`,
    unresolved: false,
    reapprovalRequired: false,
    pocSuggestion,
  };
}

describe("SodDocumentOverview", () => {
  it("shows only the selected deficiency with its complete structured content", () => {
    render(
      <SodDocumentOverview
        fields={[
          makeField("deficiency-1", "F0686", "Full first SOD.\n1. First finding\nA. Record review", "Correct pressure injury controls."),
          makeField("deficiency-2", "F0880", "Full second SOD.", "Retrain staff on infection control."),
        ]}
        selectedFieldId="deficiency-1"
      />,
    );

    expect(screen.getByRole("heading", { name: "2 deficiencies found" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "F0686" })).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "F0880" })).not.toBeInTheDocument();
    expect(screen.getByText("Full first SOD.")).toBeInTheDocument();
    expect(screen.getByText("First finding")).toBeInTheDocument();
    expect(screen.getByText("Record review")).toBeInTheDocument();
    expect(screen.queryByText("Full second SOD.")).not.toBeInTheDocument();
    expect(screen.getByText("Correct pressure injury controls.")).toBeInTheDocument();
    expect(screen.queryByText("Retrain staff on infection control.")).not.toBeInTheDocument();
    expect(screen.getByText("F0686 complete source page text")).toBeInTheDocument();
    expect(screen.queryByText("F0880 complete source page text")).not.toBeInTheDocument();
    expect(screen.getByText("Page 4")).toBeInTheDocument();
    expect(screen.queryByText("Page 9")).not.toBeInTheDocument();
  });

  it("renders the LLM per-point POC response as structured content", () => {
    render(
      <SodDocumentOverview
        fields={[
          makeField(
            "deficiency-1",
            "F0686",
            "1. Repositioning was not documented.",
            JSON.stringify([
              {
                label: "1.",
                text: "Repositioning was not documented.",
                poc: "Audit repositioning records each shift.",
              },
              {
                label: "A.",
                text: "Record review showed missing documentation.",
                poc: "Review a sample of treatment records monthly.",
              },
            ]),
          ),
        ]}
        selectedFieldId="deficiency-1"
      />,
    );

    expect(screen.getByText("Audit repositioning records each shift.")).toBeInTheDocument();
    expect(screen.getByText("Review a sample of treatment records monthly.").parentElement).toHaveClass(
      "structured-sod__point--level-2",
    );
    expect(screen.queryByText(/\"poc\"/)).not.toBeInTheDocument();
  });
});