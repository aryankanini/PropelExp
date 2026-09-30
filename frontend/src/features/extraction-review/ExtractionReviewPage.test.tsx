import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ExtractionReviewPage } from "./ExtractionReviewPage";

const session = vi.hoisted(() => ({
  navigate: vi.fn(),
  setDeficiencyId: vi.fn(),
  reset: vi.fn(),
}));

vi.mock("../../app/SessionContext", () => ({
  useSession: () => ({
    sessionId: "session-1",
    caseId: "case-1",
    navigate: session.navigate,
    setDeficiencyId: session.setDeficiencyId,
    reset: session.reset,
  }),
}));

vi.mock("../../shared/session/useEndSession", () => ({
  useEndSession: () => ({ status: "idle", endSession: vi.fn() }),
}));

describe("ExtractionReviewPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("confirms the selected deficiency and continues to POC authoring", async () => {
    const reviewField = {
      field_id: "deficiency-1",
      deficiency_id: "deficiency-1",
      label: "F0686",
      field_type: "sod",
      candidates: [],
      revisions: [
        {
          revision_id: "review-revision-1",
          revision_number: 1,
          value: "Complete statement of deficiency",
          origin: "Extracted",
          evidence: null,
        },
      ],
      evidence_items: [],
      current_revision_id: "review-revision-1",
      unresolved: false,
      reapproval_required: false,
      poc_suggestion: null,
    };
    const providerFields = [
      {
        ...reviewField,
        field_id: "provider:name",
        deficiency_id: null,
        label: "Provider name",
        field_type: "provider",
        revisions: [{ ...reviewField.revisions[0], value: "North Valley Care Center" }],
      },
      {
        ...reviewField,
        field_id: "provider:identification-number",
        deficiency_id: null,
        label: "Provider identification number",
        field_type: "provider",
        revisions: [{ ...reviewField.revisions[0], value: "12-3456" }],
      },
    ];
    const request = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(
        new Response(JSON.stringify([...providerFields, reviewField]), { status: 200 }),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({ poc_generation_eligible: true }),
          { status: 200 },
        ),
      );

    render(<ExtractionReviewPage />);
    expect(await screen.findByText("North Valley Care Center")).toBeInTheDocument();
    expect(screen.getByText("12-3456")).toBeInTheDocument();
    fireEvent.click(
      screen.getByRole("button", {
        name: "Confirm and continue to POC",
      }),
    );

    await waitFor(() => {
      expect(session.setDeficiencyId).toHaveBeenCalledWith("deficiency-1");
      expect(session.navigate).toHaveBeenCalledWith("poc-authoring");
    });
    expect(request).toHaveBeenLastCalledWith(
      expect.stringContaining(
        "/sessions/session-1/deficiencies/deficiency-1/confirmation",
      ),
      expect.objectContaining({ method: "PATCH" }),
    );
  });
});