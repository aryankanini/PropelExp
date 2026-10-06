import { useState } from "react";

import { EndSessionAction } from "../../shared/session/EndSessionAction";
import { FailedStageAlert } from "./FailedStageAlert";
import { StageTimeline, type TimelineStage } from "./StageTimeline";
import "./document-intake.css";

const stages: readonly TimelineStage[] = [
  { id: "upload", label: "Upload validation", detail: "42.8 MB PDF accepted, 96 pages", status: "complete" },
  { id: "text", label: "Native text extraction", detail: "Text recovered from 78 pages", status: "complete" },
  { id: "ocr", label: "OCR fallback", detail: "Failed on pages 29-31", status: "failed" },
  { id: "review", label: "Review package", detail: "Waiting for the failed OCR operation", status: "pending" },
];

export function ProcessingFailurePage() {
  const [recoveryQueued, setRecoveryQueued] = useState(false);

  return (
    <div className="workspace-shell">
      <a className="skip-link" href="#processing-progress">Skip to main content</a>
      <header className="app-header">
        <strong>CMS Deficiency Action Planner</strong>
      </header>
      <nav className="workflow-rail" aria-label="Case workflow">
        <div className="session-label">
          <strong>Northlake Skilled Nursing Center</strong>
          <span>96 pages, active case</span>
        </div>
        <ol>
          <li aria-current="step"><span>1</span><div>Intake<small>Processing failed</small></div></li>
          <li><span>2</span><div>Review<small>Waiting</small></div></li>
          <li><span>3</span><div>POC drafts<small>Unavailable</small></div></li>
          <li><span>4</span><div>Approval and export<small>Unavailable</small></div></li>
        </ol>
        <EndSessionAction />
      </nav>
      <main className="intake-content processing-content" id="processing-progress">
        <h1>Processing survey document</h1>
        <p className="lede">Required OCR work remains incomplete. Confirmed results are retained.</p>
        <FailedStageAlert
          stage="OCR"
          pageNumbers={[29, 30, 31]}
          retainedWork="Validated pages and provider fields remain available"
          correlationId="OCR-4F82"
          retryable
          onRecovery={() => setRecoveryQueued(true)}
        />
        {recoveryQueued ? (
          <p className="recovery-feedback" role="status">
            OCR recovery was queued. Retained work remains unchanged.
          </p>
        ) : null}
        <StageTimeline stages={stages} />
      </main>
    </div>
  );
}