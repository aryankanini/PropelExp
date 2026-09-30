import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ConfirmationPanel } from "./ConfirmationPanel";
import { UncertaintyResolution } from "./UncertaintyResolution";
import type { ReviewField } from "./types";

const field: ReviewField = {
  fieldId: "field-1",
  deficiencyId: "deficiency-1",
  label: "F-tag",
  fieldType: "f_tag",
  candidates: [{
    candidateId: "candidate-1",
    value: "F880",
    confidence: 0.68,
    uncertainty: "Conflict",
    origin: "Extracted",
    revisionId: "revision-1",
    evidence: {
      pageNumber: 24,
      fullSnippet: "The facility failed to maintain hand hygiene.",
      source: "ocr",
      highlight: { x: 0.1, y: 0.2, width: 0.5, height: 0.1 },
    },
  }],
  revisions: [],
  evidenceItems: [],
  currentRevisionId: "revision-1",
  unresolved: true,
  reapprovalRequired: false,
  pocSuggestion: null,
};

describe("uncertainty resolution", () => {
  it("submits a supported candidate and keeps originals visible", async () => {
    const resolve = vi.fn().mockResolvedValue({ status: "resolved" });
    render(<UncertaintyResolution field={field} onResolve={resolve} />);

    fireEvent.click(screen.getByRole("radio", { name: /F880/ }));
    fireEvent.click(screen.getByRole("button", { name: "Resolve value" }));

    await waitFor(() => expect(resolve).toHaveBeenCalledWith({ kind: "select", expectedRevisionId: "revision-1", candidateId: "candidate-1" }));
    expect(screen.getByText("F880")).toBeInTheDocument();
  });

  it("retains correction input after a stale conflict", async () => {
    const resolve = vi.fn().mockResolvedValue({ status: "stale", currentRevisionId: "revision-2" });
    render(<UncertaintyResolution field={field} onResolve={resolve} />);

    fireEvent.change(screen.getByLabelText("Or enter a correction"), { target: { value: "F881" } });
    fireEvent.click(screen.getByRole("button", { name: "Resolve value" }));

    expect(await screen.findByText(/Reload current values/)).toBeInTheDocument();
    expect(screen.getByLabelText("Or enter a correction")).toHaveValue("F881");
  });

  it("keeps confirmation and drafting blocked when unresolved", async () => {
    const resolve = vi.fn().mockResolvedValue({ status: "resolved" });
    render(<UncertaintyResolution field={field} onResolve={resolve} />);

    fireEvent.click(screen.getByRole("button", { name: "Leave unresolved" }));

    expect(await screen.findByText(/Confirmation and POC drafting are blocked/)).toBeInTheDocument();
  });
});

describe("confirmation", () => {
  it("names every blocker and keeps POC generation disabled", () => {
    render(
      <ConfirmationPanel
        deficiencyId="F880"
        expectedRevisionId="revision-1"
        blockers={[
          { fieldId: "f-tag", label: "F-tag", reason: "Unresolved conflict" },
          { fieldId: "sod", label: "Complete SOD", reason: "Missing evidence" },
        ]}
        onConfirm={vi.fn()}
        onReload={vi.fn()}
      />,
    );

    expect(screen.getByText(/F-tag/)).toBeInTheDocument();
    expect(screen.getByText(/Complete SOD/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate POC" })).toBeDisabled();
  });

  it("requires reload after stale confirmation", async () => {
    const confirm = vi.fn().mockResolvedValue({ status: "stale", currentRevisionId: "revision-2" });
    render(
      <ConfirmationPanel
        deficiencyId="F880"
        expectedRevisionId="revision-1"
        blockers={[]}
        onConfirm={confirm}
        onReload={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Confirm deficiency" }));

    expect(await screen.findByRole("button", { name: "Reload current values" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate POC" })).toBeDisabled();
  });

  it("unlocks POC generation after confirmation", async () => {
    render(
      <ConfirmationPanel
        deficiencyId="F880"
        expectedRevisionId="revision-1"
        blockers={[]}
        onConfirm={vi.fn().mockResolvedValue({ status: "confirmed" })}
        onReload={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Confirm deficiency" }));

    await waitFor(() => expect(screen.getByRole("button", { name: "Generate POC" })).toBeEnabled());
  });
});