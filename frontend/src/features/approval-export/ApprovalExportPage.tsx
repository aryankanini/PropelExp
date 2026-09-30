import { useEffect, useState } from "react";

import { approveRevision } from "../../shared/api/approval";
import { exportApprovedRevision } from "../../shared/api/export";
import { requestChanges } from "../../shared/api/reapproval";
import { useSession } from "../../app/SessionContext";
import { createPocApi, pocSectionOrder, type PocDraft } from "../../shared/api/poc";
import { EndSessionAction } from "../../shared/session/EndSessionAction";
import { useSessionStatus } from "../../shared/session/useSessionStatus";
import type { ApprovalBlocker, ApprovalReviewModel } from "../../shared/model/approval";
import type { ExportFailure, ExportResult } from "../../shared/model/export";
import { DRAFT_EXPORT_PREFIX } from "../../shared/model/labeledExport";
import { ApprovalReview } from "./ApprovalReview";
import { ApprovedExport } from "./ApprovedExport";
import "./approval-export.css";

export function ApprovalExportPage() {
  const { sessionId, caseId, deficiencyId, setCaseId } = useSession();
  const sessionStatus = useSessionStatus(sessionId);
  const resolvedCaseId = sessionStatus?.active_case_id ?? "";
  const resolvingCase = sessionStatus === null;

  const [approved, setApproved] = useState(false);
  const [pending, setPending] = useState(false);
  const [revisionId, setRevisionId] = useState("revision-1");
  const [draft, setDraft] = useState<PocDraft | null>(null);
  const [blockers, setBlockers] = useState<ApprovalBlocker[]>([]);
  const [failureOpen, setFailureOpen] = useState(false);
  const [exportContent, setExportContent] = useState("");

  useEffect(() => {
    if (sessionStatus?.active_case_id && sessionStatus.active_case_id !== caseId) {
      setCaseId(sessionStatus.active_case_id);
    }
  }, [caseId, sessionStatus, setCaseId]);

  useEffect(() => {
    if (!deficiencyId) return;
    createPocApi(sessionId)
      .load(deficiencyId)
      .then((current) => {
        setDraft(current);
        setRevisionId(current.current_revision_id);
      })
      .catch(() => {
        setBlockers([
          {
            code: "draft_unavailable",
            message: "The current POC draft could not be loaded.",
            section: null,
          },
        ]);
      });
  }, [deficiencyId, sessionId]);

  const currentDraftRevision = draft?.revisions.find(
    (item) => item.revision_id === draft.current_revision_id,
  );

  const review: ApprovalReviewModel = {
    caseId: resolvedCaseId || "Active case",
    deficiencyTag: deficiencyId ?? "F-tag",
    facilityName: "Active case",
    revisionId,
    revisionLabel: `Revision ${revisionId}`,
    role: "compliance_leader",
    evidence: currentDraftRevision?.grounded_claims.flatMap((claim) =>
      claim.support_references.map((reference) => reference.reference_id),
    ) ?? [],
    sections: currentDraftRevision
      ? pocSectionOrder.map((name) => ({
          id: name,
          title: name.replaceAll("_", " ").replace(/^./, (value) => value.toUpperCase()),
          content: currentDraftRevision.content[name],
          provenance: currentDraftRevision.section_origins[name].replaceAll("_", " "),
        }))
      : [],
    history: [],
  };

  async function approve() {
    if (!resolvedCaseId) {
      setBlockers([
        {
          code: "case_unavailable",
          message: "The active case could not be resolved. Return to intake and reopen the case.",
          section: null,
        },
      ]);
      return;
    }
    setPending(true);
    setBlockers([]);
    try {
      const result = await approveRevision({
        caseId: resolvedCaseId,
        sessionId,
        actorId: "leader-1",
        actorRole: "compliance_leader",
        revisionId,
      });
      setBlockers(result.blockers);
      const approvalRecorded = result.approved
        && result.copy_enabled
        && result.download_enabled;
      setApproved(approvalRecorded);
      if (approvalRecorded) {
        try {
          const exported = await exportApprovedRevision(
            resolvedCaseId,
            sessionId,
            "copy",
          );
          if (isExportFailure(exported)) {
            setFailureOpen(true);
          } else {
            setExportContent(exported.content);
            setFailureOpen(false);
          }
        } catch {
          setFailureOpen(true);
        }
      }
    } catch (error) {
      setBlockers([
        {
          code: "approval_failed",
          message: error instanceof Error
            ? `${error.message} The displayed revision is unchanged.`
            : "Approval could not be recorded. The displayed revision is unchanged.",
          section: null,
        },
      ]);
    } finally {
      setPending(false);
    }
  }

  async function returnToEditing() {
    setPending(true);
    try {
      await requestChanges(resolvedCaseId, sessionId);
      setApproved(false);
      setBlockers([
        {
          code: "changes_requested",
          message: "Revision returned to editing. Export remains disabled.",
          section: null,
        },
      ]);
    } catch {
      setBlockers([
        {
          code: "request_changes_failed",
          message: "The request was not saved. The displayed revision is unchanged.",
          section: null,
        },
      ]);
    } finally {
      setPending(false);
    }
  }

  async function copyDraft() {
    try {
      const result = await exportApprovedRevision(resolvedCaseId, sessionId, "copy");
      if (isExportFailure(result)) {
        setFailureOpen(true);
        return;
      }
      setExportContent(result.content);
      await navigator.clipboard?.writeText(result.content);
      setFailureOpen(false);
    } catch {
      setApproved(false);
      setBlockers([
        {
          code: "approval_required",
          message: "Current-revision approval is required before export.",
          section: null,
        },
      ]);
    }
  }

  async function downloadDraft() {
    setPending(true);
    try {
      const result = await exportApprovedRevision(resolvedCaseId, sessionId, "download");
      if (isExportFailure(result)) {
        setFailureOpen(true);
        return;
      }
      setExportContent(result.content);
      downloadText(result);
      setFailureOpen(false);
    } catch {
      setApproved(false);
      setBlockers([
        {
          code: "approval_required",
          message: "Current-revision approval is required before export.",
          section: null,
        },
      ]);
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="approval-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <header className="approval-header">
        <strong>CMS Deficiency Action Planner</strong>
        <span>Compliance leader · {resolvedCaseId}</span>
      </header>
      <div className="approval-body">
        <nav className="approval-rail" aria-label="Case workflow">
          <strong>Active case</strong>
          <small>{deficiencyId ?? "F-tag"} · {revisionId}</small>
          <ol>
            <li>
              <span>1</span>
              <div>
                Intake<small>Complete</small>
              </div>
            </li>
            <li>
              <span>2</span>
              <div>
                Review<small>Confirmed</small>
              </div>
            </li>
            <li>
              <span>3</span>
              <div>
                POC drafts<small>Complete</small>
              </div>
            </li>
            <li aria-current="step">
              <span>4</span>
              <div>
                Approval and export<small>{approved ? "Approved" : "Ready"}</small>
              </div>
            </li>
          </ol>
          <EndSessionAction className="button button--secondary approval-end-session" />
        </nav>
        {approved ? (
          <ApprovedExport
            revisionLabel={revisionId}
            view={{ label: DRAFT_EXPORT_PREFIX, content: exportContent, empty: !exportContent.trim() }}
            pending={pending}
            failureOpen={failureOpen}
            onCopy={() => void copyDraft()}
            onDownload={() => void downloadDraft()}
            onCloseFailure={() => setFailureOpen(false)}
          />
        ) : (
          <ApprovalReview
            review={review}
            blockers={blockers}
            pending={pending || resolvingCase}
            onApprove={() => void approve()}
            onRequestChanges={() => void returnToEditing()}
          />
        )}
      </div>
    </div>
  );
}

function isExportFailure(result: ExportResult | ExportFailure): result is ExportFailure {
  return "code" in result && result.code === "formatting_failed";
}

function downloadText(result: ExportResult) {
  const url = URL.createObjectURL(new Blob([result.content], { type: result.media_type }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = result.filename ?? "approved-poc-draft.txt";
  anchor.click();
  URL.revokeObjectURL(url);
}
