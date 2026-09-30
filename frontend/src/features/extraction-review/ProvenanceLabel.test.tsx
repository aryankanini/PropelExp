import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ProvenanceLabel } from "./ProvenanceLabel";
import type { ContentOrigin } from "./types";

describe("ProvenanceLabel", () => {
  it.each<ContentOrigin>([
    "Extracted",
    "AI-generated",
    "User-edited",
    "Approved",
  ])("renders the closed origin %s with its revision", (origin) => {
    render(<ProvenanceLabel origin={origin} revisionNumber={4} />);

    expect(screen.getByText(origin)).toBeInTheDocument();
    expect(screen.getByText("Revision 4")).toBeInTheDocument();
  });

  it("labels an edited approval for reapproval", () => {
    render(
      <ProvenanceLabel
        origin="User-edited"
        revisionNumber={5}
        reapprovalRequired
      />,
    );

    expect(screen.getByText("Reapproval required")).toBeInTheDocument();
    expect(screen.queryByText("Approved")).not.toBeInTheDocument();
  });
});