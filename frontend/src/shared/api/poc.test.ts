import { describe, expect, it } from "vitest";
import { parsePocDraft } from "./poc";

function validPayload(): Record<string, unknown> {
  return {
    deficiency_id: "deficiency-1",
    revisions: [
      {
        revision_id: "revision-1",
        deficiency_revision_id: "deficiency-revision-1",
        content: {
          affected_residents: "Affected resident guidance.",
          others_at_risk: "Other resident guidance.",
          corrective_measures: "Corrective measure guidance.",
          monitoring: "Monitoring guidance.",
          completion_date: "Completion date guidance.",
        },
        section_origins: {
          affected_residents: "ai_generated",
          others_at_risk: "ai_generated",
          corrective_measures: "ai_generated",
          monitoring: "ai_generated",
          completion_date: "ai_generated",
        },
        grounded_claims: [],
        missing_information: [],
        status: "unapproved",
      },
    ],
    current_revision_id: "revision-1",
  };
}

describe("parsePocDraft", () => {
  it("accepts exactly five non-empty sections in fixed order", () => {
    expect(parsePocDraft(validPayload()).revisions[0]?.status).toBe("unapproved");
  });

  it.each([
    ["missing", (content: Record<string, unknown>) => delete content.monitoring],
    ["empty", (content: Record<string, unknown>) => { content.monitoring = " "; }],
    ["unknown", (content: Record<string, unknown>) => { content.unknown = "No."; }],
    ["reordered", (content: Record<string, unknown>) => {
      const monitoring = content.monitoring;
      delete content.monitoring;
      content.monitoring = monitoring;
    }],
  ])("rejects a %s section response", (_case, mutate) => {
    const payload = validPayload();
    const revision = (payload.revisions as Array<Record<string, unknown>>)[0];
    mutate(revision?.content as Record<string, unknown>);
    expect(() => parsePocDraft(payload)).toThrow();
  });

  it("rejects an approved response from the authoring workflow", () => {
    const payload = validPayload();
    const revision = (payload.revisions as Array<Record<string, unknown>>)[0];
    if (revision !== undefined) revision.status = "approved";
    expect(() => parsePocDraft(payload)).toThrow("Only unapproved");
  });
});