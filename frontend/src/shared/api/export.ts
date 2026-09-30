import { apiUrl } from "./client";
import type { ExportFailure, ExportFormat, ExportResult } from "../model/export";

export async function exportApprovedRevision(
  caseId: string,
  sessionId: string,
  format: ExportFormat,
): Promise<ExportResult | ExportFailure> {
  const response = await fetch(
    apiUrl(`/api/v1/cases/${encodeURIComponent(caseId)}/export?format=${format}`),
    { headers: { "X-Session-ID": sessionId } },
  );
  const result = (await response.json()) as ExportResult | ExportFailure;
  if (!response.ok && response.status !== 503) {
    throw new Error("Current-revision approval is required for export.");
  }
  return result;
}