import { useState } from "react";

import { ProvenanceLabel } from "./ProvenanceLabel";
import type { ReviewField } from "./types";

interface FieldEditorProps {
  field: ReviewField;
  selectedCandidateId: string;
  onSelectCandidate: (candidateId: string) => void;
  onSaveCorrection: (value: string) => Promise<void> | void;
}

export function FieldEditor({
  field,
  selectedCandidateId,
  onSelectCandidate,
  onSaveCorrection,
}: FieldEditorProps) {
  const current = field.revisions.find((r) => r.current);
  const [correction, setCorrection] = useState(current?.value ?? "");
  const [error, setError] = useState<string | null>(null);

  async function saveCorrection() {
    if (!correction.trim()) {
      setError("Enter a correction before saving.");
      return;
    }
    setError(null);
    await onSaveCorrection(correction.trim());
  }

  return (
    <section className="field-editor" aria-labelledby={`${field.fieldId}-title`}>
      <header className="field-editor__header">
        <div>
          <span className="field-editor__type">Statement of Deficiency</span>
          <h2 id={`${field.fieldId}-title`} className="field-editor__tag">
            {field.label}
          </h2>
        </div>
        {current && (
          <ProvenanceLabel
            origin={current.origin}
            revisionNumber={current.revisionNumber}
            reapprovalRequired={field.reapprovalRequired}
          />
        )}
      </header>

      {field.candidates.length > 1 && (
        <div className="candidate-list" role="listbox" aria-label="Extracted candidates">
          {field.candidates.map((candidate) => {
            const selected = candidate.candidateId === selectedCandidateId;
            return (
              <button
                key={candidate.candidateId}
                className="candidate-option"
                type="button"
                role="option"
                aria-selected={selected}
                onClick={() => onSelectCandidate(candidate.candidateId)}
              >
                <div className="candidate-option__meta">
                  <span>Page {candidate.evidence.pageNumber}</span>
                  <span>{Math.round(candidate.confidence * 100)}% confidence</span>
                  {candidate.uncertainty && (
                    <span className="candidate-option__uncertainty">
                      {candidate.uncertainty}
                    </span>
                  )}
                  <ProvenanceLabel origin={candidate.origin} revisionNumber={1} />
                </div>
              </button>
            );
          })}
        </div>
      )}

      <div className="sod-text-block">
        <p className="sod-text-block__label">Extracted SOD text</p>
        <pre className="sod-text-block__content">{current?.value ?? ""}</pre>
      </div>

      {field.pocSuggestion && (
        <div className="poc-suggestion-block">
          <p className="poc-suggestion-block__label">
            AI-suggested Plan of Correction
          </p>
          <p className="poc-suggestion-block__content">{field.pocSuggestion}</p>
        </div>
      )}

      <div className="correction-editor">
        <label htmlFor={`${field.fieldId}-correction`}>
          Edit / correct SOD text
        </label>
        <textarea
          id={`${field.fieldId}-correction`}
          value={correction}
          aria-describedby={error ? `${field.fieldId}-error` : undefined}
          aria-invalid={error !== null}
          onChange={(e) => setCorrection(e.target.value)}
        />
        {error && (
          <p id={`${field.fieldId}-error`} className="field-error" role="alert">
            {error}
          </p>
        )}
        <button className="button" type="button" onClick={saveCorrection}>
          Save correction
        </button>
      </div>
    </section>
  );
}
