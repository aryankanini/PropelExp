import { apiUrl } from "./client";
import type { ReapprovalState } from "../model/reapproval";

export async function requestChanges(caseId: string, sessionId: string): Promise<ReapprovalState> {
  const response = await fetch(
    apiUrl(`/api/v1/cases/${encodeURIComponent(caseId)}/approval/request-changes`),
    {
      method: "POST",
      headers: { "X-Session-ID": sessionId, "X-Actor-Role": "compliance_leader" },
    },
  );
  if (!response.ok) throw new Error("Changes could not be requested.");
  return (await response.json()) as ReapprovalState;
}