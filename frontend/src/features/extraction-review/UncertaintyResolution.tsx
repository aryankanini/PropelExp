import { useState } from "react";

import { CandidateComparison } from "./CandidateComparison";
import type { ReviewField } from "./types";

export type ResolutionRequest =
  | { kind: "select"; expectedRevisionId: string; candidateId: string }
  | { kind: "correct"; expectedRevisionId: string; value: string }
  | { kind: "unresolved"; expectedRevisionId: string };

export type ResolutionResult =
  | { status: "resolved" }
  | { status: "stale"; currentRevisionId: string };

interface UncertaintyResolutionProps {
  field: ReviewField;
  onResolve: (request: ResolutionRequest) => Promise<ResolutionResult>;
}

export function UncertaintyResolution({ field, onResolve }: UncertaintyResolutionProps) {
  const [selectedCandidateId, setSelectedCandidateId] = useState<string | null>(null);
  const [correction, setCorrection] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function submitResolution() {
    let request: ResolutionRequest;
    if (selectedCandidateId) {
      request = { kind: "select", expectedRevisionId: field.currentRevisionId, candidateId: selectedCandidateId };
    } else if (correction.trim()) {
      request = { kind: "correct", expectedRevisionId: field.currentRevisionId, value: correction.trim() };
    } else {
      setMessage("Select a supported candidate or enter a correction.");
      return;
    }
    setPending(true);
    const result = await onResolve(request);
    setPending(false);
    setMessage(result.status === "stale"
      ? `This field changed to ${result.currentRevisionId}. Reload current values; your input is retained.`
      : "The uncertainty block was removed.");
  }

  async function leaveUnresolved() {
    setPending(true);
    await onResolve({ kind: "unresolved", expectedRevisionId: field.currentRevisionId });
    setPending(false);
    setMessage("Value remains unresolved. Confirmation and POC drafting are blocked.");
  }

  return (
    <section className="uncertainty-resolution" aria-labelledby="uncertainty-title" data-uxr="UXR-102 UXR-502">
      <header>
        <p>Uncertain value</p>
        <h2 id="uncertainty-title">Resolve {field.label}</h2>
      </header>
      <CandidateComparison
        candidates={field.candidates}
        selectedCandidateId={selectedCandidateId}
        correction={correction}
        onSelectCandidate={setSelectedCandidateId}
        onCorrectionChange={setCorrection}
      />
      {message ? <p className="resolution-message" role="status">{message}</p> : null}
      <div className="resolution-actions">
        <button className="button button--secondary" type="button" disabled={pending} onClick={leaveUnresolved}>Leave unresolved</button>
        <button className="button" type="button" disabled={pending} onClick={submitResolution}>{pending ? "Saving..." : "Resolve value"}</button>
      </div>
    </section>
  );
}