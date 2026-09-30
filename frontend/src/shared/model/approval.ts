export type ApprovalRole = "compliance_reviewer" | "compliance_leader";

export interface ApprovalBlocker {
  code: string;
  message: string;
  section: string | null;
}

export interface ApprovalState {
  status: "unapproved" | "approved" | "changes_requested" | "reapproval_required";
  revision_id: string | null;
  approved_by: string | null;
  approved_at: string | null;
}

export interface ApprovalResponse {
  approved: boolean;
  approval: ApprovalState;
  blockers: ApprovalBlocker[];
  copy_enabled: boolean;
  download_enabled: boolean;
}

export interface ReviewSection {
  id: string;
  title: string;
  content: string;
  provenance: string;
}

export interface RevisionEntry {
  revisionId: string;
  author: string;
  timestamp: string;
  summary: string;
  current: boolean;
}

export interface ApprovalReviewModel {
  caseId: string;
  deficiencyTag: string;
  facilityName: string;
  revisionId: string;
  revisionLabel: string;
  role: ApprovalRole;
  evidence: string[];
  sections: ReviewSection[];
  history: RevisionEntry[];
}