import { useCallback, useEffect, useRef, useState } from "react";
import { apiUrl } from "../api/client";

export type JobStage = "extraction" | "ocr" | "generation";
export type TerminalStatus = "completed" | "failed";

export interface JobEvent {
  job_id: string;
  event_id: number;
  stage: JobStage;
  percent: number;
  timestamp: string;
  terminal_status: TerminalStatus | null;
  failure_code: string | null;
}

export type ExtractionJobState =
  | { status: "idle" }
  | { status: "running"; percent: number; stage: JobStage }
  | { status: "completed" }
  | { status: "failed"; stage: JobStage; code: string | null };

const MAX_ESTIMATED_PERCENT = 98;

export function advanceEstimatedProgress(percent: number): number {
  return Math.min(percent + 1, MAX_ESTIMATED_PERCENT);
}

export function useExtractionJob(jobId: string | null) {
  const [state, setState] = useState<ExtractionJobState>({ status: "idle" });
  const lastEventIdRef = useRef(0);
  const esRef = useRef<EventSource | null>(null);

  const connect = useCallback(() => {
    if (!jobId) return;
    esRef.current?.close();

    const url = apiUrl(
      `/api/v1/jobs/${encodeURIComponent(jobId)}/events?last_event_id=${lastEventIdRef.current}`,
    );
    const es = new EventSource(url);
    esRef.current = es;

    es.onmessage = (event: MessageEvent<string>) => {
      let data: JobEvent;
      try {
        const parsed = JSON.parse(event.data);
        if (
          typeof parsed !== "object" ||
          parsed === null ||
          typeof parsed.event_id !== "number" ||
          typeof parsed.percent !== "number" ||
          typeof parsed.stage !== "string"
        ) {
          return;
        }
        data = parsed as JobEvent;
      } catch {
        return;
      }
      lastEventIdRef.current = data.event_id;

      if (data.terminal_status === "completed") {
        setState({ status: "completed" });
        es.close();
      } else if (data.terminal_status === "failed") {
        setState({ status: "failed", stage: data.stage, code: data.failure_code });
        es.close();
      } else {
        setState((current) => ({
          status: "running",
          percent:
            current.status === "running" && current.stage === data.stage
              ? Math.max(current.percent, data.percent)
              : data.percent,
          stage: data.stage,
        }));
      }
    };

    es.onerror = () => {
      es.close();
      setState((current) => {
        if (current.status === "completed" || current.status === "failed") return current;
        setTimeout(connect, 2000);
        return current;
      });
    };
  }, [jobId]);

  useEffect(() => {
    if (!jobId) return;
    setState({ status: "running", percent: 0, stage: "extraction" });
    connect();
    return () => esRef.current?.close();
  }, [jobId, connect]);

  useEffect(() => {
    if (state.status !== "running" || state.stage !== "generation") return;

    const timer = window.setInterval(() => {
      setState((current) =>
        current.status === "running" && current.stage === "generation"
          ? {
              ...current,
              percent: advanceEstimatedProgress(current.percent),
            }
          : current,
      );
    }, 1500);

    return () => window.clearInterval(timer);
  }, [state.status, state.status === "running" ? state.stage : null]);

  return state;
}
