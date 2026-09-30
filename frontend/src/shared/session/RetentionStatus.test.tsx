import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { RetentionStatus } from "./RetentionStatus";

afterEach(() => vi.restoreAllMocks());

describe("RetentionStatus", () => {
  it("refreshes server-owned time after reconnect", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({ storage: "session_only", remaining_inactivity_seconds: 3000 })))
      .mockResolvedValueOnce(new Response(JSON.stringify({ storage: "session_only", remaining_inactivity_seconds: 2400 })));
    render(<RetentionStatus sessionId="session-1" active />);

    expect(await screen.findByText(/approximately 50 minutes/)).toBeInTheDocument();
    fireEvent(window, new Event("online"));

    await waitFor(() => expect(screen.getByText(/approximately 40 minutes/)).toBeInTheDocument());
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("does not describe an expired deadline as approximately zero minutes", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({
        storage: "session_only",
        remaining_inactivity_seconds: 0,
        active_case_id: "case-1",
      })),
    );

    render(<RetentionStatus sessionId="session-1" active />);

    expect(await screen.findByText(/case is expiring now/i)).toBeInTheDocument();
    expect(screen.queryByText(/approximately 0 minutes/i)).not.toBeInTheDocument();
  });
});