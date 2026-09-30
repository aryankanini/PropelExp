import type { AcceptedUpload } from "./useDocumentUpload";

interface DocumentValidationStatusProps {
  accepted?: AcceptedUpload;
  rejection?: string;
  extractionStarted?: boolean;
}

export function DocumentValidationStatus({
  accepted,
  rejection,
  extractionStarted = false,
}: DocumentValidationStatusProps) {
  if (accepted) {
    return (
      <section className="intake-status intake-status--ready" role="status">
        <strong>Document is extraction-ready.</strong>
        <span>
          {accepted.page_count} pages validated. {extractionStarted
            ? "Extraction is in progress."
            : "Extraction has not started."}
        </span>
      </section>
    );
  }
  if (rejection) {
    return (
      <section className="intake-status intake-status--error" role="alert">
        <strong>Document was not accepted.</strong>
        <span>{rejection} No extraction results were created.</span>
      </section>
    );
  }
  return null;
}