import type { LabeledExportView } from "../../shared/model/labeledExport";
import { Alert } from "../../shared/ui/Alert";

export function LabeledExportPreview({ view }: { view: LabeledExportView }) {
  if (view.empty) {
    return <Alert title="Approved content is empty" assertive>Copy and download remain unavailable until the approved revision contains content.</Alert>;
  }
  return (
    <section className="export-preview" aria-labelledby="export-preview-title">
      <h2 id="export-preview-title">Export preview</h2>
      <p className="draft-label">{view.label}</p>
      <div className="export-content">{view.content}</div>
    </section>
  );
}