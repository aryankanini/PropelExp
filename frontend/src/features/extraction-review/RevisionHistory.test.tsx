import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { RevisionHistory } from "./RevisionHistory";

describe("RevisionHistory", () => {
  it("keeps historical approval separate from the current edited origin", () => {
    render(
      <RevisionHistory
        revisions={[
          { revisionId: "revision-1", revisionNumber: 1, value: "Original", origin: "Extracted", evidence: null, current: false },
          { revisionId: "revision-2", revisionNumber: 2, value: "Approved value", origin: "Approved", evidence: null, current: false },
          { revisionId: "revision-3", revisionNumber: 3, value: "Edited value", origin: "User-edited", evidence: null, current: true },
        ]}
      />,
    );

    expect(screen.getByText("Approved")).toBeInTheDocument();
    expect(screen.getByText("User-edited")).toBeInTheDocument();
    expect(screen.getByText("Current").closest("li")).toHaveTextContent("Edited value");
  });
});