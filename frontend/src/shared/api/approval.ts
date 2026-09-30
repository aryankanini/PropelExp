import { apiUrl } from "./client";
import type { ApprovalResponse } from "../model/approval";

interface ApproveRevisionInput {
  caseId: string;
  sessionId: string;
  actorId: string;
  actorRole: string;
  revisionId: string;
}

export async function approveRevision(input: ApproveRevisionInput): Promise<ApprovalResponse> {
  const response = await fetch(apiUrl(`/api/v1/cases/${encodeURIComponent(input.caseId)}/approval`), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Session-ID": input.sessionId,
      "X-Actor-ID": input.actorId,
      "X-Actor-Role": input.actorRole,
    },
    body: JSON.stringify({ revision_id: input.revisionId }),
  });
  const result = (await response.json()) as ApprovalResponse & { detail?: string };
  if (!response.ok && response.status !== 409) {
    throw new Error(result.detail ?? `Approval failed with status ${response.status}.`);
  }
  return result;
}