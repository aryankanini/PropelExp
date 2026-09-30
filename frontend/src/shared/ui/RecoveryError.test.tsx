import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { mapTerminalFailure } from "../model/problem";
import { RecoveryError } from "./RecoveryError";

describe("RecoveryError", () => {
  it("announces safe details once with exactly one action", () => {
    const error = mapTerminalFailure(
      {
        operation: "OCR on pages 29-31",
        retainedWork: "Validated pages and provider fields",
        correlationId: "OCR-4F82",
        retryable: true,
      },
      "The failed operation remains incomplete.",
    );

    render(<RecoveryError error={error} onAction={() => undefined} />);

    expect(screen.getAllByRole("alert")).toHaveLength(1);
    expect(screen.getAllByRole("button")).toHaveLength(1);
    expect(screen.getByText("Correlation ID: OCR-4F82")).toBeInTheDocument();
    expect(screen.queryByText(/provider payload/i)).not.toBeInTheDocument();
  });

  it("blocks duplicate submissions while recovery is active", async () => {
    let finish: (() => void) | undefined;
    const onAction = vi.fn(
      () => new Promise<void>((resolve) => {
        finish = resolve;
      }),
    );
    const error = mapTerminalFailure(
      {
        operation: "POC generation",
        retainedWork: "Reviewed revision 3",
        correlationId: "POC-61E9",
        retryable: true,
      },
      "Generation failed.",
    );
    render(<RecoveryError error={error} onAction={onAction} />);
    const button = screen.getByRole("button");

    fireEvent.click(button);
    fireEvent.click(button);

    expect(onAction).toHaveBeenCalledTimes(1);
    expect(button).toBeDisabled();
    finish?.();
  });
});