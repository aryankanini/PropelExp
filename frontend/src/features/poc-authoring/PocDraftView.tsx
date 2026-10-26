import type { PocDraft, PocSectionName } from "../../shared/api/poc";
import { PocEditor } from "./PocEditor";
import { PocDocumentEditor } from "./PocDocumentEditor";

interface PocDraftViewProps {
  draft: PocDraft;
  onSave: (
    deficiencyId: string,
    expectedRevisionId: string,
    updates: Partial<Record<PocSectionName, string | null>>,
  ) => Promise<PocDraft>;
  onReload: () => Promise<void>;
}

export function PocDraftView({ draft, onSave, onReload }: PocDraftViewProps) {
  const current = draft.revisions.at(-1);
  const isCombinedDocument = Boolean(current?.document_entries?.length);
  return (
    <section className="poc-draft" aria-labelledby="poc-draft-title">
      <div className="poc-title-row">
        <div>
          <p className="poc-breadcrumb">POC drafts / Selected deficiency</p>
          <h1 id="poc-draft-title">Plan of correction</h1>
          <p>
            {isCombinedDocument
              ? `${current?.document_entries?.length ?? 0} SOD and POC records in one document`
              : `Five-part unapproved draft for deficiency ${draft.deficiency_id}`}
          </p>
        </div>
        <span className="poc-revision">Unapproved · Revision {draft.revisions.length}</span>
      </div>
      {isCombinedDocument ? (
        <PocDocumentEditor draft={draft} onSave={onSave} />
      ) : (
        <PocEditor
          draft={draft}
          onSave={(expectedRevisionId, updates) =>
            onSave(draft.deficiency_id, expectedRevisionId, updates)}
          onReload={onReload}
        />
      )}
    </section>
  );
}