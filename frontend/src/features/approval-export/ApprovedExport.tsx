import { Copy, Download } from "lucide-react";

import type { LabeledExportView } from "../../shared/model/labeledExport";
import { StatusBadge } from "../../shared/ui/StatusBadge";
import { ExportFailureModal } from "./ExportFailureModal";
import { LabeledExportPreview } from "./LabeledExportPreview";

interface ApprovedExportProps {
  revisionLabel: string;
  view: LabeledExportView;
  pending: boolean;
  failureOpen: boolean;
  onCopy: () => void;
  onDownload: () => void;
  onCloseFailure: () => void;
}

export function ApprovedExport({ revisionLabel, view, pending, failureOpen, onCopy, onDownload, onCloseFailure }: ApprovedExportProps) {
  const disabled = view.empty || pending;
  return (
    <main className="export-main" id="main-content" data-uxr="UXR-002">
      <p className="breadcrumb">Approval and export / Approved revision</p>
      <div className="review-title"><div><h1>Approved POC draft</h1><p>Copy or download the current revision for local compliance handling.</p></div><StatusBadge status="approved" label="Revision approved" /></div>
      <section className="approval-detail" aria-label="Approval details">
        <div><span>Approval</span><strong>Current revision</strong></div>
        <div><span>Delivery</span><strong>Local copy or download only</strong></div>
        <div><span>External submission</span><strong>Not performed</strong></div>
      </section>
      <LabeledExportPreview view={view} />
      <div className="approval-actions">
        <button className="button button--secondary" type="button" onClick={onCopy} disabled={disabled}><Copy aria-hidden="true" /> Copy draft</button>
        <button className="button" type="button" onClick={onDownload} disabled={disabled}><Download aria-hidden="true" /> {pending ? "Preparing..." : "Download .txt"}</button>
      </div>
      <ExportFailureModal open={failureOpen} onClose={onCloseFailure} onRetry={onDownload} onCopy={onCopy} />
    </main>
  );
}