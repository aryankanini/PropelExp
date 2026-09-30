import type { ReviewCandidate } from "./types";
import { ProvenanceLabel } from "./ProvenanceLabel";

interface CandidateComparisonProps {
  candidates: readonly ReviewCandidate[];
  selectedCandidateId: string | null;
  correction: string;
  onSelectCandidate: (candidateId: string | null) => void;
  onCorrectionChange: (value: string) => void;
}

export function CandidateComparison({
  candidates,
  selectedCandidateId,
  correction,
  onSelectCandidate,
  onCorrectionChange,
}: CandidateComparisonProps) {
  return (
    <div className="candidate-comparison" data-uxr="UXR-102 UXR-502">
      <fieldset>
        <legend>Extracted candidates</legend>
        {candidates.map((candidate) => (
          <label key={candidate.candidateId} className="comparison-option">
            <input
              type="radio"
              name="supported-candidate"
              value={candidate.candidateId}
              checked={selectedCandidateId === candidate.candidateId}
              onChange={() => {
                onCorrectionChange("");
                onSelectCandidate(candidate.candidateId);
              }}
            />
            <span className="comparison-option__content">
              <strong>{candidate.value}</strong>
              <span>{candidate.evidence.fullSnippet}</span>
              <small>Page {candidate.evidence.pageNumber} · {Math.round(candidate.confidence * 100)}% confidence</small>
              <ProvenanceLabel origin={candidate.origin} revisionNumber={1} />
            </span>
          </label>
        ))}
      </fieldset>
      <div className="comparison-correction">
        <label htmlFor="candidate-correction">Or enter a correction</label>
        <textarea
          id="candidate-correction"
          value={correction}
          onChange={(event) => {
            onSelectCandidate(null);
            onCorrectionChange(event.target.value);
          }}
          aria-describedby="candidate-correction-help"
        />
        <p id="candidate-correction-help">The correction will be labeled User-edited. Original candidates remain visible.</p>
      </div>
    </div>
  );
}