import { useState } from "react";

import { DeficiencyStatus } from "./DeficiencyStatus";

export interface ConfirmationBlocker {
  fieldId: string;
  label: string;
  reason: string;
}

export type ConfirmationResult =
  | { status: "confirmed" }
  | { status: "stale"; currentRevisionId: string };

interface ConfirmationPanelProps {
  deficiencyId: string;
  expectedRevisionId: string;
  blockers: readonly ConfirmationBlocker[];
  onConfirm: (expectedRevisionId: string) => Promise<ConfirmationResult>;
  onReload: () => void;
}

export function ConfirmationPanel({
  deficiencyId,
  expectedRevisionId,
  blockers,
  onConfirm,
  onReload,
}: ConfirmationPanelProps) {
  const [confirmed, setConfirmed] = useState(false);
  const [staleRevisionId, setStaleRevisionId] = useState<string | null>(null);
  const [pending, setPending] = useState(false);
  const blocked = blockers.length > 0 || staleRevisionId !== null;

  async function confirm() {
    setPending(true);
    const result = await onConfirm(expectedRevisionId);
    setPending(false);
    if (result.status === "stale") {
      setStaleRevisionId(result.currentRevisionId);
      setConfirmed(false);
      return;
    }
    setConfirmed(true);
  }

  return (
    <section className="confirmation-panel" aria-labelledby="confirmation-title" data-uxr="UXR-502">
      <header>
        <div>
          <p>Deficiency {deficiencyId}</p>
          <h2 id="confirmation-title">Confirmation readiness</h2>
        </div>
        <DeficiencyStatus state={confirmed ? "confirmed" : blocked ? "blocked" : "ready"} />
      </header>
      {blockers.length > 0 ? (
        <div className="confirmation-blockers" role="alert">
          <strong>Resolve every blocking field</strong>
          <ul>{blockers.map((blocker) => <li key={blocker.fieldId}><a href={`#${blocker.fieldId}`}>{blocker.label}</a>: {blocker.reason}</li>)}</ul>
        </div>
      ) : null}
      {staleRevisionId ? (
        <div className="confirmation-blockers" role="alert">
          <strong>Reload required</strong>
          <p>Revision {staleRevisionId} is current. Confirmation remains denied.</p>
          <button className="button button--secondary" type="button" onClick={onReload}>Reload current values</button>
        </div>
      ) : null}
      <div className="confirmation-actions">
        <button className="button" type="button" disabled={blocked || pending || confirmed} onClick={confirm}>{pending ? "Confirming..." : "Confirm deficiency"}</button>
        <button className="button button--secondary" type="button" disabled={!confirmed}>Generate POC</button>
      </div>
    </section>
  );
}