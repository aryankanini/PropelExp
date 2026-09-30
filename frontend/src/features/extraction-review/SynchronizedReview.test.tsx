import { fireEvent, render, screen } from "@testing-library/react";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";

import { EvidenceViewer } from "./EvidenceViewer";
import { FieldEditor } from "./FieldEditor";
import type { ReviewCandidate, ReviewField } from "./types";

const candidates: ReviewCandidate[] = [
  {
    candidateId: "candidate-1",
    value: "F880",
    confidence: 0.68,
    uncertainty: "Conflicts with F881",
    origin: "Extracted",
    revisionId: "revision-1",
    evidence: {
      pageNumber: 24,
      fullSnippet: "The facility failed to maintain hand hygiene practices.",
      source: "ocr",
      highlight: { x: 0.1, y: 0.2, width: 0.5, height: 0.1 },
    },
  },
  {
    candidateId: "candidate-2",
    value: "F881",
    confidence: 0.64,
    uncertainty: "Conflicts with F880",
    origin: "Extracted",
    revisionId: "revision-1",
    evidence: {
      pageNumber: 25,
      fullSnippet: "Glove changes occurred without documented hand hygiene.",
      source: "ocr",
      highlight: { x: 0.1, y: 0.4, width: 0.6, height: 0.1 },
    },
  },
];

const field: ReviewField = {
  fieldId: "field-1",
  deficiencyId: "deficiency-1",
  label: "F-tag",
  fieldType: "f_tag",
  candidates,
  revisions: [{
    revisionId: "revision-1",
    revisionNumber: 1,
    value: "F880",
    origin: "Extracted",
    evidence: candidates[0].evidence,
    current: true,
  }],
  evidenceItems: [],
  currentRevisionId: "revision-1",
  unresolved: true,
  reapprovalRequired: false,
  pocSuggestion: null,
};

function ReviewHarness() {
  const [selectedId, setSelectedId] = useState(candidates[0].candidateId);
  const selected = candidates.find((candidate) => candidate.candidateId === selectedId) ?? null;
  return (
    <>
      <FieldEditor
        field={field}
        selectedCandidateId={selectedId}
        onSelectCandidate={setSelectedId}
        onSaveCorrection={vi.fn()}
      />
      <EvidenceViewer candidate={selected} />
    </>
  );
}

describe("synchronized review", () => {
  it("updates the page, full snippet, metadata, and highlight with selection", () => {
    render(<ReviewHarness />);

    const candidateButton = screen.getByText("F881").closest("button");
    expect(candidateButton).not.toBeNull();
    fireEvent.click(candidateButton!);

    expect(screen.getByText(/Page 25 · OCR/)).toBeInTheDocument();
    expect(screen.getByText("64% confidence")).toBeInTheDocument();
    expect(screen.getByText(candidates[1].evidence.fullSnippet)).toHaveProperty("tagName", "MARK");
  });

  it("searches the complete snippet without replacing the selected evidence", () => {
    render(<EvidenceViewer candidate={candidates[0]} />);

    fireEvent.change(screen.getByRole("searchbox"), { target: { value: "hand hygiene" } });

    expect(screen.getByText("1 matches in complete snippet")).toBeInTheDocument();
    expect(screen.getByText(candidates[0].evidence.fullSnippet)).toBeInTheDocument();
  });

  it("rejects an empty correction without submitting", () => {
    const save = vi.fn();
    render(
      <FieldEditor
        field={field}
        selectedCandidateId="candidate-1"
        onSelectCandidate={vi.fn()}
        onSaveCorrection={save}
      />,
    );

    fireEvent.change(screen.getByLabelText("Current authoritative value"), { target: { value: " " } });
    fireEvent.click(screen.getByRole("button", { name: "Save correction" }));

    expect(screen.getByRole("alert")).toHaveTextContent("Enter a correction");
    expect(save).not.toHaveBeenCalled();
  });
});