import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import type { ApprovalReviewModel } from "../../shared/model/approval";
import { ApprovalReview } from "./ApprovalReview";

const sections = [
  "Affected residents",
  "Others at risk",
  "Corrective measures",
  "Monitoring",
  "Completion date",
].map((title) => ({ id: title, title, content: `${title} content`, provenance: "User edited" }));

function review(role: ApprovalReviewModel["role"]): ApprovalReviewModel {
  return {
    caseId: "case-1",
    deficiencyTag: "F689",
    facilityName: "Northlake",
    revisionId: "revision-4",
    revisionLabel: "Revision 4",
    role,
    evidence: ["page-3"],
    sections,
    history: [{ revisionId: "Revision 4", author: "Morgan", timestamp: "Today", summary: "Current", current: true }],
  };
}

describe("ApprovalReview", () => {
  it("shows all five sections and lets a leader approve the current revision", () => {
    const approve = vi.fn();
    render(<ApprovalReview review={review("compliance_leader")} blockers={[]} pending={false} onApprove={approve} onRequestChanges={() => undefined} />);

    expect(screen.getAllByRole("article")).toHaveLength(5);
    fireEvent.click(screen.getByRole("button", { name: "Approve current revision" }));
    expect(approve).toHaveBeenCalledOnce();
  });

  it("disables reviewer approval and displays exact blockers", () => {
    render(<ApprovalReview review={review("compliance_reviewer")} blockers={[{ code: "stale_revision", message: "Refresh revision 5 before approval.", section: null }]} pending={false} onApprove={() => undefined} onRequestChanges={() => undefined} />);

    expect(screen.getByRole("button", { name: "Approve current revision" })).toBeDisabled();
    expect(screen.getByRole("alert")).toHaveTextContent("Refresh revision 5 before approval.");
    expect(screen.getByText("Only a compliance leader can approve this revision.")).toBeInTheDocument();
  });
});