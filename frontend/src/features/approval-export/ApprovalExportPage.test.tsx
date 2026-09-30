import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { approveRevision } from "../../shared/api/approval";
import { exportApprovedRevision } from "../../shared/api/export";
import { ApprovalExportPage } from "./ApprovalExportPage";

const { useSessionStatusMock } = vi.hoisted(() => ({
  useSessionStatusMock: vi.fn(),
}));

vi.mock("../../shared/api/approval", () => ({ approveRevision: vi.fn() }));
vi.mock("../../shared/api/export", () => ({ exportApprovedRevision: vi.fn() }));
vi.mock("../../shared/api/reapproval", () => ({ requestChanges: vi.fn() }));
vi.mock("../../shared/api/poc", () => {
  const sectionNames = [
    "affected_residents",
    "others_at_risk",
    "corrective_measures",
    "monitoring",
    "completion_date",
  ] as const;
  return {
    pocSectionOrder: sectionNames,
    createPocApi: () => ({
      load: async () => ({
        deficiency_id: "deficiency-1",
        current_revision_id: "revision-4",
        revisions: [{
          revision_id: "revision-4",
          deficiency_revision_id: "deficiency-revision-1",
          content: Object.fromEntries(sectionNames.map((name) => [name, name])),
          section_origins: Object.fromEntries(
            sectionNames.map((name) => [name, "ai_generated"]),
          ),
          grounded_claims: [],
          missing_information: [],
          status: "unapproved",
        }],
      }),
    }),
  };
});
vi.mock("../../app/SessionContext", () => ({
  useSession: () => ({
    sessionId: "local-session",
    caseId: "stale-case",
    deficiencyId: "deficiency-1",
    setCaseId: vi.fn(),
  }),
}));
vi.mock("../../shared/session/useSessionStatus", () => ({
  useSessionStatus: useSessionStatusMock,
}));

describe("ApprovalExportPage", () => {
  beforeEach(() => {
    useSessionStatusMock.mockReturnValue({
      storage: "session_only",
      remaining_inactivity_seconds: 3600,
      active_case_id: "case-1",
    });
  });

  it("shows export only after the API confirms current-revision approval", async () => {
    vi.mocked(exportApprovedRevision).mockResolvedValue({
      format: "copy",
      content: "APPROVED POC DRAFT\n\nAffected residents\nAffected residents",
      media_type: "text/plain",
      filename: null,
    });
    vi.mocked(approveRevision).mockResolvedValue({
      approved: true,
      approval: {
        status: "approved",
        revision_id: "revision-4",
        approved_by: "leader-1",
        approved_at: "2026-09-24T10:42:00Z",
      },
      blockers: [],
      copy_enabled: true,
      download_enabled: true,
    });
    render(<ApprovalExportPage />);

    expect(screen.queryByRole("heading", { name: "Approved POC draft" })).not.toBeInTheDocument();
    const approveButton = await screen.findByRole("button", {
      name: "Approve current revision",
    });
    await waitFor(() => expect(approveButton).toBeEnabled());
    fireEvent.click(approveButton);

    await waitFor(() => expect(screen.getByRole("heading", { name: "Approved POC draft" })).toBeInTheDocument());
    expect(screen.queryByText("Approved content is empty")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Copy draft" })).toBeEnabled();
    expect(approveRevision).toHaveBeenCalledWith(
      expect.objectContaining({ caseId: "case-1", revisionId: "revision-4" }),
    );
  });

  it("blocks approval while the authoritative case is loading", async () => {
    useSessionStatusMock.mockReturnValue(null);
    render(<ApprovalExportPage />);

    const approveButton = await screen.findByRole("button", {
      name: "Approving...",
    });

    expect(approveButton).toBeDisabled();
    fireEvent.click(approveButton);
    expect(approveRevision).not.toHaveBeenCalled();
  });
});