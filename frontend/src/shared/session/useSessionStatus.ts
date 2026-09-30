import { useEffect, useState } from "react";
import { apiUrl } from "../api/client";

export interface SessionStatus {
  storage: "session_only";
  remaining_inactivity_seconds: number;
  active_case_id: string | null;
}

export function useSessionStatus(sessionId: string, enabled = true) {
  const [status, setStatus] = useState<SessionStatus | null>(null);

  useEffect(() => {
    if (!enabled) {
      setStatus(null);
      return;
    }
    const controller = new AbortController();
    const refresh = async () => {
      try {
        const response = await fetch(apiUrl("/api/v1/session/status"), {
          headers: { "X-Session-ID": sessionId },
          signal: controller.signal,
        });
        if (response.ok) {
          setStatus((await response.json()) as SessionStatus);
        }
      } catch (error) {
        if (!(error instanceof DOMException && error.name === "AbortError")) {
          setStatus(null);
        }
      }
    };
    void refresh();
    const reconnect = () => void refresh();
    window.addEventListener("online", reconnect);
    return () => {
      controller.abort();
      window.removeEventListener("online", reconnect);
    };
  }, [enabled, sessionId]);

  return status;
}