import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { DRAFT_EXPORT_PREFIX } from "../../shared/model/labeledExport";
import { ApprovedExport } from "./ApprovedExport";

describe("ApprovedExport", () => {
  it("renders the required label before content and exposes local actions", () => {
    const copy = vi.fn();
    render(<ApprovedExport revisionLabel="Revision 4" view={{ label: DRAFT_EXPORT_PREFIX, content: "Affected residents", empty: false }} pending={false} failureOpen={false} onCopy={copy} onDownload={() => undefined} onCloseFailure={() => undefined} />);

    const preview = screen.getByRole("heading", { name: "Export preview" }).parentElement;
    expect(preview?.textContent?.indexOf(DRAFT_EXPORT_PREFIX)).toBeLessThan(preview?.textContent?.indexOf("Affected residents") ?? 0);
    fireEvent.click(screen.getByRole("button", { name: "Copy draft" }));
    expect(copy).toHaveBeenCalledOnce();
    expect(screen.getByText("Not performed")).toBeInTheDocument();
  });

  it("disables empty export and offers retry or copy after formatting failure", () => {
    render(<ApprovedExport revisionLabel="Revision 4" view={{ label: DRAFT_EXPORT_PREFIX, content: "", empty: true }} pending={false} failureOpen onCopy={() => undefined} onDownload={() => undefined} onCloseFailure={() => undefined} />);

    expect(screen.getAllByRole("button", { name: "Copy draft" })[0]).toBeDisabled();
    expect(screen.getByRole("dialog")).toHaveTextContent("approval remains valid");
    expect(screen.getByRole("button", { name: "Retry download" })).toBeEnabled();
  });
});