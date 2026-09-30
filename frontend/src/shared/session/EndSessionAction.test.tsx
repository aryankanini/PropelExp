import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { SessionProvider, useSession } from "../../app/SessionContext";
import { EndSessionAction } from "./EndSessionAction";

function Harness() {
  const { caseId, page, navigate } = useSession();

  return (
    <>
      <button type="button" onClick={() => navigate("poc-authoring", { caseId: "case-1" })}>
        Continue session
      </button>
      <span>{caseId ?? "no active case"}</span>
      <span>{page}</span>
      <EndSessionAction />
    </>
  );
}

describe("EndSessionAction", () => {
  beforeEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it("removes the active case and returns to intake after confirmation", async () => {
    const request = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(null, { status: 200 }),
    );

    render(
      <SessionProvider>
        <Harness />
      </SessionProvider>,
    );

    expect(screen.queryByRole("button", { name: "End session" })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Continue session" }));
    fireEvent.click(screen.getByRole("button", { name: "End session" }));
    fireEvent.click(screen.getByRole("button", { name: "End session and remove data" }));

    await waitFor(() => expect(screen.getByText("no active case")).toBeInTheDocument());
    expect(screen.getByText("intake")).toBeInTheDocument();
    expect(sessionStorage.getItem("cms-planner-active-case")).toBeNull();
    expect(request).toHaveBeenCalledWith(
      expect.stringContaining("/api/v1/cases/case-1"),
      expect.objectContaining({ method: "DELETE" }),
    );
  });
});