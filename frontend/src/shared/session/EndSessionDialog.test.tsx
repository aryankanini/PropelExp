import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { EndSessionDialog } from "./EndSessionDialog";

describe("EndSessionDialog", () => {
  it("shows retained failure and exposes an idempotent retry", () => {
    const confirm = vi.fn();
    render(
      <EndSessionDialog
        open
        pending={false}
        failed
        onCancel={() => undefined}
        onConfirm={confirm}
      />,
    );

    expect(screen.getByRole("alert")).toHaveTextContent("case remains available");
    fireEvent.click(screen.getByRole("button", { name: "Try cleanup again" }));
    expect(confirm).toHaveBeenCalledOnce();
  });
});