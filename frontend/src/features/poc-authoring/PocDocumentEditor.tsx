import { useEffect, useState } from "react";

import {
  pocSectionOrder,
  type PocContent,
  type PocDocumentEntry,
  type PocDraft,
  type PocSectionName,
} from "../../shared/api/poc";
import { pocSectionLabels } from "./pocSections";

interface PocDocumentEditorProps {
  draft: PocDraft;
  onSave: (
    deficiencyId: string,
    expectedRevisionId: string,
    updates: Partial<Record<PocSectionName, string | null>>,
  ) => Promise<PocDraft>;
}

export function PocDocumentEditor({ draft, onSave }: PocDocumentEditorProps) {
  const revision = draft.revisions.at(-1);
  if (!revision) throw new Error("A POC document requires a current revision.");

  return (
    <div className="poc-editor">
      {(revision.document_entries ?? []).map((entry) => (
        <DocumentEntryEditor
          key={`${entry.deficiency_id}-${draft.current_revision_id}`}
          draft={draft}
          entry={entry}
          onSave={onSave}
        />
      ))}
    </div>
  );
}

function DocumentEntryEditor({
  draft,
  entry,
  onSave,
}: {
  draft: PocDraft;
  entry: PocDocumentEntry;
  onSave: PocDocumentEditorProps["onSave"];
}) {
  const [values, setValues] = useState<PocContent>(entry.content);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => setValues(entry.content), [entry]);

  const updates = Object.fromEntries(
    pocSectionOrder
      .filter((section) => values[section].trim() !== entry.content[section])
      .map((section) => [section, values[section].trim()]),
  ) as Partial<Record<PocSectionName, string>>;
  const invalid = pocSectionOrder.some((section) => !values[section].trim());
  const changed = Object.keys(updates).length > 0;

  return (
    <section className="poc-document-entry" aria-labelledby={`poc-${entry.deficiency_id}`}>
      <h2 id={`poc-${entry.deficiency_id}`}>{entry.label}</h2>
      <div className="poc-source-sod">
        <h3>Statement of Deficiency</h3>
        <p>{entry.sod_text}</p>
      </div>
      <h3>Plan of Correction</h3>
      {pocSectionOrder.map((section) => (
        <div className="poc-field" key={section}>
          <label htmlFor={`${entry.deficiency_id}-${section}`}>
            {pocSectionLabels[section]}
          </label>
          <textarea
            id={`${entry.deficiency_id}-${section}`}
            value={values[section]}
            disabled={saving}
            onChange={(event) =>
              setValues((current) => ({ ...current, [section]: event.target.value }))
            }
          />
        </div>
      ))}
      {error && <p className="poc-inline-error" role="alert">{error}</p>}
      <button
        className="button"
        type="button"
        disabled={!changed || invalid || saving}
        onClick={() => {
          setSaving(true);
          setError("");
          void onSave(entry.deficiency_id, draft.current_revision_id, updates)
            .catch((reason: unknown) => {
              setError(reason instanceof Error ? reason.message : "The POC could not be saved.");
            })
            .finally(() => setSaving(false));
        }}
      >
        {saving ? "Saving..." : `Save ${entry.label} POC`}
      </button>
    </section>
  );
}
