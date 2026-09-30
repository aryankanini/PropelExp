import { useState } from "react";
import { apiUrl } from "../api/client";

export function useEndSession(sessionId: string, caseId: string | null) {
  const [status, setStatus] = useState<"idle" | "ending" | "failed">("idle");

  async function endSession(): Promise<boolean> {
    if (!caseId) return true;
    setStatus("ending");
    try {
      const response = await fetch(apiUrl(`/api/v1/cases/${caseId}`), {
        method: "DELETE",
        headers: { "X-Session-ID": sessionId },
      });
      if (response.ok) {
        setStatus("idle");
        return true;
      }
    } catch {
      // The failed state keeps the active case visible for an idempotent retry.
    }
    setStatus("failed");
    return false;
  }

  return { status, endSession };
}