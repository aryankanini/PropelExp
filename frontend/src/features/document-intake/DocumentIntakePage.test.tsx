import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { SessionProvider } from "../../app/SessionContext";
import { DocumentIntakePage } from "./DocumentIntakePage";

afterEach(() => vi.restoreAllMocks());

describe("DocumentIntakePage", () => {
  function renderPage() {
    return render(
      <SessionProvider>
        <DocumentIntakePage />
      </SessionProvider>,
    );
  }

  it("selects one supported file and presents the upload action", () => {
    renderPage();
    const input = screen.getByLabelText("Select CMS-2567");
    const file = new File(["content"], "cms-2567.pdf", { type: "application/pdf" });

    fireEvent.change(input, { target: { files: [file] } });

    expect(screen.getByText("cms-2567.pdf")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Upload CMS-2567" })).toBeEnabled();
    expect(screen.getByText(/50 MB and 200 pages/)).toBeInTheDocument();
  });

  it("rejects an oversized file and provides choose-another recovery", () => {
    renderPage();
    const file = new File(["x"], "too-large.pdf", { type: "application/pdf" });
    Object.defineProperty(file, "size", { value: 50 * 1024 * 1024 + 1 });

    fireEvent.change(screen.getByLabelText("Select CMS-2567"), {
      target: { files: [file] },
    });

    expect(screen.getByRole("alert")).toHaveTextContent("exceeds the 50 MB");
    expect(screen.getByRole("button", { name: "Choose another file" })).toBeInTheDocument();
  });

  it("cancels end-session confirmation without removing the screen", () => {
    sessionStorage.setItem("cms-planner-active-case", "case-1");
    renderPage();

    fireEvent.click(screen.getByRole("button", { name: "End session" }));
    fireEvent.click(screen.getByRole("button", { name: "Cancel" }));

    expect(screen.getByRole("heading", { name: "Upload CMS-2567" })).toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});