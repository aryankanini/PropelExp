export type ContentOrigin =
  | "Extracted"
  | "AI-generated"
  | "User-edited"
  | "Approved";

export interface HighlightCoordinates {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface EvidenceDetail {
  pageNumber: number;
  fullSnippet: string;
  source: "native-text" | "ocr";
  highlight: HighlightCoordinates;
}

export interface ReviewCandidate {
  candidateId: string;
  value: string;
  confidence: number;
  uncertainty: string | null;
  origin: ContentOrigin;
  revisionId: string;
  evidence: EvidenceDetail;
}

export interface RevisionEntry {
  revisionId: string;
  revisionNumber: number;
  value: string;
  origin: ContentOrigin;
  evidence: EvidenceDetail | null;
  current: boolean;
}

export interface ReviewField {
  fieldId: string;
  deficiencyId: string;
  label: string;
  fieldType: "provider" | "f_tag" | "sod";
  candidates: readonly ReviewCandidate[];
  revisions: readonly RevisionEntry[];
  evidenceItems: readonly EvidenceDetail[];
  currentRevisionId: string;
  unresolved: boolean;
  reapprovalRequired: boolean;
  pocSuggestion: string | null;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function projectEvidence(e: any): EvidenceDetail {
  return {
    pageNumber: e.page_number,
    fullSnippet: e.full_snippet,
    source: e.source,
    highlight: { x: e.highlight.x, y: e.highlight.y, width: e.highlight.width, height: e.highlight.height },
  };
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function projectReviewField(raw: any): ReviewField {
  const currentRevisionId: string = raw.current_revision_id;
  const revisions: RevisionEntry[] = (raw.revisions ?? []).map((r: any) => ({
    revisionId: r.revision_id,
    revisionNumber: r.revision_number,
    value: r.value,
    origin: r.origin,
    evidence: r.evidence ? projectEvidence(r.evidence) : null,
    current: r.revision_id === currentRevisionId,
  }));
  const candidates: ReviewCandidate[] = (raw.candidates ?? []).map((c: any) => ({
    candidateId: c.candidate_id,
    value: c.value,
    confidence: c.confidence,
    uncertainty: c.uncertainty ?? null,
    origin: c.origin,
    revisionId: c.candidate_id,
    evidence: projectEvidence(c.evidence),
  }));
  return {
    fieldId: raw.field_id,
    deficiencyId: raw.deficiency_id,
    label: raw.label,
    fieldType: raw.field_type,
    candidates,
    revisions,
    evidenceItems: (raw.evidence_items ?? []).map(projectEvidence),
    currentRevisionId,
    unresolved: raw.unresolved ?? false,
    reapprovalRequired: raw.reapproval_required ?? false,
    pocSuggestion: raw.poc_suggestion ?? null,
  };
}

export type AsyncState = "ready" | "loading" | "empty" | "error";
