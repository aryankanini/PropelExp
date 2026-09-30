import { History } from "lucide-react";

import { ProvenanceLabel } from "./ProvenanceLabel";
import type { RevisionEntry } from "./types";

interface RevisionHistoryProps {
  revisions: readonly RevisionEntry[];
}

export function RevisionHistory({ revisions }: RevisionHistoryProps) {
  return (
    <section className="review-revisions" aria-labelledby="review-revisions-title" data-uxr="UXR-103">
      <h2 id="review-revisions-title"><History aria-hidden="true" size={18} /> Revision history</h2>
      <ol>
        {[...revisions].reverse().map((revision) => (
          <li key={revision.revisionId}>
            <div className="review-revisions__meta">
              <ProvenanceLabel origin={revision.origin} revisionNumber={revision.revisionNumber} />
              {revision.current ? <strong>Current</strong> : null}
            </div>
            <p>{revision.value}</p>
            {revision.evidence ? <small>Evidence retained from page {revision.evidence.pageNumber}</small> : null}
          </li>
        ))}
      </ol>
    </section>
  );
}