import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { DocumentValidationStatus } from "./DocumentValidationStatus";

describe("DocumentValidationStatus", () => {
  it("shows readiness without claiming extraction completion", () => {
    render(
      <DocumentValidationStatus
        accepted={{
          status: "extraction_ready",
          case_id: "case-1",
          upload_id: "upload-1",
          size_bytes: 10,
          page_count: 2,
        }}
      />,
    );

    expect(screen.getByText("Document is extraction-ready.")).toBeInTheDocument();
    expect(screen.getByText(/Extraction has not started/)).toBeInTheDocument();
  });

  it("reports extraction progress after the job starts", () => {
    render(
      <DocumentValidationStatus
        accepted={{
          status: "extraction_ready",
          case_id: "case-1",
          upload_id: "upload-1",
          size_bytes: 100,
          page_count: 9,
        }}
        extractionStarted
      />,
    );

    expect(screen.getByText(/Extraction is in progress/)).toBeInTheDocument();
    expect(screen.queryByText(/Extraction has not started/)).not.toBeInTheDocument();
  });

  it("announces a server rejection without extraction results", () => {
    render(<DocumentValidationStatus rejection="The document is not identifiable as CMS-2567." />);

    expect(screen.getByRole("alert")).toHaveTextContent("No extraction results were created");
  });
});