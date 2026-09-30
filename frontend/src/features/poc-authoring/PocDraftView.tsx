import type { PocDraft, PocSectionName } from "../../shared/api/poc";
import { PocEditor } from "./PocEditor";

interface PocDraftViewProps {
  draft: PocDraft;
  onSave: (
    expectedRevisionId: string,
    updates: Partial<Record<PocSectionName, string | null>>,
  ) => Promise<PocDraft>;
  onReload: () => Promise<void>;
}

export function PocDraftView({ draft, onSave, onReload }: PocDraftViewProps) {
  return (
    <section className="poc-draft" aria-labelledby="poc-draft-title">
      <div className="poc-title-row">
        <div>
          <p className="poc-breadcrumb">POC drafts / Selected deficiency</p>
          <h1 id="poc-draft-title">Plan of Correction</h1>
          <p>Five-part unapproved draft for deficiency {draft.deficiency_id}</p>
        </div>
        <span className="poc-revision">Unapproved · Revision {draft.revisions.length}</span>
      </div>
      <PocEditor draft={draft} onSave={onSave} onReload={onReload} />
    </section>
  );
}