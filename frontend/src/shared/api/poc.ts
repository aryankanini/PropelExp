import { apiUrl } from "./client";

export const pocSectionOrder = [
  "affected_residents",
  "others_at_risk",
  "corrective_measures",
  "monitoring",
  "completion_date",
] as const;

export type PocSectionName = (typeof pocSectionOrder)[number];
export type SectionOrigin = "ai_generated" | "user_edited";

export interface SupportReference {
  kind: "reviewed_field" | "evidence_span";
  reference_id: string;
}

export interface GroundedClaimContract {
  kind: "supported_claim";
  section: PocSectionName;
  text: string;
  support_references: readonly SupportReference[];
}

export interface MissingInformationContract {
  kind: "missing_information";
  marker_id: string;
  section: PocSectionName;
  required_fact: string;
}

export type PocContent = Readonly<Record<PocSectionName, string>>;

export interface PocRevision {
  revision_id: string;
  deficiency_revision_id: string;
  content: PocContent;
  section_origins: Readonly<Record<PocSectionName, SectionOrigin>>;
  grounded_claims: readonly GroundedClaimContract[];
  missing_information: readonly MissingInformationContract[];
  status: "unapproved";
}

export interface PocDraft {
  deficiency_id: string;
  revisions: readonly PocRevision[];
  current_revision_id: string;
}

export interface PocProblem {
  code: string;
  message: string;
  correlation_id: string;
  retryable: boolean;
  action: "none" | "retry" | "reload";
  status: number;
}

export class PocApiError extends Error {
  constructor(readonly problem: PocProblem) {
    super(problem.message);
    this.name = "PocApiError";
  }
}

export interface PocApi {
  generate(deficiencyId: string): Promise<PocDraft>;
  load(deficiencyId: string): Promise<PocDraft>;
  save(
    deficiencyId: string,
    expectedRevisionId: string,
    sectionUpdates: Partial<Record<PocSectionName, string | null>>,
  ): Promise<PocDraft>;
}

export function createPocApi(
  sessionId: string,
  fetcher: typeof fetch = fetch,
): PocApi {
  const request = async (path: string, init?: RequestInit): Promise<PocDraft> => {
    const response = await fetcher(apiUrl(path), {
      ...init,
      headers: {
        "X-Session-ID": sessionId,
        ...(init?.headers ?? {}),
      },
    });
    const payload: unknown = await response.json();
    if (!response.ok) {
      throw new PocApiError(parseProblem(payload));
    }
    return parsePocDraft(payload);
  };

  return {
    generate: (deficiencyId) =>
      request(`/deficiencies/${encodeURIComponent(deficiencyId)}/poc`, {
        method: "POST",
      }),
    load: (deficiencyId) =>
      request(`/deficiencies/${encodeURIComponent(deficiencyId)}/poc`),
    save: (deficiencyId, expectedRevisionId, sectionUpdates) =>
      request(`/deficiencies/${encodeURIComponent(deficiencyId)}/poc`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          expected_revision_id: expectedRevisionId,
          section_updates: sectionUpdates,
        }),
      }),
  };
}

export function parsePocDraft(value: unknown): PocDraft {
  const draft = record(value, "POC draft");
  const revisions = array(draft.revisions, "revisions").map(parseRevision);
  const currentRevisionId = text(draft.current_revision_id, "current_revision_id");
  if (revisions.length === 0 || revisions.at(-1)?.revision_id !== currentRevisionId) {
    throw new Error("POC response does not identify its latest revision.");
  }
  exactKeys(draft, ["deficiency_id", "revisions", "current_revision_id"], "POC draft");
  return {
    deficiency_id: text(draft.deficiency_id, "deficiency_id"),
    revisions,
    current_revision_id: currentRevisionId,
  };
}

function parseRevision(value: unknown): PocRevision {
  const revision = record(value, "POC revision");
  exactKeys(
    revision,
    [
      "revision_id",
      "deficiency_revision_id",
      "content",
      "section_origins",
      "grounded_claims",
      "missing_information",
      "status",
    ],
    "POC revision",
  );
  if (revision.status !== "unapproved") {
    throw new Error("Only unapproved POC drafts can be edited.");
  }
  return {
    revision_id: text(revision.revision_id, "revision_id"),
    deficiency_revision_id: text(
      revision.deficiency_revision_id,
      "deficiency_revision_id",
    ),
    content: sectionRecord(revision.content, text),
    section_origins: sectionRecord(revision.section_origins, origin),
    grounded_claims: array(revision.grounded_claims, "grounded_claims").map(
      parseGroundedClaim,
    ),
    missing_information: array(
      revision.missing_information,
      "missing_information",
    ).map(parseMissingInformation),
    status: "unapproved",
  };
}

function parseGroundedClaim(value: unknown): GroundedClaimContract {
  const claim = record(value, "grounded claim");
  exactKeys(claim, ["kind", "section", "text", "support_references"], "grounded claim");
  if (claim.kind !== "supported_claim") {
    throw new Error("Unknown grounded claim kind.");
  }
  const references = array(claim.support_references, "support_references").map(
    (item): SupportReference => {
      const reference = record(item, "support reference");
      exactKeys(reference, ["kind", "reference_id"], "support reference");
      if (reference.kind !== "reviewed_field" && reference.kind !== "evidence_span") {
        throw new Error("Unknown support reference kind.");
      }
      return {
        kind: reference.kind,
        reference_id: text(reference.reference_id, "reference_id"),
      };
    },
  );
  if (references.length === 0) {
    throw new Error("Grounded claims require a support reference.");
  }
  return {
    kind: "supported_claim",
    section: sectionName(claim.section),
    text: text(claim.text, "claim text"),
    support_references: references,
  };
}

function parseMissingInformation(value: unknown): MissingInformationContract {
  const marker = record(value, "missing information marker");
  exactKeys(marker, ["kind", "marker_id", "section", "required_fact"], "marker");
  if (marker.kind !== "missing_information") {
    throw new Error("Unknown missing information marker kind.");
  }
  return {
    kind: "missing_information",
    marker_id: text(marker.marker_id, "marker_id"),
    section: sectionName(marker.section),
    required_fact: text(marker.required_fact, "required_fact"),
  };
}

function parseProblem(value: unknown): PocProblem {
  const problem = record(value, "problem response");
  const action = problem.action;
  if (action !== "none" && action !== "retry" && action !== "reload") {
    throw new Error("Unknown recovery action.");
  }
  return {
    code: text(problem.code, "problem code"),
    message: text(problem.message, "problem message"),
    correlation_id: text(problem.correlation_id, "correlation_id"),
    retryable: boolean(problem.retryable, "retryable"),
    action,
    status: number(problem.status, "status"),
  };
}

function sectionRecord<T>(
  value: unknown,
  parseValue: (item: unknown, name: string) => T,
): Record<PocSectionName, T> {
  const sectionValues = record(value, "POC sections");
  exactKeys(sectionValues, pocSectionOrder, "POC sections");
  return Object.fromEntries(
    pocSectionOrder.map((name) => [name, parseValue(sectionValues[name], name)]),
  ) as Record<PocSectionName, T>;
}

function sectionName(value: unknown): PocSectionName {
  if (typeof value !== "string" || !pocSectionOrder.includes(value as PocSectionName)) {
    throw new Error("Unknown POC section.");
  }
  return value as PocSectionName;
}

function origin(value: unknown, name: string): SectionOrigin {
  if (value !== "ai_generated" && value !== "user_edited") {
    throw new Error(`${name} has an unknown origin.`);
  }
  return value;
}

function record(value: unknown, name: string): Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new Error(`${name} must be an object.`);
  }
  return value as Record<string, unknown>;
}

function array(value: unknown, name: string): readonly unknown[] {
  if (!Array.isArray(value)) {
    throw new Error(`${name} must be an array.`);
  }
  return value;
}

function text(value: unknown, name: string): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${name} must be non-empty text.`);
  }
  return value;
}

function boolean(value: unknown, name: string): boolean {
  if (typeof value !== "boolean") {
    throw new Error(`${name} must be boolean.`);
  }
  return value;
}

function number(value: unknown, name: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new Error(`${name} must be a number.`);
  }
  return value;
}

function exactKeys(
  value: Record<string, unknown>,
  expected: readonly string[],
  name: string,
): void {
  const actual = Object.keys(value);
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) {
    throw new Error(`${name} has missing, unknown, or reordered fields.`);
  }
}