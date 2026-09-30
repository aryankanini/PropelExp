import { Search } from "lucide-react";
import { useDeferredValue, useState } from "react";

import type { AsyncState, ReviewCandidate } from "./types";

interface EvidenceViewerProps {
  candidate: ReviewCandidate | null;
  state?: AsyncState;
  errorMessage?: string;
}

export function EvidenceViewer({
  candidate,
  state = "ready",
  errorMessage = "Supporting evidence could not be loaded.",
}: EvidenceViewerProps) {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query.trim().toLocaleLowerCase());

  if (state === "loading") {
    return <aside className="evidence-viewer evidence-viewer--state" role="status">Loading selected evidence.</aside>;
  }
  if (state === "error") {
    return <aside className="evidence-viewer evidence-viewer--state evidence-viewer--error" role="alert">{errorMessage} The selected value has not changed.</aside>;
  }
  if (state === "empty" || candidate === null) {
    return <aside className="evidence-viewer evidence-viewer--state">No evidence-linked candidates are available.</aside>;
  }

  const snippet = candidate.evidence.fullSnippet;
  const matches = deferredQuery.length > 0
    ? snippet.toLocaleLowerCase().split(deferredQuery).length - 1
    : 0;

  return (
    <aside className="evidence-viewer" aria-labelledby="evidence-viewer-title" data-uxr="UXR-102 UXR-502">
      <header className="evidence-viewer__header">
        <div>
          <h2 id="evidence-viewer-title">Source evidence</h2>
          <p>Page {candidate.evidence.pageNumber} · {candidate.evidence.source === "ocr" ? "OCR" : "Native text"}</p>
        </div>
        <strong>{Math.round(candidate.confidence * 100)}% confidence</strong>
      </header>
      <label className="evidence-search">
        <span>Search full evidence</span>
        <span className="evidence-search__control">
          <Search aria-hidden="true" size={16} />
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </span>
      </label>
      <p className="evidence-search__status" role="status">
        {deferredQuery ? `${matches} matches in complete snippet` : "Complete snippet shown"}
      </p>
      <div className="evidence-page">
        <p><mark>{snippet}</mark></p>
      </div>
    </aside>
  );
}