import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import {
  PocApiError,
  pocSectionOrder,
  type PocApi,
  type PocDraft,
  type PocProblem,
  type PocSectionName,
} from "../../shared/api/poc";
import { PocAuthoringPage } from "./PocAuthoringPage";

function draft(
  revisionId = "revision-1",
  options: { marker?: boolean; edited?: PocSectionName } = {},
): PocDraft {
  const marker = options.marker
    ? [{
        kind: "missing_information" as const,
        marker_id: "marker-risk",
        section: "others_at_risk" as const,
        required_fact: "Identify residents using mechanical lifts.",
      }]
    : [];
  return {
    deficiency_id: "deficiency-1",
    current_revision_id: revisionId,
    revisions: [{
      revision_id: revisionId,
      deficiency_revision_id: "deficiency-revision-1",
      content: {
        affected_residents: "Resident assessment guidance.",
        others_at_risk: options.marker
          ? "[Missing information: Identify residents using mechanical lifts.]"
          : "Review other residents at risk.",
        corrective_measures: "Educate staff on transfer procedures.",
        monitoring: "Audit transfers weekly.",
        completion_date: "Record a supported completion date.",
      },
      section_origins: Object.fromEntries(
        pocSectionOrder.map((name) => [
          name,
          name === options.edited ? "user_edited" : "ai_generated",
        ]),
      ) as Record<PocSectionName, "ai_generated" | "user_edited">,
      grounded_claims: [{
        kind: "supported_claim",
        section: "affected_residents",
        text: "The reviewed record identifies a transfer concern.",
        support_references: [{ kind: "evidence_span", reference_id: "page-12-span-4" }],
      }],
      missing_information: marker,
      status: "unapproved",
    }],
  };
}

function api(overrides: Partial<PocApi> = {}): PocApi {
  return {
    generate: vi.fn().mockResolvedValue(draft()),
    load: vi.fn().mockResolvedValue(draft("revision-current")),
    save: vi.fn().mockResolvedValue(draft("revision-2", { edited: "monitoring" })),
    ...overrides,
  };
}

describe("POC authoring", () => {
  it("blocks generation for an unconfirmed revision with an explicit reason", () => {
    const client = api();
    render(<PocAuthoringPage confirmed={false} api={client} />);
    expect(screen.getByRole("button", { name: "Generate POC" })).toBeDisabled();
    expect(screen.getByText(/confirm the current deficiency revision/i)).toBeVisible();
    expect(client.generate).not.toHaveBeenCalled();
  });

  it("coalesces pending clicks and shows one unapproved five-section draft", async () => {
    let resolveGeneration: ((value: PocDraft) => void) | undefined;
    const generate = vi.fn(() => new Promise<PocDraft>((resolve) => {
      resolveGeneration = resolve;
    }));
    render(<PocAuthoringPage api={api({ generate })} />);
    const button = screen.getByRole("button", { name: "Generate POC" });
    fireEvent.click(button);
    fireEvent.click(button);
    expect(generate).toHaveBeenCalledTimes(1);
    resolveGeneration?.(draft());
    expect(await screen.findByText("Unapproved · Revision 1")).toBeVisible();
    expect(screen.getAllByRole("heading", { level: 2 }).filter((heading) => /^\d\./.test(heading.textContent ?? ""))).toHaveLength(5);
  });

  it("keeps a rejected generated response out of completed presentation", async () => {
    render(<PocAuthoringPage api={api({ generate: vi.fn().mockRejectedValue(new Error("POC sections has missing, unknown, or reordered fields.")) })} />);
    fireEvent.click(screen.getByRole("button", { name: "Generate POC" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Draft response rejected");
    expect(screen.queryByText(/Unapproved · Revision/)).not.toBeInTheDocument();
  });

  it("renders grounded claims with navigable evidence while generic guidance remains normal", async () => {
    render(<PocAuthoringPage api={api()} />);
    fireEvent.click(screen.getByRole("button", { name: "Generate POC" }));
    const link = await screen.findByRole("link", { name: "Evidence page-12-span-4" });
    expect(link).toHaveAttribute("href", "#support-evidence_span-page-12-span-4");
    expect(screen.getByDisplayValue("Audit transfers weekly.")).toBeVisible();
  });

  it("names unsupported information, blocks readiness, and saves a user-edited replacement", async () => {
    const save = vi.fn().mockResolvedValue(draft("revision-2", { edited: "others_at_risk" }));
    render(<PocAuthoringPage api={api({ generate: vi.fn().mockResolvedValue(draft("revision-1", { marker: true })), save })} />);
    fireEvent.click(screen.getByRole("button", { name: "Generate POC" }));
    expect(await screen.findByText("Approval readiness blocked")).toBeVisible();
    expect(screen.getAllByText("Identify residents using mechanical lifts.").length).toBeGreaterThan(0);
    const replacement = screen.getByLabelText(/supported replacement for other residents/i);
    fireEvent.change(replacement, { target: { value: "Residents 4 and 8 were reviewed on September 20." } });
    fireEvent.click(screen.getByRole("button", { name: "Save revision" }));
    await waitFor(() => expect(save).toHaveBeenCalledWith("deficiency-1", "revision-1", {
      others_at_risk: "Residents 4 and 8 were reviewed on September 20.",
    }));
    expect(await screen.findByDisplayValue("Review other residents at risk.")).toBeVisible();
    const section = screen.getByRole("heading", { name: "2. Other residents at risk" }).closest("section");
    expect(section && within(section).getByText("User-edited")).toBeVisible();
  });

  it("edits all five stable sections and submits the current revision", async () => {
    const save = vi.fn().mockResolvedValue(draft("revision-2"));
    render(<PocAuthoringPage api={api({ save })} />);
    fireEvent.click(screen.getByRole("button", { name: "Generate POC" }));
    await screen.findByText("Unapproved · Revision 1");
    for (const textarea of screen.getAllByRole("textbox")) {
      fireEvent.change(textarea, { target: { value: `${textarea.getAttribute("id")} updated` } });
    }
    fireEvent.click(screen.getByRole("button", { name: "Save revision" }));
    await waitFor(() => expect(save).toHaveBeenCalledWith("deficiency-1", "revision-1", expect.objectContaining({
      affected_residents: "poc-affected_residents updated",
      completion_date: "poc-completion_date updated",
    })));
    expect(Object.keys(save.mock.calls[0]?.[2] as object)).toHaveLength(5);
  });

  it("retains local edits after save failure and retries the same revision", async () => {
    const save = vi.fn()
      .mockRejectedValueOnce(new Error("Temporary retention failure."))
      .mockResolvedValueOnce(draft("revision-2", { edited: "monitoring" }));
    render(<PocAuthoringPage api={api({ save })} />);
    fireEvent.click(screen.getByRole("button", { name: "Generate POC" }));
    const monitoring = await screen.findByLabelText("Monitoring");
    fireEvent.change(monitoring, { target: { value: "Retained local monitoring edit." } });
    fireEvent.click(screen.getByRole("button", { name: "Save revision" }));
    expect(await screen.findByText(/your local edits are retained/i)).toBeVisible();
    expect(monitoring).toHaveValue("Retained local monitoring edit.");
    fireEvent.click(screen.getByRole("button", { name: "Retry save" }));
    await waitFor(() => expect(save).toHaveBeenCalledTimes(2));
    expect(save.mock.calls[1]?.[1]).toBe("revision-1");
  });

  it("does not overwrite a stale revision and reloads only on explicit action", async () => {
    const problem: PocProblem = {
      code: "stale_revision",
      message: "The draft changed before this edit could be saved.",
      correlation_id: "correlation-1",
      retryable: false,
      action: "reload",
      status: 409,
    };
    const load = vi.fn().mockResolvedValue(draft("revision-current"));
    render(<PocAuthoringPage api={api({ save: vi.fn().mockRejectedValue(new PocApiError(problem)), load })} />);
    fireEvent.click(screen.getByRole("button", { name: "Generate POC" }));
    const monitoring = await screen.findByLabelText("Monitoring");
    fireEvent.change(monitoring, { target: { value: "Stale local edit." } });
    fireEvent.click(screen.getByRole("button", { name: "Save revision" }));
    expect(await screen.findByText("Newer draft available")).toBeVisible();
    expect(monitoring).toHaveValue("Stale local edit.");
    expect(load).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Reload current draft" }));
    await waitFor(() => expect(load).toHaveBeenCalledWith("deficiency-1"));
    expect(await screen.findByText("Unapproved · Revision 1")).toBeVisible();
  });
});