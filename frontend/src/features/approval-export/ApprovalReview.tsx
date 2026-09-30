import { Check, FileWarning, SendToBack } from "lucide-react";

import type { ApprovalBlocker, ApprovalReviewModel } from "../../shared/model/approval";
import { StatusBadge } from "../../shared/ui/StatusBadge";
import { RevisionHistory } from "./RevisionHistory";

interface ApprovalReviewProps {
  review: ApprovalReviewModel;
  blockers: ApprovalBlocker[];
  pending: boolean;
  onApprove: () => void;
  onRequestChanges: () => void;
}

export function ApprovalReview({ review, blockers, pending, onApprove, onRequestChanges }: ApprovalReviewProps) {
  const complete = review.sections.length === 5 && review.sections.every((section) => section.content.trim());
  const canApprove = review.role === "compliance_leader" && complete && !pending;

  return (
    <div className="approval-layout" data-uxr="UXR-002">
      <main className="approval-main" id="main-content">
        <p className="breadcrumb">Approval and export / {review.deficiencyTag}</p>
        <div className="review-title">
          <div><h1>Review current POC revision</h1><p>Compare evidence, provenance, completeness, and all five required sections.</p></div>
          <StatusBadge status="awaiting" label={`${review.revisionLabel} · Current`} />
        </div>
        {blockers.length ? (
          <section className="blocker-summary" role="alert" tabIndex={-1}>
            <h2><FileWarning aria-hidden="true" /> Approval blocked</h2>
            <ul>{blockers.map((blocker) => <li key={`${blocker.code}-${blocker.section}`}>{blocker.message}</li>)}</ul>
          </section>
        ) : null}
        <section className="evidence-strip" aria-label="Deficiency evidence and completeness">
          <div><span>Deficiency</span><strong>{review.deficiencyTag}</strong></div>
          <div><span>Evidence</span><strong>{review.evidence.length} reviewed sources</strong></div>
          <div><span>Completeness</span><strong>{review.sections.length} of 5 sections</strong></div>
          <StatusBadge status={complete ? "approved" : "blocked"} label={complete ? "Complete" : "Incomplete"} />
        </section>
        <section className="section-review" aria-labelledby="section-review-title">
          <h2 id="section-review-title">Plan of correction</h2>
          {review.sections.map((section, index) => (
            <article key={section.id} className="review-section">
              <div className="section-number">{index + 1}</div>
              <div><h3>{section.title}</h3><p>{section.content}</p><small>Provenance: {section.provenance}</small></div>
            </article>
          ))}
        </section>
        <div className="approval-actions">
          <button className="button button--secondary" type="button" onClick={onRequestChanges} disabled={pending}><SendToBack aria-hidden="true" /> Request changes</button>
          <button className="button" type="button" onClick={onApprove} disabled={!canApprove}><Check aria-hidden="true" /> {pending ? "Approving..." : "Approve current revision"}</button>
        </div>
        {review.role !== "compliance_leader" ? <p className="disabled-reason">Only a compliance leader can approve this revision.</p> : null}
      </main>
      <RevisionHistory entries={review.history} />
    </div>
  );
}